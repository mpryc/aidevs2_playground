import logging

logger = logging.getLogger(__name__)

def get_answer(task_details_response: dict):
    logger.info("We will solve some 1st World problem !")

    if 'cookie' in task_details_response:
        return task_details_response['cookie']
    return None