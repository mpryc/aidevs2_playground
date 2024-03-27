import logging
import json
from lib.curlutils import send_request, HTTPMethod
from lib.variables import get_environment_variable, AIDEVS_OPENAI_API_KEY

logger = logging.getLogger(__name__)

MODERATION_MODEL = 'text-moderation-latest'

# https://platform.openai.com/docs/api-reference/embeddings
API_ENDPOINT = 'https://api.openai.com/v1/embeddings'


def _string_to_embeddings_input(input_string):
    json_data = {
        "input": input_string,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }
    return json_data

def _get_embeddings(input_json):
    openai_api_key = get_environment_variable(AIDEVS_OPENAI_API_KEY)
    output_http = send_request(API_ENDPOINT, HTTPMethod.POST, input_json, openai_api_key)
    return output_http

def get_answer(task_details_response: dict):
    logger.info(f"Solving embedding task for input: {dict}")

    embedding_text = task_details_response['msg'].split(': ')[1]
    input_json = _string_to_embeddings_input(embedding_text)
    valid = _get_embeddings(input_json)
    return json.loads(valid.text)['data'][0]['embedding']

