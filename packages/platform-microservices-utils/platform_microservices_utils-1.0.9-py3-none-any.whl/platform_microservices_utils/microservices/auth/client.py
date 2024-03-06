# Python Imports
import requests

# Django Imports

# Third-Party Imports
from platform_microservices_utils.base.client import MicroserviceClient
from platform_microservices_utils.logger import get_logger

# Project-Specific Imports

# Relative Import
from .requests.endpoints.urls import ValidateTokenUrl, HasPermUrl
from ..base.headers.default import DefaultHeaders
from .params import HasPermParams


class ValidateTokenClient:
    """A class for validating user tokens with the authentication microservice."""

    def __init__(self):
        """Initialize the ValidateTokenClient instance."""
        self.logger = get_logger(__name__)

    def validate_user_token(self, token: str, tenant_identifier: str):
        """Validate a user token with the authentication microservice."""
        try:
            validate_token_response = self._send_auth_request(
                token=token, tenant_identifier=tenant_identifier
            )
            self.logger.debug(
                "Response: %s", validate_token_response.text
            )  # Log response
            if validate_token_response.status_code == 200:
                self.logger.debug("Successfully validated access token.")
            else:
                self.logger.error(
                    "Failed to validate token. Status code: %s. Response text: %s",
                    validate_token_response.status_code,
                    validate_token_response.text,
                )
            return validate_token_response
        except requests.exceptions.RequestException as e:
            self.logger.error("Error during token validation: %s", e)
            return None

    def get_validate_token_url(self):
        """Get the URL for validating a token."""
        url = ValidateTokenUrl.get_validate_token_url()
        self.logger.debug("Retrieved validate token URL: %s", url)
        return url

    def get_validate_token_headers(self, token, tenant_identifier):
        """Get the headers for validating a token."""
        headers = DefaultHeaders(
            token=token, tenant_identifier=tenant_identifier
        ).build_default_headers()
        self.logger.debug("Retrieved validate token headers: %s", headers)
        return headers

    def _send_auth_request(self, token, tenant_identifier) -> requests.Response:
        """Send a request to validate a token."""
        url = self.get_validate_token_url()
        headers = self.get_validate_token_headers(
            token=token, tenant_identifier=tenant_identifier
        )
        response = MicroserviceClient(url=url, headers=headers).get()
        self.logger.debug("Sent token validation request to URL: %s", url)
        return response


class HasPermClient:
    """A class for checking user permissions with the authentication microservice."""

    def __init__(self):
        """Initialize the HasPermClient instance."""
        self.logger = get_logger(__name__)

    def check_user_permissions(
        self, username: str, endpoint: str, token: str, tenant_identifier: str
    ):
        """Check a user's permissions with the authentication microservice."""
        try:
            has_perm_response = self._send_auth_request(
                username=username,
                endpoint=endpoint,
                token=token,
                tenant_identifier=tenant_identifier,
            )
            self.logger.debug("Response: %s", has_perm_response.text)  # Log response
            if has_perm_response.status_code == 200:
                self.logger.debug("Successfully checked user permissions.")
            else:
                self.logger.error(
                    "Failed to check permissions. Status code: %s. Response text: %s",
                    has_perm_response.status_code,
                    has_perm_response.text,
                )
            return has_perm_response
        except requests.exceptions.RequestException as e:
            self.logger.error("Error during permissions check: %s", e)
            return None

    def get_check_permissions_url(self):
        """Get the URL for checking permissions."""
        url = HasPermUrl.get_has_perm_url()
        self.logger.debug("Retrieved check permissions URL: %s", url)
        return url

    def get_check_permissions_headers(self, token, tenant_identifier):
        """Get the headers for checking permissions."""
        headers = DefaultHeaders(
            token=token, tenant_identifier=tenant_identifier
        ).build_default_headers()
        self.logger.debug("Retrieved check permissions headers: %s", headers)
        return headers

    def get_check_permissions_params(self, username, endpoint):
        """Get the params for checking permissions."""
        params = HasPermParams.build_params(username=username, endpoint=endpoint)
        self.logger.debug("Retrieved check permissions params: %s", params)
        return params

    def _send_auth_request(
        self, username, endpoint, token, tenant_identifier
    ) -> requests.Response:
        """Send a request to check permissions."""
        url = self.get_check_permissions_url()
        headers = self.get_check_permissions_headers(
            token=token, tenant_identifier=tenant_identifier
        )
        params = self.get_check_permissions_params(username=username, endpoint=endpoint)
        response = MicroserviceClient(url=url, headers=headers).get(params=params)
        self.logger.debug("Sent permissions check request to URL: %s", url)
        return response
