from .auth import Auth
from .cloudlets import Cloudlet
from .requester import Requester

__version__ = "0.2.0"

"""
The akapy package imports the Auth, Cloudlet, and Requester classes, as well as defines the __version__ variable.

The Auth class provides authentication functionality.
The Cloudlet class represents a cloudlet resource and operations on it.
The Requester provides a request client for making API calls.

Together this allows akapy to authenticate with a service, access cloudlet resources, 
and make API requests to manage and utilize cloudlets. The __version__ provides the package version.
"""
