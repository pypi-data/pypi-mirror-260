from ..requester import Requester
from ..auth import Auth


class Cloudlet:
    """Handles Cloudlet API requests."""

    def __init__(self, auth=None) -> None:
        """
        Initialize Cloudlet API client.

        Args:
            auth: Auth object for handling credentials. Will use default if not provided.
        """
        if auth is None:
            self.auth = Auth()
        else:
            self.auth = auth

        self.endpoint = "cloudlets/api/v2"
        self.requester = Requester(self.auth.get_session(), self.auth.host_url)

    def get_all(self):
        return self.requester.make_request(
            method = "GET",
            endpoint = f"{self.endpoint}/cloudlet-info"
        )
