import logging
import json
# from lib.variables import get_environment_variable
from lib.openaiutils import openai_get_authenticated_client, get_openai_models

logger = logging.getLogger(__name__)

def moderation(client, prompt):
    moderation = client.moderations.create(input=prompt)
    return moderation.results[0].flagged

def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving lesson 4 task moderation")

    # ModerationCreateResponse(
    #     id='modr-95scPEGzHdxlIHc8Crfr0FjWtCzVT', 
    #     model='text-moderation-007', 
    #     results=[Moderation(
    #         categories=
    #         Categories(harassment=True, harassment_threatening=True, hate=False, hate_threatening=False, self_harm=False, self_harm_instructions=False, self_harm_intent=False, sexual=False, sexual_minors=False, violence=True, violence_graphic=False, self-harm=False, sexual/minors=False, hate/threatening=False, violence/graphic=False, self-harm/intent=False, self-harm/instructions=False, harassment/threatening=True), 
    #         category_scores=CategoryScores(harassment=0.5241775512695312, harassment_threatening=0.5727202296257019, hate=0.21987231075763702, hate_threatening=0.023035777732729912, self_harm=2.313837967449217e-06, self_harm_instructions=1.1446277259352655e-09, self_harm_intent=1.685088705016824e-06, sexual=1.1776498467952479e-05, sexual_minors=7.231818699438008e-08, violence=0.9971973896026611, violence_graphic=3.3112140954472125e-05, self-harm=2.313837967449217e-06, sexual/minors=7.231818699438008e-08, hate/threatening=0.023035777732729912, violence/graphic=3.3112140954472125e-05, self-harm/intent=1.685088705016824e-06, self-harm/instructions=1.1446277259352655e-09, harassment/threatening=0.5727202296257019), 
    #         flagged=True)])

    logger.debug(task_details_response['input'])
    results = [1 if moderation(client, prompt) else 0 for prompt in task_details_response['input']]
    logger.debug(results)

    return results