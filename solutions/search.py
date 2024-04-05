import logging
import re
import uuid
from typing import Optional
from lib.openaiutils import openai_get_authenticated_client
from qdrant_client import QdrantClient
from qdrant_client.http.models import UpdateStatus
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse
import requests
from typing import Optional, List, Dict, Any
from qdrant_client.http.models import Distance, VectorParams
from openai import OpenAI
from qdrant_client.models import PointStruct

logger = logging.getLogger(__name__)

API_ENDPOINT = 'https://api.openai.com/v1/embeddings'

EMBEDDING_MODEL = "text-embedding-ada-002"
COLLECTION_NAME = "unknown_news"


def upsert_data(openai_client: OpenAI, qdrant_client: QdrantClient, texts: List[str]):
    points = []
    logger.info("Func upsert_data")
    title_txt = texts.get('title')
    info_txt = texts.get('info')
    url_txt = texts.get('url')
    date_txt = texts.get('date')

    logger.debug("Creating Embedding")
    text_vector = openai_client.embeddings.create(input=info_txt, model=EMBEDDING_MODEL)
    text_id = str(uuid.uuid4())
    payload = {"title": title_txt, "info": info_txt, "url": url_txt, 'date': date_txt}
    point = PointStruct(id=text_id, vector=text_vector.data[0].embedding, payload=payload)
    points.append(point)

    operation_info = qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points)

    if operation_info.status == UpdateStatus.COMPLETED:
        logger.info("Data inserted successfully!")
    else:
        logger.error("Failed to insert data")

def retrieve_json_data_from_url(url: str) -> Optional[List[Dict[str, Any]]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error retrieving JSON data from URL: {e}")
        return None

def _get_qdrant_client(host: str, port: int) -> Optional[QdrantClient]:
    qdrant_client = QdrantClient(host="localhost",port=6333)
    try:
        my_collection = "test_connection"

        qdrant_client.count(
            collection_name=my_collection, 
            exact=True,
        )
        logger.info(f"Connected to Qdrant: { host }:{port}")
        return qdrant_client
    except ResponseHandlingException:
        logger.error(f"Can't connect to Qdrant: { host }:{port}")
        logger.info("""
                    
                    Are you sure you are running Qdrant locally?\n
                    You may use ./scripts/run_quadrant.sh to start it
                    on the system with docker or podman and bash
                    
                    """)
        return None
    except UnexpectedResponse:
        logger.debug(f"We've connected to Qdrant: { host }:{port}")
        return qdrant_client

def _extract_urls(text: str):
    url_regex = r'https?://\S+\.json(?=\s|$)'
    
    urls = re.findall(url_regex, text)
    
    if len(urls) > 0:
        return urls[0]
    return None

def insert_json_data_to_qdrant(json_data: List[Dict[str, Any]], openai_client: OpenAI, qdrant_client: QdrantClient, size: int = 1536) -> bool:
    try:
        qdrant_collection_name = "unknown_news"
        qdrant_client.recreate_collection(
            collection_name=qdrant_collection_name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

        for item in json_data:
            upsert_data(openai_client, qdrant_client, item)

        logger.info("JSON data inserted into Qdrant successfully!")
        return True
    except Exception as e:
        logger.error(f"Error inserting JSON data into Qdrant: {e}")
        return False

def search_using_qdrant(openai_client: OpenAI, qdrant_client: QdrantClient, search_query: str, limit: int = 1) -> Optional[str]:

    texts = {}
    texts['info'] = search_query

    query_vector = openai_client.embeddings.create(input=search_query, model=EMBEDDING_MODEL)
    search_embedding = query_vector.data[0].embedding

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=search_embedding,
        limit=limit,
    )
    

    # Return first as it's limit 1
    for item in search_result:
        payload = item.payload
        return payload.get('url')

    return None

def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving QDrant task")
    question_text = task_details_response['question']
    json_url = _extract_urls(task_details_response['msg'])

    qdrant_client = _get_qdrant_client(host="localhost",port=6333)
    if not qdrant_client:
        return None

    json_data = retrieve_json_data_from_url(json_url)
    if json_data is not None:
        if not insert_json_data_to_qdrant(json_data, client, qdrant_client):
            return None
    result = search_using_qdrant(client, qdrant_client, question_text)
    
    logger.info(f"Question { question_text }")
    logger.info(f"QDrant R { result }")

    return result
