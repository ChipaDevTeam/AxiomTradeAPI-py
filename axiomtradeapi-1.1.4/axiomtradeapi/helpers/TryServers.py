import requests
from axiomtradeapi.urls import AAllBaseUrls


def try_servers(path: str, timeout: float = 3.0):
    """
    Tries all base URLs with the provided path. Returns the first server that responds with HTTP 200.
    Args:
        path (str): The path to append to each base URL (should start with '/').
        timeout (float): Timeout for each request in seconds.
    Returns:
        tuple: (base_url, response) if successful, else (None, None)
    """
    base_urls = [
        getattr(AAllBaseUrls, attr)
        for attr in dir(AAllBaseUrls)
        if attr.startswith("BASE_URL")
    ]
    for base_url in base_urls:
        url = base_url + path
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                return base_url, resp
        except Exception:
            continue
    return None, None
