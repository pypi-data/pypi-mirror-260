import requests as requests_lib
from requests.adapters import HTTPAdapter, Retry

from chaiverse.config import BASE_SUBMITTER_URL, BASE_FEEDBACK_URL
from chaiverse.utils import get_url
from chaiverse.cli_utils.login_cli import get_developer_key_from_cache


# Increased retry from 3 to 6 only if initial connect failed, and it will not cause any side effects.
# This requests is intended to be directly imported to replace the requests library
requests = requests_lib.Session()
retries = Retry(connect=6, backoff_factor=1)
requests.mount('http://', HTTPAdapter(max_retries=retries))
requests.mount('https://', HTTPAdapter(max_retries=retries))


class _ChaiverseHTTPClient():
    def __init__(self, developer_key=None, hostname=None, debug_mode=False):
        if developer_key is None:
            developer_key = get_developer_key_from_cache()
        self.developer_key = developer_key
        self.hostname = hostname
        self.debug_mode = debug_mode

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.developer_key}"}

    def get(self, endpoint, submission_id=None, **kwargs):
        url = get_url(endpoint, hostname=self.hostname, submission_id=submission_id)
        response = self._request(requests.get, url=url, **kwargs)
        return response

    def put(self, endpoint, data):
        url = get_url(endpoint, hostname=self.hostname)
        response = self._request(requests.put, url=url, json=data)
        return response

    def post(self, endpoint, data=None, submission_id=None, **kwargs):
        url = get_url(endpoint, hostname=self.hostname, submission_id=submission_id)
        response = self._request(requests.post, url=url, json=data, **kwargs)
        return response

    def delete(self, endpoint):
        url = get_url(endpoint, hostname=self.hostname)
        response = self._request(requests.delete, url=url)
        return response

    def _request(self, func, url, **kwargs):
        response = func(url=url, headers=self.headers, **kwargs)
        if not self.debug_mode:
            assert response.status_code == 200, response.json()
            response = response.json()
        return response


class SubmitterClient(_ChaiverseHTTPClient):
    def __init__(self,
            developer_key=None,
            hostname=None,
            debug_mode=False):
        hostname = BASE_SUBMITTER_URL if not hostname else hostname
        super().__init__(developer_key, hostname, debug_mode)


class FeedbackClient(_ChaiverseHTTPClient):
    def __init__(self,
            developer_key=None,
            hostname=None,
            debug_mode=False):
        hostname = BASE_FEEDBACK_URL if not hostname else hostname
        super().__init__(developer_key, hostname, debug_mode)
