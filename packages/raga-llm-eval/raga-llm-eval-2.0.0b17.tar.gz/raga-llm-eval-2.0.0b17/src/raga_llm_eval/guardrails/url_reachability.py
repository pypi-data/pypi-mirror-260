from typing import List
from urllib import request, error

import requests
from .utils import extract_urls


class URLReachability:
    """
    This scanner checks URLs for their reachability.
    """

    def __init__(
        self,
        question,
        response,
        success_status_codes: List[int] = None,
        threshold: int = 5,
    ):
        """
        Initialize the test instance with the provided parameters.

        Args:
        - question: str, the question to be evaluated for contextual relevancy
        - response: str, the response for the question
        - success_status_codes: A list of status codes that are considered as successful.
        - threshold: int, The timeout in seconds for the HTTP requests (default 5)
        """
        self.question = question
        self.output = response

        if success_status_codes is None:
            success_status_codes = (200, 201, 202, 301, 302)

        self._success_status_codes = success_status_codes
        self._timeout = threshold

    def is_reachable(self, url: str) -> bool:
        """
        Check if the URL is reachable.
        """

        print(f"URL: {url}")

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        try:
            # print(url)
            connection = request.urlopen(url, timeout=self._timeout)
            status_code = connection.getcode()
            connection.close()
            return status_code in self._success_status_codes
        except error.URLError:
            return False

    def run(self):

        # import pdb

        # pdb.set_trace()

        urls = extract_urls(self.output)
        score = 1.0

        if not urls:
            score = 1.0

        unreachable_urls = [url for url in urls if not self.is_reachable(url)]

        if unreachable_urls:
            score = 0.0

        result = {
            "prompt": self.question,
            "response": self.output,
            "score": score,
            "threshold": self._timeout,
            "is_passed": "Passed" if score else "Failed",
        }

        return result
