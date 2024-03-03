# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_requests.ipynb.

# %% auto 0
__all__ = ['get_failed_response', 'make_api_request']

# %% ../nbs/04_requests.ipynb 4
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# %% ../nbs/04_requests.ipynb 5
def get_failed_response(
    error_message="Some kind of API error ccured while interacting with the given URL",
) -> requests.Response:
    failed_response = requests.Response()
    failed_response.status_code = 500
    failed_response.reason = error_message
    failed_response._content = orjson.dumps({"message": f"{error_message}"})
    return failed_response


async def make_api_request(
    url: str,
    http_method: str = "GET",
    headers: dict = {},
    data: dict = {},
    auth: tuple = (),
    cookies: dict = {},
    params: dict = {},
) -> requests.Response:
    """Makes an API request to the given url with the given parameters."""
    if not all(headers.values()):
        return get_failed_response()
    s = requests.Session()
    retries = Retry(
        total=10,
        backoff_factor=0.1,
        status_forcelist=[403, 406, 408, 413, 429, 500, 502, 503, 504],
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))

    try:
        req = requests.Request(
            http_method,
            url,
            data=data,
            headers=headers,
            auth=auth,
            cookies=cookies,
            params=params,
        )
        prepped = req.prepare()
        resp = s.send(prepped)
        return resp
    except Exception as e:
        get_logger().error("Connection error while fetching data {}".format(e))
        return get_failed_response()
