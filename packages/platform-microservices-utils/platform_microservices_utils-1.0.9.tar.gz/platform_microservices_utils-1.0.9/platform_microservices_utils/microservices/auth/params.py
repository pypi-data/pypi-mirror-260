# Python Imports
from platform_microservices_utils.common import DynamicAttributes

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import



class HasPermParams:
    """Class for building parameters for permission validation."""

    @classmethod
    def build_params(cls, username: str, endpoint: str):
        """Build parameters for permission validation. Returns a dictionary."""
        return DynamicAttributes(username=username, endpoint_url=endpoint).__dict__
