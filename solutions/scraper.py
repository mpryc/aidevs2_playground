import logging
import time

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate

from lib.openaiutils import get_openai_models
from lib.langchainutils import langchain_get_authenticated_client

logger = logging.getLogger(__name__)


def _load_documents_with_retry(loader, retry_count: int, error_indicator: str = "server error", min_art_length: int = 300, **kwargs):
    for _ in range(retry_count):
        try:
            docs = loader.load(**kwargs)
            for doc in docs:
                if error_indicator.lower() in doc.page_content.lower():
                    raise Exception("Error content detected in loaded documents")
                if len(doc.page_content.lower()) < min_art_length:
                    raise Exception("Error too short content detected")
            return docs
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            logger.info("Retrying...")
            time.sleep(1)
    return None


def get_answer(task_details_response: dict):
    logger.info("Solving scraper task using langchain")

    input_text_url = task_details_response['input']
    question_text = task_details_response['question']
    msg_text = task_details_response['msg']

    loader = WebBaseLoader(input_text_url, header_template={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',})
    loaded_docs = _load_documents_with_retry(loader, 3, "server error")
    if loaded_docs is None:
        logger.error("Failed to load documents after retries")
        return None

    models = get_openai_models()


    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>
    {context}
    </context>

    Question: {input}""")

    llm = langchain_get_authenticated_client(models.gpt_3_5_turbo.name)

    document_chain = create_stuff_documents_chain(llm, prompt)

    result = document_chain.invoke({
        "input": f"{question_text}. Rules: {msg_text}",
        "context": [loaded_docs[0]]
    })

    logger.debug(f"OpenAI Response { result }")

    return result
