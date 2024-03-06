# Python Imports
from abc import ABC, abstractmethod

# Django Imports
from django.http import JsonResponse
from django.urls import resolve

# Third-Party Imports
from platform_microservices_utils.logger import get_logger
from platform_microservices_utils.common import TokenAndTenantExtractionService
from platform_microservices_utils.microservices.auth.response import (
    SuccessResponse,
    IsValidResponse,
    HasPermResponse,
)
from platform_microservices_utils.security.validations.microservice_auth import (
    MicroserviceRequestValidation,
)

from properties import EXCLUDED_ENDPOINTS

# Project-Specific Imports

 # Relative Import
from .client import ValidateTokenClient, HasPermClient

class BaseAuthenticationMiddleware:
    """Base class for authentication middleware."""

    def __init__(self, get_response):
        """Initialize the BaseAuthenticationMiddleware instance."""
        self.get_response = get_response
        self.logger = get_logger(__name__)
        self.token_client = ValidateTokenClient()

    def __call__(self, request):
        """Handle the incoming request."""
        endpoint = self._get_endpoint_name(request=request)
        is_valid_key, response = MicroserviceRequestValidation(
            request=request
        ).is_valid_key()

        if self._is_excluded_endpoint(endpoint=endpoint) or is_valid_key:
            return self.get_response(request)
        token_and_tenant_extractor = TokenAndTenantExtractionService(request=request)
        token = token_and_tenant_extractor.extract_token()
        tenant_identifier = token_and_tenant_extractor.extract_tenant_identifier()
        validation_response = self.token_client.validate_user_token(
            token, tenant_identifier
        )
        return self._handle_validation_result(validation_response, request)

    def _handle_validation_result(self, validation_response, request):
        """Handle the token validation result."""
        if validation_response is None:
                return ServiceUnavailableResponse.get_response()
        if validation_response.status_code == 200:
            validation_response_obj = SuccessResponse(**validation_response.json())
            data_obj = IsValidResponse(**validation_response_obj.data)
            if data_obj.is_valid:
                request.username = data_obj.username
                return self.get_response(request)

        self.logger.error(
            "Token validation failed with status code: %s",
            validation_response.status_code,
        )

        return JsonResponse(
            validation_response.json(), status=validation_response.status_code
        )

    def _get_endpoint_name(self, request):
        """Helper method to get the endpoint name from the request."""
        resolver_match = resolve(request.path_info)
        return resolver_match.route if resolver_match.route is not None else None

    @abstractmethod
    def _is_excluded_endpoint(self, endpoint):
        """Check if an endpoint is excluded from authentication."""
        endpoint in EXCLUDED_ENDPOINTS


class BaseAuthorizationMiddleware:
    """Base class for authorization middleware."""

    def __init__(self, get_response):
        """Initialize the BaseAuthorizationMiddleware instance."""
        self.get_response = get_response
        self.logger = get_logger(__name__)
        self.perm_client = HasPermClient()

    def __call__(self, request):
        """Handle the incoming request."""
        endpoint = self._get_endpoint_name(request=request)
        is_valid_key, response = MicroserviceRequestValidation(
            request=request
        ).is_valid_key()
        if self._is_excluded_endpoint(endpoint=endpoint) or is_valid_key:
            return self.get_response(request)
        username = request.username
        token_and_tenant_extractor = TokenAndTenantExtractionService(request=request)
        token = token_and_tenant_extractor.extract_token()
        tenant_identifier = token_and_tenant_extractor.extract_tenant_identifier()
        has_perm_response = self.perm_client.check_user_permissions(
            username=username,
            endpoint=endpoint,
            token=token,
            tenant_identifier=tenant_identifier,
        )
        return self._handle_validation_result(has_perm_response, request)

    def _handle_validation_result(self, has_perm_response, request):
        """Handle the permission validation result."""
        if has_perm_response is None:
            return ServiceUnavailableResponse.get_response()
        if has_perm_response.status_code == 200:
            has_perm_response_obj = SuccessResponse(**has_perm_response.json())
            data_obj = HasPermResponse(**has_perm_response_obj.data)
            if data_obj.has_perm:
                return self.get_response(request)

        self.logger.error(
            "Permission validation failed with status code: %s",
            has_perm_response.status_code,
        )

        return JsonResponse(
            has_perm_response.json(), status=has_perm_response.status_code
        )

    def _get_endpoint_name(self, request):
        """Helper method to get the endpoint name from the request."""
        resolver_match = resolve(request.path_info)
        return resolver_match.route if resolver_match.route is not None else None

    @abstractmethod
    def _is_excluded_endpoint(self, endpoint):
        """Check if an endpoint is excluded from authorization."""
        pass



class ServiceUnavailableResponse:
    @classmethod
    def get_response(cls):
        """Returns the service unavailable response."""
        return JsonResponse(
            {
                "error": "Service Currently Unavailable. Please try again after some time.",
                "status": 503,
            },
            status=503,
        )
