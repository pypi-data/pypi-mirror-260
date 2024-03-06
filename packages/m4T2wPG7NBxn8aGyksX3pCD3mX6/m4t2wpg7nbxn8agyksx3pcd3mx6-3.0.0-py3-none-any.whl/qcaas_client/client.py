# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Oxford Quantum Circuits Ltd
import logging
import re
import threading
import warnings
from datetime import datetime
from functools import wraps
from json import JSONDecodeError
from time import sleep
from typing import List, Optional, Union
from urllib.parse import urlparse
from uuid import uuid4
from importlib.metadata import version, PackageNotFoundError
import requests
from qcaas_common.enums import ClientTaskStatus as TaskStatus

from scc.compiler.config import CompilerConfig
from collections import defaultdict


class ServerException(Exception):
    """Generic exception thrown back from the server."""

    def __init__(self, message, server_error_code, metadata=None):
        super().__init__(message)
        self.server_error_code = server_error_code
        self.metadata = metadata or dict()


class ExpiredTokenException(ServerException):
    """Exception for handling expired token errors from server requests"""

    pass


class QPUTask:
    """
    Payload for executing tasks on a QPU. Program is the QASM program to be executed.
    """

    def __init__(
        self,
        program: str,
        config: CompilerConfig = None,
        task_id=None,
        hybrid_marker=None,
        qpu_id=None,
        tag="",
    ):
        self.task_id = task_id
        self.program = program
        self.config: CompilerConfig = config or CompilerConfig()
        self.hybrid_marker: Optional[str] = hybrid_marker
        self.qpu_id: Optional[str] = qpu_id
        self.tag: Optional[str] = tag

    def to_json(self):
        task = {
            "task_id": self.task_id or -1,
            "program": self.program,
            "config": self.config.to_json(),
            "qpu_id": self.qpu_id,
            "tag": self.tag,
        }
        if self.hybrid_marker:
            task["hybrid_marker"] = self.hybrid_marker
        return task


class QPUTaskResult:

    def __init__(self, id_, result=None, metrics=None, error_details=None):
        self.id = id_
        self.result = result
        self.metrics = metrics or dict()
        self.error_details: QPUTaskErrors = error_details

    def has_errored(self):
        return self.error_details is not None


class QPUTaskErrors:

    def __init__(self, error_message, error_code=None):
        self.error_code = error_code or -1
        self.error_message = error_message


