import os

from dotenv import load_dotenv
from qcaas_common.logger import get_logger

log = get_logger(__name__)


def load_env_file_if_exists(env_file: str = ".env"):
    # Load env file if it exists, env_file name/path relational from the qcaas package
    # root folder.
    if os.path.isabs(env_file):
        env_path = env_file
    else:
        env_path = os.path.join(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
            ),
            env_file,
        )
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)
        log.info(f"Loaded env file from '{env_path}'.")
    else:
        log.info(f"Couldn't find env file at '{env_path}'. Not loading")
