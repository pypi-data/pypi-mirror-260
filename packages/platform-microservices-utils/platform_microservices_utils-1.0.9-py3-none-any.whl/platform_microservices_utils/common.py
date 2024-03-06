# Python Imports
import uuid

# Relative Import
from platform_microservices_utils.logger import get_logger
from platform_microservices_utils.base.constants import DefaultHeadersMapping

# Third-Party Imports

# Django Imports

# Project-Specific Imports


class DynamicAttributes:
    """
    A class for creating dynamic objects with key-value pairs as attributes.

    Args:
        **kwargs: Key-value pairs to be assigned as object attributes.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class QueryParams:
    """A class for dynamically creating query parameters."""

    def __init__(self, **kwargs):
        """Initialize the QueryParams with the provided parameters."""
        self.params = kwargs

    def add_param(self, key, value):
        """Add a query parameter."""
        self.params[key] = value

    def remove_param(self, key):
        """Remove a query parameter."""
        if key in self.params:
            del self.params[key]

    def generate_query_string(self):
        """Generate the query string."""
        query_string = "&".join(
            [f"{key}={value}" for key, value in self.params.items()]
        )
        return f"{query_string}" if query_string else ""


class UUIDGenerator:
    """
    Utility class for generating UUIDs.
    """

    @classmethod
    def generate_uuid(cls):
        """
        Generates a UUID.
        """
        return str(uuid.uuid4())


class TokenAndTenantExtractionService:
    """Service to extract token and tenant identifier from the request."""

    def __init__(self, request):
        """Initialize the TokenAndTenantExtractionService instance with the request."""
        self.request = request
        self.logger = get_logger(__name__)

    def extract_token(self):
        """Extracts the token from the request."""
        authorization_header = self.request.headers.get(
            DefaultHeadersMapping.AUTHORIZATION.value
        )
        if authorization_header:
            token_parts = authorization_header.split()
            if len(token_parts) == 2 and (
                token_parts[0].lower() == "bearer" or token_parts[0].lower() == "jwt"
            ):
                token = token_parts[1]
                self.logger.debug("Token extracted successfully: %s", token)
                return authorization_header
        self.logger.debug("Token missing in request.")
        return None

    def extract_tenant_identifier(self):
        """Extracts the tenant identifier from the request."""
        tenant_identifier = self.request.headers.get(
            DefaultHeadersMapping.TENANT_IDENTIFIER.value
        )
        if tenant_identifier:
            self.logger.debug(
                "Tenant identifier extracted successfully: %s", tenant_identifier
            )
        else:
            self.logger.debug("Tenant identifier missing in request.")
        return tenant_identifier
