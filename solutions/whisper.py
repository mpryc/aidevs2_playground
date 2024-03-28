import logging
from lib.openaiutils import openai_get_authenticated_client, get_openai_models
from lib.curlutils import download_file_to_temp
import re
import os

logger = logging.getLogger(__name__)

def _extract_urls(text: str):
    url_regex = r'https?://\S+\.mp3(?=\s|$)'
    
    urls = re.findall(url_regex, text)
    
    return urls


def get_answer(task_details_response: dict):
    client = openai_get_authenticated_client()
    logger.info("Solving whisper task")

    mp3_urls = _extract_urls(task_details_response['msg'])

    models = get_openai_models()

    logger.info("Found url of the file: %s", mp3_urls[0])

    tmp_audio_file = download_file_to_temp(mp3_urls[0])
    logger.info("Downloaded file to: %s", tmp_audio_file)
    audio_file= open(tmp_audio_file, "rb")

    transcription = client.audio.transcriptions.create(
        model=models.whisper_1.name,
        file=audio_file
    )

    if os.path.exists(tmp_audio_file):
        os.remove(tmp_audio_file)
        logger.debug(f"Temporary file {tmp_audio_file} removed.")

    logger.debug(f"OpenAI Audio Transcription Response { transcription.text }")

    return transcription.text