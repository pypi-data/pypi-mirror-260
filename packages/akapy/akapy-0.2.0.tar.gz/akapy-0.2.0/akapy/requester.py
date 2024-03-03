import requests
import shutil
from pprint import pprint
from urllib.parse import urljoin


class Requester:
    def __init__(self, session, host_url):
        self.HEADERS = {"accept": "application/json"}
        self.session = session
        self.host_url = host_url
        self.response_cache = {}

    def print_error(self, message, response):
        """Print error message and response (if provided)."""
        print("=" * shutil.get_terminal_size().columns)
        print(message)
        if response:
            pprint(response)

    def make_request(self, endpoint, method, **kwargs) -> dict:
        """
        Make API request to endpoint.

        Args:
            endpoint: API endpoint
            method: HTTP method
            kwargs: Parameters to pass to requests method

        Returns:
            JSON response
        """
        if not isinstance(kwargs, dict):
            raise TypeError("Final argument must be of dictionary type")

        if endpoint in self.response_cache:
            return self.response_cache[endpoint].json()

        try:
            response = getattr(self.session, method.lower())(
                urljoin(self.host_url, endpoint),
                **kwargs,
                headers=self.HEADERS,
            )
            response.raise_for_status()
            self.response_cache[endpoint] = response
            return response.json()

        except requests.exceptions.HTTPError as e:
            self.print_error("HTTP ERROR", e)
            return {}

        except requests.exceptions.ConnectionError as e:
            self.print_error("CONNECTION ERROR", e)
            return {}

        except requests.exceptions.Timeout as e:
            self.print_error("TIMEOUT OCCURRED", e)
            return {}

        except requests.exceptions.RequestException as e:
            self.print_error("SOME ERROR OCCURRED", e)
            return {}
