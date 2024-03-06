# Python Imports

# Django Imports

# Third-Party Imports
from platform_microservices_utils.security.hash.hash_generator import KeyDerivation
from platform_microservices_utils.security.hmac.token_generator import (
    MicroserviceTokenGenerator,
)
from platform_microservices_utils.common import UUIDGenerator

# Project-Specific Imports

# Relative Import
from .constants import DefaultHeadersMapping


class HeaderBuilder:
    """Build headers for microservice-to-microservice communication."""

    def __init__(
        self,
        tenant_identifier=None,
        microservice_token=None,
        microservice_request_key=None,
        microservice_request_id=None,
        **kwargs
    ):
        """Initialize HeaderBuilder."""
        self.tenant_identifier = tenant_identifier
        self.microservice_token = microservice_token
        self.microservice_request_key = microservice_request_key
        self.microservice_request_id = microservice_request_id
        self.additional_headers = kwargs

    def _generate_microservice_token(self):
        """Generate a microservice token using the token generator."""
        return MicroserviceTokenGenerator().generate_token()

    def _generate_microservice_request_key(self, request_id):
        """Generate a microservice token using the token generator."""
        return KeyDerivation.generate_key(request_id=request_id)

    def _generate_microservice_request_id(self):
        """Generate a microservice token using the token generator."""
        return UUIDGenerator.generate_uuid()

    def build_headers(self):
        """Build headers for microservice-to-microservice communication."""
        headers = {}
        request_id = self._generate_microservice_request_id()
        if self.tenant_identifier:
            headers[DefaultHeadersMapping.TENANT_IDENTIFIER.value] = (
                self.tenant_identifier
            )
        if self.microservice_token:
            headers[DefaultHeadersMapping.MICROSERVICE_TOKEN.value] = (
                self._generate_microservice_token()
            )
        if self.microservice_request_key:
            headers[DefaultHeadersMapping.MICROSERVICE_REQUEST_KEY.value] = (
                self._generate_microservice_request_key(request_id)
            )
        if self.microservice_request_id:
            headers[DefaultHeadersMapping.MICROSERVICE_REQUEST_ID.value] = request_id

        headers.update(
            {
                key: value
                for key, value in self.additional_headers.items()
                if value is not None
            }
        )
        return headers
