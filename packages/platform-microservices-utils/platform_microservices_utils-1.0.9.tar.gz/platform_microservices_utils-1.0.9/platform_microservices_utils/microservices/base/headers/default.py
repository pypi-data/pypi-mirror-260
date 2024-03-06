# Python Imports

# Django Imports

# Third-Party Imports
from platform_microservices_utils.base.constants import DefaultHeadersMapping

# Project-Specific Imports

# Relative Import



class DefaultHeaders():
    """Class for building default headers for requests."""

    def __init__(self, token, tenant_identifier):
        """Initialize the DefaultHeaders instance."""
        self.token = token
        self.tenant_identifier = tenant_identifier

    def build_default_headers(self) -> dict:
        """Build default headers for requests."""
        return {
            DefaultHeadersMapping.AUTHORIZATION.value: self.token,
            DefaultHeadersMapping.TENANT_IDENTIFIER.value: self.tenant_identifier,
        }
