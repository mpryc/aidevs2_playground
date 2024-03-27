import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class HTTPMethod:
    GET = 'GET'
    POST = 'POST'


def send_request(url: str, method: HTTPMethod = HTTPMethod.GET, data: Optional[Dict[str, Any]] = None,
                 auth_token: Optional[str] = None) -> requests.Response:
    """
    Perform request to a given url.

    Args:
        url (str): URL of the endpoint.
        method (HTTPMethod, optional): Method, 'POST' or 'GET'.
        data (dict, optional): POST data, default is None.
        auth_token (str, optional): Bearer authentication token.

    Returns:
        requests.Response: Response from the server.
    """
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    if method == HTTPMethod.GET:
        response = requests.get(url, headers=headers)
    elif method == HTTPMethod.POST:
        if data is None:
            raise ValueError("POST data must be provided when using POST method.")
        logger.info(f"URL: \n\t{url}\n")
        logger.debug(f"Data: \n\t{data}\n")
        response = requests.post(url, json=data, headers=headers)
    else:
        raise ValueError("Method not known. Use one of: 'GET' or 'POST'.")

    return response
