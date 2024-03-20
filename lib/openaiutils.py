from openai import OpenAI
import logging
from typing import Optional
import json

from lib.variables import get_environment_variable, AIDEVS_OPENAI_API_KEY

logger = logging.getLogger(__name__)

OPENAI_MODELS_FILE = 'openaimodels/modellist.json'

def openai_get_authenticated_client() -> Optional[OpenAI]:
    openai_api_key = get_environment_variable(AIDEVS_OPENAI_API_KEY)
    if not openai_api_key:
        logger.error("Please set the AIDEVS_API_KEY environment variable")
        return None
    else:
        logger.debug(f"Got OpenAI API Key: {openai_api_key}")
    return OpenAI(
        api_key=openai_api_key,
    )

class OpenAIModels:
    def __init__(self, models):
        for model in models:
            setattr(self, model.name.replace('-', '_').replace('.', "_"), model)
        self._models = models

    def __iter__(self):
        return iter(self._models)

class OpenAIModel:
    def __init__(self, name, description, context_window, training_data, category):
        self.name = name
        self.description = description
        self.context_window = context_window
        self.training_data = training_data
        self.category = category

def get_openai_models():
    with open(OPENAI_MODELS_FILE, 'r') as f:
        data = json.load(f)

        models_data = data.get('models', [])

    models = []
    for model_data in models_data:
        model = OpenAIModel(
            name=model_data.get('name'),
            description=model_data.get('description'),
            context_window=model_data.get('context_window'),
            training_data=model_data.get('training_data'),
            category=model_data.get('category')
        )
        models.append(model)

    return OpenAIModels(models)