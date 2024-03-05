from akamai.edgegrid import EdgeGridAuth, EdgeRc
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class Auth:
    """Handles authentication and creates requests session."""

    def __init__(
        self,
        EDGERC_PATH: str = "~/.edgerc",
        SECTION: str = "default",
        RETRY_ITERATION: int = 5,
        RETRY_BACKOFF: int = 1,
    ) -> None:
        """
        Initialize authentication and create requests session.

        Args:
            EDGERC_PATH: Path to .edgerc file
            SECTION: Section in .edgerc file
            RETRY_ITERATION: Number of retries
            RETRY_BACKOFF: Backoff factor between retries
        """

        self.SECTION = SECTION
        self.EDGERC = EdgeRc(EDGERC_PATH)
        self.HOSTURL = f"https://{self.EDGERC.get(self.SECTION, 'host')}"
        self.SESSION = requests.Session()

        self.RETRY_STRATEGY = Retry(
            total=RETRY_ITERATION,
            backoff_factor=RETRY_BACKOFF,
            status_forcelist=tuple(range(500, 600)),
            allowed_methods=frozenset(["DELETE", "GET", "POST", "PUT"]),
        )

        self.ADAPTER = HTTPAdapter(max_retries=self.RETRY_STRATEGY)
        self.SESSION.mount("http://", self.ADAPTER)
        self.SESSION.mount("https://", self.ADAPTER)

        self.SESSION.auth = EdgeGridAuth.from_edgerc(self.EDGERC, self.SECTION)

    def get_session(self):
        """Returns the requests session."""
        return self.SESSION

    @property
    def host_url(self):
        """Returns the base API host URL."""
        return self.HOSTURL
