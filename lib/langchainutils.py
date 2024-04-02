import logging
from typing import Optional
from langchain_openai import ChatOpenAI

from lib.variables import get_environment_variable, AIDEVS_OPENAI_API_KEY

logger = logging.getLogger(__name__)

def langchain_get_authenticated_client(openai_model: str) -> Optional[ChatOpenAI]:
    openai_api_key = get_environment_variable(AIDEVS_OPENAI_API_KEY)
    if not openai_api_key:
        logger.error("LangChain: Please set the AIDEVS_API_KEY environment variable")
        return None
    else:
        logger.debug("LangChain: Got OpenAI API Key: %s", openai_api_key)
    return ChatOpenAI(model=openai_model, openai_api_key=openai_api_key)
