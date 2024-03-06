# Python Imports

# Django Imports

# Third-Party Imports
from platform_microservices_utils.url_builder import BuildUrl

# Project-Specific Imports

# Relative Import


class BaseEndpoint:
    """Base class for managing generic endpoints."""

    def __init__(self,endpoint_config_manager):
        """Initialize the BaseEndpoint instance."""
        self.endpoint_config = endpoint_config_manager

    def get_endpoint(self):
        """Get the endpoint."""
        raise NotImplementedError("Subclasses must implement this method.")


class EndpointUrl(BuildUrl):
    """Class for constructing URLs related to various"""

    @classmethod
    def get_url(cls, endpoint_class):
        """Get the URL for the specified endpoint class."""
        endpoint = endpoint_class.get_endpoint()
        return cls.construct_url(endpoint=endpoint)
