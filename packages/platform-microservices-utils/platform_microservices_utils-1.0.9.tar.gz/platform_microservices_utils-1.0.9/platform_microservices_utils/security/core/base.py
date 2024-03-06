# Python Imports
import base64
import hashlib

# Django Imports

# Third-Party Imports
from platform_microservices_utils.config.env import SecretKeyProvider
from platform_microservices_utils.common import UUIDGenerator
from platform_microservices_utils.base.constants import DefaultHeadersMapping

# Project-Specific Imports

# Relative Import


class KeyDerivationBase:
    """
    Base class for key derivation using PBKDF2.
    """

    @classmethod
    def derive_key(cls, secret_key=None, request_id=None, iterations=100000):
        """
        Derive a key using PBKDF2.
        """

        combined_key = cls._combine_keys(request_id, secret_key)

        # Use PBKDF2 to derive a key
        derived_key = hashlib.pbkdf2_hmac(
            "sha256", combined_key.encode(), b"", iterations=iterations
        )
        encoded_key = base64.b64encode(derived_key).decode("utf-8")

        return encoded_key

    @classmethod
    def _combine_keys(cls, request_id, secret_key):
        """
        Combine the secret key and request ID with a specific format.
        """
        return f"{secret_key}###{request_id}"


class KeyGenerationUtility:
    """Utility class for key generation."""

    @classmethod
    def get_secret_key(cls):
        """Get the secret key."""
        return SecretKeyProvider.get_secret_key()

    @classmethod
    def get_request_id(cls):
        """Generate a UUID as a request ID."""
        return UUIDGenerator.generate_uuid()


class MicroserviceBase:
    def __init__(self, request):
        self.request = request
        self.microservice_token = request.headers.get(
            DefaultHeadersMapping.MICROSERVICE_TOKEN.value
        )
        self.microservice_request_key = request.headers.get(
            DefaultHeadersMapping.MICROSERVICE_REQUEST_KEY.value
        )
        self.microservice_request_id = request.headers.get(
            DefaultHeadersMapping.MICROSERVICE_REQUEST_ID.value
        )
