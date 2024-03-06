# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import
from ....base.endpoints.core import EndpointUrl
from .endpoints import AuthPassEndpoint,ValidateTokenEndpoint,HasPermEndpoint
from platform_microservices_utils.ini_parser import endpoint_config


class AuthPassUrl(EndpointUrl):
    """Class for constructing URLs related to the authentication microservice."""

    @classmethod
    def get_auth_pass_url(cls):
        """Get the URL for authenticating user passwords."""
        auth_pass_endpoint = AuthPassEndpoint(endpoint_config)
        return cls.get_url(auth_pass_endpoint)


class ValidateTokenUrl(EndpointUrl):
    """Class for constructing URLs related to token validation in the authentication microservice."""

    @classmethod
    def get_validate_token_url(cls):
        """Get the URL for token validation."""
        validation_token_endpoint = ValidateTokenEndpoint(endpoint_config)
        return cls.get_url(validation_token_endpoint)
    # @classmethod
    # def get_validate_token_url(cls):
    #     """Get the URL for token validation."""
    #     return "http://127.0.0.1:8000/auth/verify-token"


class HasPermUrl(EndpointUrl):
    """Class for constructing URLs related to permission validation in the authentication microservice."""

    @classmethod
    def get_has_perm_url(cls):
        """Get the URL for validating a token."""
        has_perm_endpoint = HasPermEndpoint(endpoint_config)
        return cls.get_url(has_perm_endpoint)

    # @classmethod
    # def get_has_perm_url(cls):
    #     """Get the URL for token validation."""
    #     return "http://127.0.0.1:8000/authorisation/has-perm"
