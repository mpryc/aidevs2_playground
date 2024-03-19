import logging
import os
import json
from typing import Dict, Any, Optional

AIDEVS_API_KEY = 'AIDEVS_API_KEY'
AIDEVS_AUTH_TOKEN = 'AIDEVS_AUTH_TOKEN'
AIDEVS_TASK_NAME = 'AIDEVS_TASK_NAME'

ENVIRONMENT_FILE = ".aidevsenv.json"

logger = logging.getLogger(__name__)

def _load_environment() -> Dict[str, Any]:
    if os.path.exists(ENVIRONMENT_FILE):
        with open(ENVIRONMENT_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def _save_environment(environment: Dict[str, Any]) -> None:
    with open(ENVIRONMENT_FILE, "w") as file:
        json.dump(environment, file, indent=4)

def get_environment_variable(key: str) -> Optional[str]:
    value: Optional[str] = os.environ.get(key)
    if value:
        logger.debug(f"Retrieved environment variable: {key}={value}")
    else:
        logger.warn(f"No value found for environment variable: {key}")
    return value

def get_aidevsenvironment_variable(key: str) -> Optional[Any]:
    environment: Dict[str, Any] = _load_environment()
    value: Optional[Any] = environment.get(key)
    if value:
        logger.debug(f"Retrieved AIDevs environment variable: {key}={value}")
    else:
        logger.warning(f"No value found for AIDevs environment variable: {key}")
    return value

def set_aidevsenvironment_variable(key, value):
    environment = _load_environment()
    environment[key] = value
    _save_environment(environment)
    logger.debug(f"Set environment variable: {key}={value}")
