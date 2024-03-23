import logging
import json
from lib.openaiutils import openai_get_authenticated_client, get_openai_models

logger = logging.getLogger(__name__)

_CHAT_MSGS=[
    {
        "role": "system",
        "content": '''Jesteś bloggerem, który prowadzi blog kulinarny. Na podstawie tematów podanych w outlinie napisz rozdziały będące częścią przepisu na pizzę w języku polskim. Rozdziały powinny zostać zapisanne lekkim językiem nadającym się do publikacji w internecie. Outlin zostanie dostarczon jako tablica stringów. Rozwiń kazdy z dozdziałów do długości około 5 do 10 zdań

Odpowiedz powinna zostać zwrocona w fromacie JSON jako tablica stringów zawierającej kolejne rozdziały. Długość tablicy z rozdziałami powinna być identyczna z długością outlinu. Nie dodawaj tytułów do tej tablicy, jedynie napisane rozdziały. 
'''
    }
]


# [{'role': 'system', 'content': "Jesteś bloggerem, który prowadzi blog kulinarny. Pomóz przygotować przepis na pizzę w języku polskim według podanego outlinu, która zostanie dostarczona jako tablica stringów.\n\nOdpowiedz powinna zostać zwrocona w postaci tablicy stringów zawierającej kolejne rozdziały. Długość tablicy z rozdziałami powinna być identyczna z długością outlinu.\n\n\n### Examples\nOutline moe wyglądać tak: ['Wstęp: kilka słów na temat historii pizzy', 'Niezbędne składniki na pizzę', 'Robienie pizzy', 'Pieczenie pizzy w piekarniku']\n\nOdpowiedz powinna wyglądać w formacie: ['Tu wpisz rozdzial 1', 'Tu wpisz rozdzial 2', 'Tu wpisz rozdzial 3', 'Tu wpisz rozdzial 4']\n"}, 
# {'role': 'user', 'content': ['Wstęp: kilka słów na temat historii pizzy', 'Niezbędne składniki na pizzę', 'Robienie pizzy', 'Pieczenie pizzy w piekarniku']}]

def get_answer(task_details_response: dict):
    logger.info("Solving lesson 4 task blogger")

    client = openai_get_authenticated_client()
    models = get_openai_models()

    logger.debug(task_details_response['blog'])

    user_json_data = {
        "role": "user",
        "content": str(task_details_response['blog'])
    }

    _CHAT_MSGS.append(user_json_data)

    print(_CHAT_MSGS)

 
    task_response = client.chat.completions.create(
        model=models.gpt_3_5_turbo.name,
        messages=_CHAT_MSGS,
        temperature=1,
        max_tokens=2000,
        top_p=1
    )

    logger.debug(f"OpenAI Response { task_response }")

    print(task_response.choices[0].message.content)
    return json.loads(task_response.choices[0].message.content)
