# Python Imports
import requests

# Third-Party Imports
from platform_microservices_utils.base.client import MicroserviceClient
from platform_microservices_utils.logger import get_logger

from .headers import MicroserviceAdminHeaders
from .params import IsSubscribedParams
from .payloads import IncreaseUsageCountPayload

# Relative Import
from .requests.endpoints.urls import IncreaseUsageUrl, IsSubscribedUrl

# Django Imports


# Project-Specific Imports


class IsTenantSubscribedClient:
    """A class for validating tenant subscription status with the subscription microservice."""

    def __init__(self):
        """Initialize the IsSubscriptionValidator instance."""
        self.logger = get_logger(__name__)

    def validate_subscription(
        self, username: str, endpoint_url: int, tenant_identifier: str
    ):
        """Validate a user token with the subscription microservice."""
        try:
            subscription_check_response = self._send_subscription_check_request(
                username=username,
                endpoint_url=endpoint_url,
                tenant_identifier=tenant_identifier,
            )
            self.logger.debug(
                "Response: %s", subscription_check_response.text
            )  # Log response
            if subscription_check_response.status_code == 200:
                self.logger.debug("Successfully validated subscription status.")
            else:
                self.logger.error(
                    "Failed to validate subscription status. Status code: %s. Response text: %s",
                    subscription_check_response.status_code,
                    subscription_check_response.text,
                )
            return subscription_check_response
        except requests.exceptions.RequestException as e:
            self.logger.error("Error during subscription status validation: %s", e)
            return None

    def get_subscription_check_url(self):
        """Get the URL for validating subscription status."""
        url = IsSubscribedUrl.get_is_subscribed_url()
        self.logger.debug("Retrieved subscription status check URL: %s", url)
        return url

    def get_subscription_check_headers(self, tenant_identifier):
        """Get the headers for validating subscription status."""
        headers = MicroserviceAdminHeaders(
            tenant_identifier=tenant_identifier
        ).build_headers()
        self.logger.debug("Retrieved subscription status check headers: %s", headers)
        return headers

    def get_subscription_check_params(
        self, username: str, endpoint_url: int, tenant_identifier: str
    ):
        """Get the params for validating subscription status."""
        params = IsSubscribedParams.build_params(
            username=username,
            endpoint_url=endpoint_url,
            tenant_identifier=tenant_identifier,
        )
        self.logger.debug("Retrieved subscription status check params: %s", params)
        return params

    def _send_subscription_check_request(
        self, username: str, endpoint_url: int, tenant_identifier: str
    ) -> requests.Response:
        """Send a request to validate subscription status."""
        url = self.get_subscription_check_url()
        headers = self.get_subscription_check_headers(
            tenant_identifier=tenant_identifier
        )
        response = MicroserviceClient(url=url, headers=headers).get(
            self.get_subscription_check_params(
                username=username,
                endpoint_url=endpoint_url,
                tenant_identifier=tenant_identifier,
            )
        )
        self.logger.debug("Sent subscription status check request to URL: %s", url)
        return response


class IncreaseUsageCountClient:
    """A client class for increasing usage counts with the subscription microservice."""

    def __init__(self):
        """Initialize the IncreaseUsageCountClient instance."""
        self.logger = get_logger(__name__)

    def increase_usage_count(
        self, username: str, endpoint_url: int, tenant_identifier: str
    ):
        """Increase usage count with the subscription microservice."""
        try:
            increase_usage_response = self._send_increase_usage_count_request(
                username=username,
                endpoint_url=endpoint_url,
                tenant_identifier=tenant_identifier,
            )
            self.logger.debug(
                "Response: %s", increase_usage_response.text
            )  # Log response
            if increase_usage_response.status_code == 200:
                self.logger.debug("Successfully increased usage count.")
            else:
                self.logger.error(
                    "Failed to increase usage count. Status code: %s. Response text: %s",
                    increase_usage_response.status_code,
                    increase_usage_response.text,
                )
            return increase_usage_response
        except requests.exceptions.RequestException as e:
            self.logger.error("Error during increasing usage count: %s", e)
            return None

    def get_increase_usage_count_url(self):
        """Get the URL for increasing usage count."""
        url = IncreaseUsageUrl.get_increase_count_url()
        self.logger.debug("Retrieved increase usage count URL: %s", url)
        return url

    def get_increase_usage_count_headers(self):
        """Get the headers for increasing usage count."""
        headers = MicroserviceAdminHeaders().build_headers()
        self.logger.debug("Retrieved increase usage count headers: %s", headers)
        return headers

    def get_increase_usage_count_payload(
        self, username: str, endpoint_url: int, tenant_identifier: str
    ):
        """Get the payload for increasing usage count."""
        payload = IncreaseUsageCountPayload(
            username=username,
            endpoint_url=endpoint_url,
            tenant_identifier=tenant_identifier,
        ).get_payload()
        self.logger.debug("Retrieved increase usage count payload: %s", payload)
        return payload

    def _send_increase_usage_count_request(
        self, username: str, endpoint_url: int, tenant_identifier: str
    ) -> requests.Response:
        """Send a request to increase usage count."""
        url = self.get_increase_usage_count_url()
        headers = self.get_increase_usage_count_headers()
        response = MicroserviceClient(url=url, headers=headers).post(
            data=self.get_increase_usage_count_payload(
                username=username,
                endpoint_url=endpoint_url,
                tenant_identifier=tenant_identifier,
            )
        )
        self.logger.debug("Sent increase usage count request to URL: %s", url)
        return response

