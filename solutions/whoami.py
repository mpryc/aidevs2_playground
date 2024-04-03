import logging

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate

from lib.aidevutils import register_task_token, get_task_details
from lib.openaiutils import get_openai_models
from lib.langchainutils import langchain_get_authenticated_client
from langchain.schema.document import Document
from langchain.text_splitter import TokenTextSplitter
from typing import Any, List

logger = logging.getLogger(__name__)


def get_text_chunks_langchain(text: str):
    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs

def get_another_information():
    register_task_token('whoami')
    task_details_response = get_task_details()
    if not task_details_response:
        logger.error("Failed to retrieve task")
        return None
    else:
        logger.debug(f"Task: {task_details_response}")
        return task_details_response

def get_llm_answer(llm: Any, documents: List):
    question_text = "Guess who the person is."
    rules_text = """
     - Response DUNNO if you are not 99% sure about the name and surname.
     - Give the name and surname as response.
     - Remove any dots from the response
     - Double check it's just the name and surname, nothing else
     - Make sure the person is correctly identified
     - If you have even a small doubts about the person or more then one person matches, response DUNNO
    """

    prompt = ChatPromptTemplate.from_template("""Tell the name of the person,
        but only if you are certain about this person:
    <context>
    {context}
    </context>

    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)

    result = document_chain.invoke({
        "input": f"{question_text}. Rules: {rules_text}",
        "context": documents
    })
    return result


def get_answer(task_details_response: dict):
    logger.info("Solving whoami task using langchain")
    documents = []
    about_person = task_details_response['hint']
    docs = get_text_chunks_langchain(about_person)
    documents.extend(docs)


    models = get_openai_models()
    llm = langchain_get_authenticated_client(models.gpt_3_5_turbo.name)


    result = get_llm_answer(llm, documents)

    if "DUNNO" not in result:
        return result


    i = 0

    while i < 10:
        i += 1
        task_details_response = get_another_information()
        if not task_details_response:
            continue
        about_person = task_details_response['hint']
        docs = get_text_chunks_langchain(about_person)
        documents.extend(docs)
        result = get_llm_answer(llm, documents)
        if "DUNNO" not in result:
            return result
    return None