# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

from platform_microservices_utils.ini_parser import endpoint_config

# Relative Import
from ....base.endpoints.core import EndpointUrl
from .endpoints import IsSubscribedEndpoint, IncreaseUsageEndpoint


class IsSubscribedUrl(EndpointUrl):
    """Class for constructing URLs related to checking subscription status."""

    @classmethod
    def get_is_subscribed_url(cls):
        """Get the URL for checking tenant subscription status."""
        is_subscribed = IsSubscribedEndpoint(endpoint_config)
        return cls.get_url(is_subscribed)


class IncreaseUsageUrl(EndpointUrl):
    """Class for constructing URLs related to increasing usage counts."""

    @classmethod
    def get_increase_count_url(cls):
        """Get the URL for increasing usage count."""
        is_subscribed = IncreaseUsageEndpoint(endpoint_config)
        return cls.get_url(is_subscribed)