def retry_on_expired_token(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ExpiredTokenException:
            self._authentication_token = None
            return func(self, *args, **kwargs)

    return wrapper


def _get_unscheduled_tasks_results(tasks, scheduled_tasks) -> list[str]:
    results = []
    unscheduled_tasks = [task for task in tasks if task not in scheduled_tasks]
    for task in unscheduled_tasks:
        results.append(
            QPUTaskResult(
                id_=task.task_id,
                error_details=QPUTaskErrors("Failed to schedule task."),
            ))
    return results


class OQCClient:

    def __init__(self, url, email=None, password=None, timeout=(5, 25),
                 authentication_token=None):
        self.server_version = None
        self._authentication_token = authentication_token
        self._qpus = None
        self.timeout = timeout
        self.default_qpu_id = "qpu:uk:2:0eb3cf2363"
        if email:
            self._email = _validated_email(email)
        else:
            self._email = None
        if password:
            self._password = _validated_password(password)
        else:
            self._password = None

        if url is None:
            raise ValueError("Need a URL to connect too.")

        if (email and not password) or (password and not email):
            raise ValueError(
                "If one of email and password are provided, both must be provided")

        if authentication_token and (email or password):
            raise ValueError(
                "If one authentication_token is specified, email and password must not be specified"
            )

        # build the user agent
        ver = ""
        try:
            ver = version("qcaas_client")
        except Exception:
            pass
        self.user_agent_string = "QCaaS Client " + ver

        self.server_lock = threading.Lock()

        # get the server version
        self.url = _validated_url(url)
        vesion = self._get("/admin/version", authenticate=False).json()
        self.server_version = vesion["version"]
        if self.server_version == 2 and authentication_token:
            raise ValueError(
                "You can't provide an authentication_token for this server")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = _validated_email(value)
        self._authentication_token = None  # Clear existing token to force re-auth.

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = _validated_password(value)
        self._authentication_token = None  # Clear existing token to force re-auth.

    def _handle_response_error(self, response):
        if not self.server_version and response.status_code != 200:
            raise ServerException(response.content.decode("utf-8"),
                                  response.status_code)
        if self.server_version and self.server_version >= 3 and response.status_code == 401:
            raise ServerException("Authentication Error", response.status_code, {})

        if response.status_code != 200:
            # Right now we can, occasionally, return HTML blobs. Looks ugly,
            # but better than parsing exception.
            if not response.headers.get("content-type",
                                        "").startswith("application/json"):
                raise ServerException(response.content.decode("utf-8"),
                                      response.status_code)
            else:
                exception_info = response.json()
                exception_keys = exception_info.keys()
                if self.server_version >= 3 and "response" in exception_info:
                    raise ServerException(
                        exception_info["response"]["errors"][0],
                        response.status_code,
                        exception_info,
                    )
                else:
                    if "message" in exception_keys:
                        message = exception_info.pop("message")
                    elif "msg" in exception_keys:
                        message = exception_info.pop("msg")
                    elif "failed_tasks" in exception_keys:
                        message = exception_info.pop("failed_tasks")
                    else:
                        raise ServerException(
                            f"Request failed but exception "
                            f"message malformed. {str(exception_info)}",
                            response.status_code,
                            exception_info,
                        )
                    # FEATURE REQUEST: Replace string match;
                    # requires configuring JWT expired error
                    if "Token has expired" in message:
                        raise ExpiredTokenException(message, exception_info)
                    else:
                        raise ServerException(message, response.status_code,
                                              exception_info)

    def _handle_response_messages(self, response):
        try:
            response = response.json()
            if isinstance(response, dict):
                messages = [response.get("message", "")]
                messages.extend(response.get("messages", []))
                for message in messages:
                    if message != "":
                        if message.startswith("Warning"):
                            warnings.warn(message)
                        else:
                            logging.info(message)
        except JSONDecodeError:
            pass

    @retry_on_expired_token
    def _put(self, endpoint, data=None, authenticate=True, json=None, **kwargs):
        """Helper for put requests. Applies common info such as headers etc."""
        if authenticate:
            self.authenticate()
        headers = kwargs.get("headers", self._build_headers(json_content=True))
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        response = requests.put(
            endpoint,
            data,
            json=json,
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        self._handle_response_error(response)
        self._handle_response_messages(response)

        return response

    @retry_on_expired_token
    def _get(self, endpoint, params=None, data=None, json=None, authenticate=True,
             **kwargs):
        """Helper for get requests. Applies common info such as headers etc."""
        if authenticate:
            self.authenticate()
        headers = kwargs.get("headers", self._build_headers())
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        response = requests.get(
            endpoint,
            params,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        self._handle_response_error(response)
        self._handle_response_messages(response)

        return response

    @retry_on_expired_token
    def _post(self, endpoint, json=None, data=None, authenticate=True, **kwargs):
        """Helper for post requests. Applies common info such as headers etc."""
        if authenticate:
            self.authenticate()
        auth_headers = self._build_headers()
        headers = kwargs.pop("headers") if kwargs.get("headers") is not None else {}
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        response = requests.post(
            endpoint,
            data,
            json,
            headers=headers | auth_headers,
            timeout=self.timeout,
            **kwargs,
        )
        self._handle_response_error(response)
        self._handle_response_messages(response)

        return response

    @retry_on_expired_token
    def _delete(self, endpoint, json=None, data=None, authenticate=True, **kwargs):
        """Helper for post requests. Applies common info such as headers etc."""
        if authenticate:
            self.authenticate()
        auth_headers = self._build_headers()
        headers = kwargs.pop("headers") if kwargs.get("headers") is not None else {}
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        response = requests.delete(
            endpoint,
            data,
            json,
            headers=headers | auth_headers,
            timeout=self.timeout,
            **kwargs,
        )
        self._handle_response_error(response)
        self._handle_response_messages(response)

        return response

    def authenticate(self):
        if (self._email is None
                and self._password is None) or self._authentication_token is not None:
            return

        payload = {"email": self._email or "", "password": self._password or ""}
        if self.server_version == 3:
            logout = self._post("/admin/logout", {}, authenticate=False)
            auth = self._post("/admin/login?include_auth_token=true", payload,
                              authenticate=False)
            self._handle_response_messages(auth)
            response = auth.json()
            self._authentication_token = response["response"]["user"][
                "authentication_token"]
        else:
            auth = self._post("/auth", payload, authenticate=False)
            self._handle_response_messages(auth)
            response = auth.json()
            self._authentication_token = response["access_token"]

        return self._authentication_token is not None

    def get_qpus(self):
        qpus = self._get("/admin/qpu").json()
        return qpus["items"]

    def _get_qpu_endpoint(self, qpu_id=None):
        if self.server_version == 2:
            return ""
        if qpu_id is None or qpu_id == "" or qpu_id == "lucy":
            qpu_id = self.default_qpu_id
        if not self._qpus:
            self._qpus = self.get_qpus()

        try:
            url = next(qpu["url"] for qpu in self._qpus if qpu["id"] == qpu_id)
            return url
        except StopIteration:
            raise ValueError(f"Invalid qpu_id: {qpu_id}")

    def _build_headers(self, json_content=False):
        """Create authentication header."""
        headers = dict()
        headers["User-agent"] = self.user_agent_string
        if self._authentication_token is not None:
            if self.server_version == 3:
                headers["Authentication-Token"] = self._authentication_token
            else:
                headers["Authorization"] = f"Bearer {self._authentication_token}"

        if json_content:
            headers["Content-Type"] = "application/json"

        return headers

    def get_token_expiry_time(self) -> Optional[str]:
        if self._authentication_token is None:
            return None
        if self.server_version == 3:
            auth_token = self._get(
                f"/admin/auth_tokens/{self._authentication_token}").json()
            expires_at = auth_token["expires_at"]
            expires_timestamp = int(
                datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S").timestamp())
            return expires_timestamp
        else:
            return self._get("/admin/token_expiry").json()

    def change_password(self, email, password, validate=True):
        """Change the users password"""
        if self.server_version == 3:
            user = self.get_user_info(email, validate)
            if user:
                response = self._post(
                    f"/admin/users/{user['id']}/update_password",
                    json={
                        "password":
                        (_validated_password(password) if validate else password),
                        "password_confirm":
                        (_validated_password(password) if validate else password),
                    },
                )
            else:
                return None
        else:
            response = self._put(
                "/admin/users/passwords",
                json={
                    "email": _validated_email(email) if validate else email,
                    "password": _validated_password(password) if validate else password,
                },
            )

        # If we're updating our own password, re-assign for re-auth.
        if response.status_code == 200 and self.email == email:
            self.password = password
        return response

    def get_password_expiry_time(self, email, validate=True) -> Optional[str]:
        if self.server_version == 3:
            user = self.get_user_info(email, validate)
            if user:
                results = self._get(f"/admin/users/{user['id']}").json()
            else:
                return None
        else:
            results = self._get(
                "/admin/users/password_expiry",
                {
                    "email": _validated_email(email) if validate else email
                },
            ).json()
        return results.get("password_expires_at", None)

    def get_user_info(self, email, validate=True):
        if self.server_version == 3:
            results = self._get(
                f"/admin/users?q={_validated_email(email) if validate else email}"
            ).json()

            if results["total"] > 0:
                return results["items"][0]
            else:
                return None
        else:
            results = self._get(
                "/admin/users",
                {
                    "email": _validated_email(email) if validate else email
                },
            ).json()
            return results

    def get_next_window(self):
        """
        Fetches the next active window.

        Note: Currently _only_ AWS windows are defined, this endpoint
        will take a type of window defined once that is defined.
        """
        next_window_dict = self._get("/windows/next").json()

        if next_window_dict == {} or "next_window" not in next_window_dict:
            return None

        return _validate_datetime_format(
            next_window_dict.get("next_window").get("starting"))

    def create_one_off_window_(
        self,
        qpu_id,
        start_datetime,
        end_datetime,
        lease_type,
        lease_holder_name,
        duration_hours,
        window_name,
        window_start,
    ):
        params = {
            "qpu_id": qpu_id,
            "start_time": start_datetime,
            "end_time": end_datetime,
            "lease_type": lease_type,
            "lease_holder_name": lease_holder_name,
            "duration_hours": duration_hours,
            "window_name": window_name,
            "window_start": window_start,
        }

        return self._post("/windows/one-off-window", params)

    def get_dedicated_window_history(self, latest=False):
        params = {}
        if isinstance(latest, bool) and latest is True:
            params["latest"] = True

        return self._get("/windows/history", params).json()

    def password_reset(self, email, validate=True):
        """
        Sends an email to a user for them to reset a password.
        """
        self._post(
            "/password_reset",
            data={"email": _validated_email(email) if validate else email},
        )

    def create_auth_token(self, expires_at):
        """
        Create a new auth token.
        """
        if self.server_version < 3:
            raise ValueError("You can't use auth tokens on this server")

        try:
            date = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("expires_at must be in the format 2024-12-31T23:59:59")

        token = self._post(
            "/admin/users/current_user/auth_tokens",
            json={"expires_at": expires_at},
        )
        self._handle_response_messages(token)
        response = token.json()
        return response["token"]

    def delete_auth_token(self, token):
        """
        Create a new auth token.
        """
        if self.server_version < 3:
            raise ValueError("You can't use auth tokens on this server")
        token = self._delete(f"/auth_tokens/{token}")
        self._handle_response_messages(token)
        response = token.json()
        return response["token"]

    def get_system_status(self):
        # FEATURE REQUEST: Result format may need expanding/making nicer.
        return self._get("/monitoring/statuses").json()

    def get_calibration(self, qpu_id=None, date_filter=None):
        # FEATURE REQUEST: Find precise format of date filter,
        # align with types or parsing.
        if qpu_id is None or qpu_id == "lucy":
            qpu_id = self.default_qpu_id
        params = {"qpu_id": qpu_id}
        if date_filter is not None:
            params["date"] = str(date_filter)
        return self._get("/monitoring/calibrations", params).json()

    def get_features(self, qpu_id=None, date_filter=None):
        if qpu_id is None or qpu_id == "lucy":
            qpu_id = self.default_qpu_id
        params = {"qpu_id": qpu_id}
        if date_filter is not None:
            params["date"] = str(date_filter)
        return self._get("/monitoring/features", params).json()

    # Retry attempt = index of next attempted request delay.
    retry_cadence = [1, 2, 5, 8, 10, 15, 30]

    def execute_tasks(
        self,
        tasks: Union[QPUTask, List[QPUTask]],
        include_metrics=False,
    ) -> List[QPUTaskResult]:
        """
        Executes the QPU tasks and then blocks until a results are retrieved for all
        of them. Automatically disconnects socket unless auto_disconnect=False.
        """
        scheduled_tasks = self.schedule_tasks(tasks)

        def retry_delay(attempt):
            if attempt > len(self.retry_cadence):
                return self.retry_cadence[-1]

            if attempt <= 0:
                return self.retry_cadence[0]

            return self.retry_cadence[attempt - 1]

        # FEATURE REQUEST: Add processing timeout.
        results = []
        scheduled_count = len(scheduled_tasks)
        current_task_index = 0
        retry_attempt = 0
        while current_task_index < scheduled_count:
            scheduled_task = scheduled_tasks[current_task_index]
            task_info = self.get_task(scheduled_task.task_id)
            status = self._get_task_status(task_info)
            if status == TaskStatus.FAILED.value:
                logging.info(f"{scheduled_task.task_id} failed execution.")
                error_details = self._get_task_errors(task_info)
                results.append(
                    QPUTaskResult(scheduled_task.task_id, error_details=error_details))
            elif status == TaskStatus.COMPLETED.value:
                logging.info(f"{scheduled_task.task_id} completed execution.")
                qpu_result = self._get_task_results(scheduled_task.task_id, task_info)
                if include_metrics:
                    qpu_result.metrics = self.get_task_metrics(scheduled_task.task_id)
                results.append(qpu_result)

            # If we have a new result, process the next block, otherwise
            # retry with increasing delay.
            if current_task_index != len(results):
                current_task_index = len(results)
                retry_attempt = 0
            else:
                logging.info(f"Still waiting on {scheduled_task.task_id}...")
                retry_attempt += 1
                sleep(retry_delay(retry_attempt))

        if not isinstance(tasks, list):
            tasks = [tasks]

        results.extend(_get_unscheduled_tasks_results(tasks, scheduled_tasks))

        return results

    def create_task_ids(self, ntasks: int, qpu_id: str = None,
                        tag: str = None) -> List[str]:
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            return self._post(f"{server}/tasks", json={
                "qpu_id": qpu_id,
                "task_count": ntasks,
                "tag": tag
            }).json()
        else:
            return self._post(f"/tasks?n={ntasks}").json()

    def schedule_tasks(self, tasks: Union[QPUTask, List[QPUTask]], qpu_id: str = None,
                       tag: str = None) -> List[QPUTask]:
        """
        Schedules all tasks to run on the QPU and updates the task objects with the
        associated run ID's. Automatically disconnects socket unless
        auto_disconnect=False. If wait for acknowledgement the set of tasks returned
        will contain only those that are confirmed to have been schedueled, otherwise
        will just return all tasks.
        """

        if not isinstance(tasks, List):
            tasks = [tasks]

        invalid_tasks = [task for task in tasks if not isinstance(task, QPUTask)]
        if any(invalid_tasks):
            raise ValueError(f"{', '.join([str(task) for task in invalid_tasks])}"
                             f" are invalid types to try and schedule.")

        if self.server_version >= 3:
            # if qpu_id is provided, set it on all tasks
            if qpu_id:
                for task in tasks:
                    task.qpu_id = qpu_id
            else:
                for task in tasks:
                    if not task.qpu_id:
                        task.qpu_id = self.default_qpu_id

                # qpu_id is not provided globally, so it must be on all tasks already
                # and must be the same on all tasks
                qpu_id = tasks[0].qpu_id
                for task in tasks:
                    if qpu_id != task.qpu_id:
                        raise ValueError("All tasks must have the same qpu_id")

        # Get task IDs from the endpoint
        uninitialized_tasks = [t for t in tasks if t.task_id is None]
        if uninitialized_tasks:
            task_ids = self.create_task_ids(len(uninitialized_tasks), qpu_id, tag)
            # Assign ID's to particular tasks. At this point the ID's have no
            # meaning beyond 'pending submission'.
            for task, task_id in zip(uninitialized_tasks, task_ids):
                task.task_id = task_id

        # With auto-disconnect on you have to wait for a response before
        # disconnecting.
        endpoint = "/tasks/submit"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        print({"tasks": [task.to_json() for task in tasks]})
        self._post(
            endpoint=endpoint,
            json={"tasks": [task.to_json() for task in tasks]},
        )
        return tasks

    def _get_task_results(self, task_id, task_info: dict):
        results = task_info.get("results", None)
        if results is None:
            return results

        return QPUTaskResult(task_id, results)

    def get_task_results(self, task_id, qpu_id: str = None) -> Optional[QPUTaskResult]:
        """
        Returns a QPUTaskResult that holds information about the tasks results
        and running. Returns none otherwise.
        """
        endpoint = f"/tasks/{str(task_id)}/results"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint

        results = self._get(endpoint).json()
        return self._get_task_results(task_id, results)

    def _get_task_errors(self, task_info: dict):
        error_details = task_info.get("task_error", None)
        if error_details is None:
            return None

        return QPUTaskErrors(
            error_details.get("error_message", "Unknown error."),
            error_details.get("error_code", -1),
        )

    def get_task_errors(self, task_id, qpu_id: str = None) -> Optional[QPUTaskErrors]:
        endpoint = f"/tasks/{str(task_id)}/error"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        errors = self._get(endpoint).json()
        return self._get_task_errors(errors)

    def get_tasks_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        qpu_id: str = None,
    ) -> list[dict]:
        url = "/tasks"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            url = server + url

        params = []
        if start_date is not None:
            params.append(f"start_date={start_date}")
        if end_date is not None:
            params.append(f"end_date={end_date}")

        url += f"?{'&'.join(params)}" if params else ""

        return self._get(url).json()

    def _get_task_status(self, task_info: dict):
        return task_info.get("status", TaskStatus.UNKNOWN.value)

    def get_task_status(self, task_id, qpu_id: str = None):
        endpoint = f"/tasks/{str(task_id)}/status"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint

        status = self._get(endpoint).json()
        return self._get_task_status(status)

    def get_task(self, task_id, qpu_id: str = None):
        endpoint = f"/tasks/{str(task_id)}/all_info"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        return self._get(endpoint).json()

    def _get_task_metrics(self, task_info: dict):
        return task_info.get("execution_metadata", None)

    def get_task_metrics(self, task_id, qpu_id: str = None):
        endpoint = f"/tasks/{str(task_id)}/execution_metadata"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        metrics = self._get(endpoint).json()
        return self._get_task_metrics(metrics)

    def _get_task_metadata(self, task_info: dict):
        return task_info.get("metadata", None)

    def get_task_metadata(self, task_id, qpu_id: str = None):
        """
        The results from this endpoint are the compilation metadata passed through at
        the time of task submission, not additional metadata about the task
        itself. See the metrics for that.
        """
        endpoint = f"/tasks/{str(task_id)}/metadata"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        metadata = self._get(endpoint).json()
        return self._get_task_metadata(metadata)

    def get_task_timings(self, task_id, qpu_id: str = None):
        endpoint = f"/tasks/{str(task_id)}/timings"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        metadata = self._get(endpoint).json()
        return metadata.get("timings", None)

    def get_task_execution_estimates(self, task_ids: Union[uuid4, list[uuid4]],
                                     qpu_id: str = None):
        if not isinstance(task_ids, list):
            task_ids = [task_ids]
        endpoint = "/monitoring/task_wait_time"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint
        return self._post(
            endpoint,
            json={
                "task_ids": [str(id) for id in task_ids]
            },
        ).json()

    def get_qpu_execution_estimates(self, qpu_ids: Union[str, list[str]] = None):
        if qpu_ids is None:
            qpu_ids = self.default_qpu_id
        if not isinstance(qpu_ids, list):
            qpu_ids = [qpu_ids]

        if self.server_version >= 3:
            # split the list of qpus by server
            split_qpus = defaultdict(list)

            for qpu_id in qpu_ids:
                try:
                    if qpu_id=="lucy":
                        qpu_id=self.default_qpu_id
                    qpu_url = self._get_qpu_endpoint(qpu_id)
                    split_qpus[qpu_url].append(qpu_id)
                except ValueError:
                    pass

            response = {"qpu_wait_times": []}
            for server, qpu_list in split_qpus.items():
                json_message = {"targets": [str(id) for id in qpu_list]}
                resp1 = self._post(
                    server + "/monitoring/qpu_wait_time",
                    json=json_message,
                ).json()
                for wait_time in resp1["qpu_wait_times"]:
                    response["qpu_wait_times"].append(wait_time)

            return response
        else:
            return self._post(
                "/monitoring/qpu_wait_time",
                json={
                    "targets": [str(id) for id in qpu_ids]
                },
            ).json()

    def cancel_task(self, task_ids: Union[uuid4, list[uuid4]], qpu_id: str = None):
        if not isinstance(task_ids, list):
            task_ids = [task_ids]

        endpoint = "/tasks/cancel_many"
        if self.server_version >= 3:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = server + endpoint

        return self._post(endpoint, json={"tasks": [str(id) for id in task_ids]})

    def create_user(self, name, email, password=None, validate=True):
        if self.server_version >= 3:
            name_parts = name.split(" ", 1)
            first_name = ""
            last_name = ""
            if len(name_parts) == 1:
                first_name = ""
                last_name = name_parts[0]
            elif len(name_parts) > 1:
                first_name = name_parts[0]
                last_name = name_parts[1]
            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "email": _validated_email(email) if validate else email,
                "password": "" if not password else password,
            }
        else:
            payload = {
                "name": _validated_name(name) if validate else name,
                "email": _validated_email(email) if validate else email,
            }
            if password is not None:
                payload["password"] = password
        return self._post("/admin/users", json=payload).json()


def _validate_datetime_format(time: str):
    try:
        datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        return time
    except ValueError as e:
        warnings.warn(f"Unable to convert {time} to a datetime, with exception {e}")
        return None


def _validated_email(email: str) -> str:
    pattern = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if not re.fullmatch(pattern, email):
        raise ValueError(f"{email} does not appear to be a valid email")
    return email


def _validated_url(url: str) -> str:
    if urlparse(url).scheme not in ["http", "https"]:
        raise ValueError(f"{url} does not appear to be a valid url")
    return url.rstrip("/")


def _validated_name(name: str) -> str:
    if len(name.strip()) < 1:
        raise ValueError(f"Invalid user name: {name}")
    return name


def _validated_password(password: str) -> str:
    if len(password.strip()) == 0:
        raise ValueError("provided an empty password field.")
    return password
