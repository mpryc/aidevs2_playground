from typing import Optional, Dict, Any
import logging
import importlib.util
import sys
from urllib.parse import urljoin
from lib.curlutils import send_request, HTTPMethod
from lib.variables import set_aidevsenvironment_variable, get_aidevsenvironment_variable, \
                          get_environment_variable, AIDEVS_AUTH_TOKEN, AIDEVS_TASK_NAME, AIDEVS_API_KEY

logger = logging.getLogger(__name__)

AIDEVS_PREFIX = 'https://tasks.aidevs.pl/'
URL_TOKEN_PREFIX = urljoin(AIDEVS_PREFIX, 'token/')
URL_TASK_PREFIX = urljoin(AIDEVS_PREFIX, 'task/')
URL_ANSWER_PREFIX = urljoin(AIDEVS_PREFIX, 'answer/')
URL_HINT_PREFIX = urljoin(AIDEVS_PREFIX, 'hint/')


def register_task_token(task_name: str) -> bool:
    # Check if AIDEVS_API_KEY is set in the environment
    aidevs_api_key_env = get_environment_variable(AIDEVS_API_KEY)
    if not aidevs_api_key_env:
        logger.error("Please set the AIDEVS_API_KEY environment variable")
        return False
    
    api_key_json = {"apikey": aidevs_api_key_env}

    # Construct URL for token registration
    url_token = URL_TOKEN_PREFIX + task_name

    try:
        # Send request to register token
        response = send_request(url_token, method=HTTPMethod.POST, data=api_key_json)
        response_data = response.json()

        # Check response for success or failure
        if response_data.get('code') == 0:
            task_auth_token = response_data.get('token')
            logger.debug(f"Token registration successful: {task_auth_token}")
            # Set the authentication token in environment variables
            set_aidevsenvironment_variable(AIDEVS_AUTH_TOKEN, task_auth_token)
            set_aidevsenvironment_variable(AIDEVS_TASK_NAME, task_name)
            return True
        else:
            logger.error(f"Token registration failed: {response_data.get('msg')}")
            return False

    except Exception as e:
        logger.error(f"Error occurred during token registration: {e}")
        return False


def get_task_hint(task_name: str) -> Optional[Dict[str, Any]]:
    hint_url = URL_HINT_PREFIX + task_name
    try:
        response = send_request(hint_url, method=HTTPMethod.GET)
        response_data = response.json()
        if 'code' in response_data and response_data['code'] != 0:
            logger.error(f"Error occurred while fetching task hint: {response_data}")
            return None
        return response_data
    except Exception as e:
        logger.error(f"Error occurred while fetching task hint: {e}")
        return None


def get_task_details() -> Optional[Dict[str, Any]]:
    # Retrieve AIDEVS authentication token from previously registered auth
    aidevs_auth_token = get_aidevsenvironment_variable(AIDEVS_AUTH_TOKEN)
    if not aidevs_auth_token:
        logger.error("AIDEVS authentication token not found. Please ensure it is set.")
        return None
    
    # Construct URL for fetching task details
    task_url = urljoin(URL_TASK_PREFIX, aidevs_auth_token)

    logger.debug(f"Task URL: {task_url}")

    try:
        response = send_request(task_url, method=HTTPMethod.GET)
        response_data = response.json()
        if response_data['code'] == 0:
            logger.info(f"Success response: \n\t{response_data}\n")        
            return response_data
        else:
            logger.error(f"Error response: {response_data}")
            return None
    except ValueError as e:
        logger.error(f"Error: {e}")
        return None


def send_answer(answer_str: str) -> Optional[Dict[str, Any]]:
    # Prepare JSON payload for the answer
    answer_json = {"answer": answer_str}

    try:
        aidevs_auth_token = get_aidevsenvironment_variable(AIDEVS_AUTH_TOKEN)
        if not aidevs_auth_token:
            logger.error("AIDEVS authentication token not found. Please ensure it is set.")
            return None        
        answer_token_url = urljoin(URL_ANSWER_PREFIX, aidevs_auth_token)
        # Send request to submit the answer
        response = send_request(answer_token_url, method=HTTPMethod.POST, data=answer_json)
        response_data = response.json()

        # Check response for success or failure
        if response_data.get('code') == 0:
            logger.info("Answer submitted successfully")
            return response_data
        else:
            logger.error(f"Error submitting answer: {response_data}")
            return None

    except Exception as e:
        logger.error(f"Error occurred while submitting answer: {e}")
        return None



def load_task_module(task_name: str):
    try:
        # Construct the module name based on task_name
        module_name = f"solutions.{task_name}"

        # Import the module dynamically
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            logger.error(f"Module {module_name} not found")
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Check if the module has the required function get_answer
        if not hasattr(module, 'get_answer'):
            logger.error(f"Module {module_name} does not contain 'get_answer' function")
            return None

        return module
    except Exception as e:
        logger.error(f"Error loading task module for {task_name}: {e}")
        return None
