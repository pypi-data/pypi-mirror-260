# Python Imports
from enum import Enum

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import


class DefaultHeadersMapping(Enum):
    """Enumeration of default headers mapping."""

    TENANT_IDENTIFIER = "Tenant-Identifier"
    AUTHORIZATION = "Authorization"
    MICROSERVICE_TOKEN = "X-Microservice-Token"
    MICROSERVICE_REQUEST_KEY = "X-Microservice-Request-Key"
    MICROSERVICE_REQUEST_ID = "X-Microservice-Request-Id"

class RequestHeadersMapping(Enum):
    """Enumeration of default headers mapping."""

    TENANT_IDENTIFIER = "HTTP_TENANT_IDENTIFIER"
    AUTHORIZATION = "Authorization"
