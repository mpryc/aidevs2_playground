#!/bin/env python

import argparse
import logging
from lib.aidevutils import send_answer, get_task_details, register_task_token, get_task_hint, load_task_module
from lib.variables import get_aidevsenvironment_variable, AIDEVS_TASK_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# First we retrieve the auth_token from a given env variable AIDEVS_API_KEY
# We used that key to get the token for the task
# The token get's stored in a local store, so we don't need to request auth
# token multiple times (It's valid for 180s). Secondly we want to store the
# token to allow answer for the task that may be using external tooling for
# data processing 
def main():

    task_name = None
    answer = None

    parser = argparse.ArgumentParser(description="Send HTTP request and display response.")
    parser.add_argument("-q", "--question", action="store", dest="question", help="Task Name")
    parser.add_argument("-s", "--sent-answer", action="store_true", dest="sentanswer", help="Sent answer based on provided solution in python")
    parser.add_argument("-a", "--answer", action="store", dest="answer", help="Answer to a previous task")
    parser.add_argument("-x", "--hint", action="store_true", dest="hint", help="Include hints")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug", help="Include hints")


    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Logging level set to DEBUG")

    if args.question:
        task_name = args.question
        if args.hint:
            logger.info(f"Requested Hint for the task {task_name}")
            response = get_task_hint(task_name)
            if not response:
                logger.error("Failed to retrieve hint")
            else:
                logger.info(f"GOT hint: {response}")

            return None
    elif args.hint:
        logger.error("Hint should be used together with question")
        return None

    if task_name:
        register_task_token(task_name)
        task_details_response = get_task_details()
        if not task_details_response:
            logger.error("Failed to retrieve task")
            return None
        else:
            logger.debug(f"Task: {task_details_response}")
    
    if args.answer:
        answer = args.answer
    elif args.sentanswer:
        if not task_name:
            task_name = get_aidevsenvironment_variable(AIDEVS_TASK_NAME)
            logging.info(f"Got task name: {task_name}")
            # TODO: Ugly, but let's improve later as we don't know what
            #       task details we expect in the future, currently
            #       we re-use auth token, but get the new task details
            task_details_response = get_task_details()
            if not task_details_response:
                logger.error("Failed to retrieve task")
                return None
            else:
                logger.debug(f"Task: {task_details_response}")
           
        if task_name:
            task_module = load_task_module(task_name)
            if task_module is not None:
                answer = task_module.get_answer(task_details_response)
                if not answer:
                    logger.error("Answer not automatically provided - NOT SUBMITTED !!!")
            else:
                logger.error("Could not find file for the task with proper answer function")
        else:
            logger.error("Can not answer, not known task name")
            return None

    if answer:
        logger.info(f"Answer SUBMITTED: {answer}")
        response_from_answer = send_answer(answer)
        logger.info(f"Response: {response_from_answer}")

if __name__ == "__main__":
    main()
