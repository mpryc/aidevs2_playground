import logging
from lib.variables import get_environment_variable
from lib.openaiutils import openai_get_authenticated_client, get_openai_models


logger = logging.getLogger(__name__)

_CHAT_MSGS=[
    {
        "role": "system",
        "content": '''You are a system that categorizes tasks.

Categorize the given task into one of the categories from context.

Give an output in a json file that has well defined structure: { "category": "<category>"}

## context
- categories: 
- dom (home)
- praca (work)
- inne (other)

# examples:
- zrobić coś dla szefa (do something for the boss): { "category": "praca" (work)}
- posprzątac w pokoju (clean up the room): {"category": "dom" (home)}
- pojeździć na rowerze (go cycling): {"category": "inne" (other)}'''
    },
    {
        "role": "user",
        "content": "przygotować dla szefa raport sprzedaży za marzec (prepare a sales report for March for the boss)"
    }
]


def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving lesson 3 task 2")

    models = get_openai_models()
 
    task_response = client.chat.completions.create(
        model=models.gpt_3_5_turbo.name,
        messages=_CHAT_MSGS,
        temperature=1,
        max_tokens=64,
        top_p=1
    )

    logger.debug(f"OpenAI Response { task_response }")

    return task_response
