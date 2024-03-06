# Python Imports
from platform_microservices_utils.common import DynamicAttributes

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import


class IsSubscribedParams:
    """Class for assembling parameters related to subscription status check."""

    @classmethod
    def build_params(cls, username: str, endpoint_url: str, tenant_identifier: str):
        """Build parameters for subscription status validation."""
        return DynamicAttributes(
            username=username,
            endpoint_url=endpoint_url,
            tenant_identifier=tenant_identifier,
        ).__dict__
