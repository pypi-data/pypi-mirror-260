from ..requester import Requester
from ..auth import Auth
from typing import Union, Dict, List


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
        self.cloudlet_types = {
            0: {"name": "Edge Redirector", "abbreviation": "ER"},
            1: {"name": "Visitor Prioritization", "abbreviation": "VP"},
            3: {"name": "Forward Rewrite", "abbreviation": "FR"},
            4: {"name": "Request Control", "abbreviation": "RC"},
            5: {"name": "API Prioritization", "abbreviation": "AP"},
            6: {"name": "Audience Segmentation", "abbreviation": "AS"},
            7: {"name": "Phased Release", "abbreviation": "PR"},
            9: {"name": "Application Load Balancer", "abbreviation": "ALB"},
        }

    def _get_cloudlet_id(self, cloudlet_id: Union[int, str]) -> Union[int, None]:
        """Converts a cloudlet ID to an integer.

        Args:
            cloudlet_id (Union[int, str]): The cloudlet ID, either as an integer
                or a string name/abbreviation.

        Returns:
            int: The integer cloudlet ID.

        This handles looking up the integer ID from the name/abbreviation
        if a string is provided.
        """
        cloudlet_type_int = None
        if isinstance(cloudlet_id, int):
            cloudlet_type_int = cloudlet_id
        else:
            for k, v in self.cloudlet_types.items():
                if cloudlet_id in (v["name"], v["abbreviation"]):
                    cloudlet_type_int = k
                    break
        return cloudlet_type_int

    def get_all(self) -> List[Dict]:
        """Gets information on all cloudlets.

        Makes a GET request to the /cloudlet-info endpoint to retrieve 
        a list of dictionaries containing information on all available cloudlets.

        Returns:
            List[Dict]: A list of dictionaries containing information on all cloudlets.
        """
        return self.requester(method="GET", endpoint=f"{self.endpoint}/cloudlet-info")

    def by_type(self, cloudlet_id: Union[int, str]) -> List[Dict]:
        """Get cloudlet type information.

        Args:
            cloudlet_id (Union[int, str]): The cloudlet type identifier, 
                either as an integer or a name/abbreviation string.
                Cloudlet type options:
                    0: "Edge Redirector" (ER)
                    1: "Visitor Prioritization" (VP)
                    3: "Forward Rewrite" (FR)
                    4: "Request Control" (RC)
                    5: "API Prioritization" (AP)
                    6: "Audience Segmentation" (AS)
                    7: "Phased Release" (PR)
                    9: "Application Load Balancer" (ALB)

        Returns:
            List[Dict]: List of dictionaries containing the cloudlet type information.

        This function handles looking up the cloudlet type integer ID
        from the name or abbreviation string if provided.
        It constructs the API endpoint using this integer ID and makes the request.
        """

        return self.requester(
            method="GET", endpoint=f"{self.endpoint}/{self._get_cloudlet_id(cloudlet_id)}"
        )

    def list_groups(self) -> List[Dict]:
        """
        List all groups available to the user.

        Makes a GET request to the groups endpoint to retrieve a
        list containing information about the groups.

        Returns:
            List[Dict]: List containing the group information dicts.
        """
        return self.requester(endpoint=f"{self.endpoint}/group-info", method="GET")

    def list_policies(
        self, 
        is_deleted: bool = False, 
        cloudlet_id: Union[int, str, None] = None
    ) -> List[Dict]:
        """
        List policies filtered by deleted status and cloudlet ID.

        Args:
            is_deleted: Whether to include deleted policies.
            cloudlet_id: Optional cloudlet ID to filter by. Can pass:
                - Integer cloudlet ID
                - String abbreviation (e.g. "ER") 
                - Full cloudlet name (e.g. "Edge Redirector")

        Returns: 
            List of dictionaries containing policy information.
        """
        params = f"?includeDeleted={is_deleted}"
        if cloudlet_id is not None:
            params += f"&cloudletId={self._get_cloudlet_id(cloudlet_id)}"

        print(params)

        return self.requester(
            endpoint=f"{self.endpoint}/policies{params}", 
            method="GET"
        )
