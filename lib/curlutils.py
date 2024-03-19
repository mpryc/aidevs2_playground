import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class HTTPMethod:
    GET = 'GET'
    POST = 'POST'


def send_request(url: str, method: HTTPMethod = HTTPMethod.GET, data:
                       Optional[Dict[str, Any]] = None) -> requests.Response:
    """
    Perform request to a given url.

    Args:
        url (str): URL of the endpoint.
        method (HTTPMethod, optional): Method, 'POST' or 'GET'.
        data (dict, optional): POST data, domyślnie None.

    Returns:
        requests.Response: Response from the server.
    """
    if method == HTTPMethod.GET:
        response = requests.get(url)
    elif method == HTTPMethod.POST:
        if data is None:
            raise ValueError("POST data must be provided when using POST method.")
        logger.info(f"URL: \n\t{url}\n")
        logger.debug(f"Data: \n\t{data}\n")
        response = requests.post(url, json=data)
    else:
        raise ValueError("Method not known. Use one of: 'GET' or 'POST'.")

    return response
