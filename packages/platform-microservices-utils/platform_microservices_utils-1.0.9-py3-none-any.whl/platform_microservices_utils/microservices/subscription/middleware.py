# Python Imports
from abc import ABC, abstractmethod

# Third-Party Imports
from decouple import config

# Django Imports
from django.http import JsonResponse
from django.urls import resolve

# from multitenancy.tenant_context import set_current_tenant
from platform_microservices_utils.common import TokenAndTenantExtractionService
from platform_microservices_utils.logger import get_logger
from platform_microservices_utils.microservices.auth.middleware import (
    ServiceUnavailableResponse,
)
from platform_microservices_utils.security.validations.microservice_auth import (
    MicroserviceRequestValidation,
)

from .client import IncreaseUsageCountClient, IsTenantSubscribedClient
from .response import IsSubcribedResponse, SuccessResponse

# Project-Specific Imports


# Relative Import


class BaseSubscriptionMiddleware:
    """Base class for subscription middleware."""

    def __init__(self, get_response):
        """Initialize the BaseSubscriptionMiddleware instance."""
        self.get_response = get_response
        self.logger = get_logger(__name__)
        self.token_client = IsTenantSubscribedClient()
        self.username = None
        self.tenant_identifier = None
        self.endpoint_url = None

    def __call__(self, request):
        """Handle the incoming request."""

        # Get the current database connection
        self.endpoint_url = self._get_endpoint_name(request=request)
        is_valid_key, response = MicroserviceRequestValidation(
            request=request
        ).is_valid_key()
        if self._is_excluded_endpoint(endpoint=self.endpoint_url) or is_valid_key:
            return self.get_response(request)
        token_and_tenant_extractor = TokenAndTenantExtractionService(request=request)
        token = token_and_tenant_extractor.extract_token()
        tenant_identifier = token_and_tenant_extractor.extract_tenant_identifier()
        # self._set_default_connection()
        self._set_username(request=request)
        self._set_tenant_identifier(tenant_identifier=tenant_identifier)

        validation_response = self.token_client.validate_subscription(
            username=self.username,
            endpoint_url=self.endpoint_url,
            tenant_identifier=self.tenant_identifier,
        )
        return self._handle_validation_result(validation_response, request)

    def _handle_validation_result(self, validation_response, request):
        """Handle the subscription validation result."""

        if validation_response is None:
            return ServiceUnavailableResponse.get_response()
        if validation_response.status_code == 200:
            validation_response_obj = SuccessResponse(**validation_response.json())
            data_obj = IsSubcribedResponse(**validation_response_obj.data)
            if data_obj.is_subscribed and data_obj.has_count:
                response = self.get_response(request)
                is_incressed, increase_usage_respone = self._increase_usage(
                    username=self.username,
                    tenant_identifier=self.tenant_identifier,
                    endpoint_url=self.endpoint_url,
                )
                if is_incressed:
                    return response
        self.logger.error(
            "subscription  validation failed with status code: %s",
            validation_response.status_code,
        )
        response_json = validation_response.json()
        del response_json['data']
        return JsonResponse(response_json, status=validation_response.status_code
        )

    def _get_endpoint_name(self, request):
        """Helper method to get the endpoint name from the request."""
        resolver_match = resolve(request.path_info)
        return resolver_match.route if resolver_match.route is not None else None

    @abstractmethod
    def _is_excluded_endpoint(self, endpoint):
        """Check if an endpoint is excluded from authentication."""
        pass

    def _increase_usage(self, username, tenant_identifier, endpoint_url):
        """Check if an endpoint is excluded from authentication."""
        resposne = IncreaseUsageCountClient().increase_usage_count(
            username=username,
            tenant_identifier=tenant_identifier,
            endpoint_url=endpoint_url,
        )
        if resposne.status_code in [200, 201]:
            return True, resposne.json()
        return False, resposne.json()

    def _set_username(self, request):
        """Helper method to get set username."""
        self.username = request.user.username

    def _set_tenant_identifier(self, tenant_identifier):
        """Helper method to get set tenant identifier."""
        self.tenant_identifier = tenant_identifier
