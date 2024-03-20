import logging
from lib.variables import get_environment_variable
from lib.openaiutils import openai_get_authenticated_client, get_openai_models


logger = logging.getLogger(__name__)

_CHAT_MSGS=[
    {
        "role": "system",
        "content": '''You will be provided with data about the books, their authors and years of publishing. 

Answer should be a combined single JSON with two fields 'title' and 'author' for each given book. Do not include other JSON elements.

The response should be in a JSON format without newlines and spaces between JSON elements.

### Examples
- Romeo i Julia
- [{'title':'Romeo i Julia','author':'William Shakespeare'}]

- Another Book
- Rok 1957
-  [{'title':'Another Book,'author':'Other Author'},{'title':'Sample Book published in 1957','author':'Author of Another Book'}]
'''
    },
    {
        "role": "user",
        "content": '''Romeo i Julia
Cień wiatru
Rok 1984
'''
    }
]


def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving lesson 3 task 1")

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
