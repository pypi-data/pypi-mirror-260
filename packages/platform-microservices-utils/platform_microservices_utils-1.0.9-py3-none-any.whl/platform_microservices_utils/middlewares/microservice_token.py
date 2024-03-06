# Python Imports

# Django Imports
from django.http import JsonResponse

# Third-Party Imports
from platform_microservices_utils.base.constants import DefaultHeadersMapping
from platform_microservices_utils.security.hash.hash_validator import KeyValidation
from platform_microservices_utils.security.hmac.token_validator import (
    MicroserviceTokenValidator,
)

# Project-Specific Imports

# Relative Import
from platform_microservices_utils.logger import get_logger


class MicroserviceTokenMiddleware:
    """
    Middleware to validate microservice tokens.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = get_logger(__name__)

    def __call__(self, request):
        try:
            microservice_token = request.headers.get(
                DefaultHeadersMapping.MICROSERVICE_TOKEN.value
            )
            microservice_request_key = request.headers.get(
                DefaultHeadersMapping.MICROSERVICE_REQUEST_KEY.value
            )
            microservice_request_id = request.headers.get(
                DefaultHeadersMapping.MICROSERVICE_REQUEST_ID.value
            )

            if (
                microservice_token
                and microservice_request_key
                and microservice_request_id
            ):
                # Log all values
                self.logger.info(
                    "Microservice token: %s, Microservice request key: %s, Microservice request ID: %s",
                    microservice_token,
                    microservice_request_key,
                    microservice_request_id,
                )

                is_microservice_request = self.is_microservice_request(
                    request_id=microservice_request_id,
                    hashed_key=microservice_request_key,
                )
                if is_microservice_request:
                    is_valid_token = self.validate_token(
                        hashed_token=microservice_token
                    )
                    if not is_valid_token:
                        return JsonResponse(
                            {"error": "Invalid microservice token"}, status=401
                        )
        except Exception as e:
            self.logger.error("An error occurred: %s", e)
            return JsonResponse(
                {"error": "An error occurred while processing the request"}, status=500
            )
        response = self.get_response(request)
        return response

    def validate_token(self, hashed_token):
        """
        Validates the token using HMAC algorithm.
        """
        try:
            return MicroserviceTokenValidator.validate_token(hashed_token=hashed_token)
        except Exception as e:
            self.logger.error("An error occurred while validating token: %s", e)
            return False

    def is_microservice_request(self, request_id, hashed_key):
        """
        Validates the token using HMAC algorithm.
        """
        try:
            return KeyValidation.validate_key(
                request_id=request_id, received_key=hashed_key
            )
        except Exception as e:
            self.logger.error("An error occurred while validating key: %s", e)
            return False
