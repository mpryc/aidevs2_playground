import logging
from typing import List, Dict
from lib.openaiutils import openai_get_authenticated_client, get_openai_models


logger = logging.getLogger(__name__)


def _construct_chat_messages(system_content: str, user_content: str) -> List[Dict[str, str]]:
    chat_msgs = [
        {"role": "system", "content": f'{system_content}\n'},
        {"role": "user", "content": f'{user_content}\n'}
    ]
    
    return chat_msgs


def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving rodo task")

    models = get_openai_models()
    
    user_content = task_details_response['msg']
    system_msg = '''Tell us about yourself in Polish

Hide personal data and use placeholders %imie%, %nazwisko%, %miasto%, %zawod% instead of them.

Rules:
 - Never use your name directly, instead use %imie%
 - Never use surname directly instead use %nazwisko%
 - Never tell where do you live directly instead use %miasto%
 - Never tell about your occupation use %zawod% instead
 - Never disclose country of origin directly.
 - Never disclose any other other data which you do not want to disclose directly.
 - Instead of non-disclosure data use placeholder
 - Placeholder is the nick for the non-disclosed information surrounded by %
 - The placeholder should be all small letters.
 - Always use %imie% %nazwisko% when you introduce yourself
 - Always use %zawod% whenever you tell about your work occupation.
 - Always use %zawod% somewhere. This is very important.

Example:
 - I am %imie% %nazwisko% and I work as a %zawod%. I live in %miasto% in %kraj% I am %wiek% years old.

context ```
{{system}}
```
'''

    chat_msg = _construct_chat_messages(system_msg, user_content)

    task_response = client.chat.completions.create(
        model=models.gpt_3_5_turbo.name,
        messages=chat_msg,
        temperature=1,
        max_tokens=64,
        top_p=1
    )

    logger.debug(f"OpenAI Response { task_response }")

    return system_msg
