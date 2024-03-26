import logging
from lib.variables import get_environment_variable
from lib.openaiutils import openai_get_authenticated_client, get_openai_models


logger = logging.getLogger(__name__)

_CHAT_MSGS_1=[
    {
        "role": "system",
        "content": '''You will get question which contain name of some person. Return me only name of this person as response and nothing else. 

### Examples
Q: jakie hobby ma Zenon?

A: Zenon
'''
    }
]

_CHAT_MSGS_2=[]

_CHAT_MSGS_2_SYSTEM = {
        "role": "system",
        "content": '''You have knowledge about people. Based on this knowledge respond shortly to asked question. Respond only with your provided knowledge in context and nothing else. 

Context```
KNOWLEDGE
'''
    }
_CHAT_MSGS_2_USER = {
        "role": "user",
        "content": "QUESTION"
    }


def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving lesson 7 task 1")
    print(task_details_response['question'])

    user_json_data = {
        "role": "user",
        "content": str(task_details_response['question'])
    }

    _CHAT_MSGS_1.append(user_json_data)

    models = get_openai_models()
 
    # get name from question
    task_response = client.chat.completions.create(
        model=models.gpt_3_5_turbo.name,
        messages=_CHAT_MSGS_1,
        temperature=1,
        max_tokens=64,
        top_p=1
    )

    logger.debug(f"OpenAI Response { task_response }")

    name = task_response.choices[0].message.content

    # filer sentences with name which we got
    filtered_sentences = [sentence for sentence in task_details_response['input'] if name in sentence]

    # build promt with filtered context
    _CHAT_MSGS_2_SYSTEM['content'] = _CHAT_MSGS_2_SYSTEM['content'].replace('KNOWLEDGE', str(filtered_sentences))
    _CHAT_MSGS_2_USER['content'] = _CHAT_MSGS_2_USER['content'].replace('QUESTION', str(task_details_response['question']))
    _CHAT_MSGS_2.append(_CHAT_MSGS_2_SYSTEM)
    _CHAT_MSGS_2.append(_CHAT_MSGS_2_USER)

    # Ask for response for original question
    task_response = client.chat.completions.create(
        model=models.gpt_3_5_turbo.name,
        messages=_CHAT_MSGS_2,
        temperature=1,
        max_tokens=200,
        top_p=1
    )

    logger.debug(f"OpenAI Response { task_response }")

    return task_response.choices[0].message.content