# Python Imports

# Django Imports
from django.http import JsonResponse

# Third-Party Imports

# Project-Specific Imports
from platform_microservices_utils.logger import get_logger

# Relative Import
from ..core.base import MicroserviceBase
from ..hash.hash_validator import KeyValidation
from ..hmac.token_validator import MicroserviceTokenValidator






class MicroserviceAuthenticator(MicroserviceBase):
    def __init__(self, request):
        """
        Initialize MicroserviceAuthenticator with the provided request.
        """
        self.logger = get_logger(__name__)
        super().__init__(request)

    def authenticate(self):
        """
        Authenticate microservice requests.

        Returns:
            Tuple: A tuple containing a boolean indicating authentication success or failure,
            and a JSON response if authentication fails.
        """
        try:
            if (
                self.microservice_token
                and self.microservice_request_key
                and self.microservice_request_id
            ):
                # Scenario 1: Successful authentication
                self.logger.info(
                    "Microservice token: %s, Microservice request key: %s, Microservice request ID: %s",
                    self.microservice_token,
                    self.microservice_request_key,
                    self.microservice_request_id,
                )

                is_microservice_request = MicroserviceRequestValidation(
                    request=self.request
                ).is_valid_key()
                if is_microservice_request:
                    self.logger.info("Microservice request is valid")
                    is_valid_token = MicroserviceTokenValidation(
                        request=self.request
                    ).is_valid_token()
                    if not is_valid_token:
                        # Scenario 2: Failed authentication due to invalid token
                        self.logger.error("Invalid microservice token")
                        return False, JsonResponse(
                            {"error": "Invalid microservice token"}, status=401
                        )
                    # Scenario 3: Failed authentication due to invalid request
                    self.logger.error("Invalid microservice request")
                self.logger.error(
                    "Missing microservice token, request key, or request ID"
                )
                return True, None

        except Exception as e:
            self.logger.error("An error occurred: %s", e)
            return JsonResponse(
                {"error": "An error occurred while processing the request"}, status=500
            )


class MicroserviceTokenValidation(MicroserviceBase, MicroserviceTokenValidator):
    """
    Validates microservice tokens.
    """

    def __init__(self, request):
        """
        Initialize MicroserviceTokenValidation with the provided request.
        """
        super().__init__(request)
        self.logger = get_logger(__name__)

    def is_valid_token(self):
        """
        Check if the microservice token is valid.

        Returns:
            Tuple: A tuple containing a boolean indicating token validity and a JSON response if invalid.
        """
        if self.microservice_token:
            is_valid_token = self.validate_token(hashed_token=self.microservice_token)
            if not is_valid_token:
                self.logger.error("Invalid microservice token")
                return False, JsonResponse(
                    {"error": "Invalid microservice token"}, status=401
                )
            else:
                self.logger.info("Microservice token is valid")
        return True, None


class MicroserviceRequestValidation(MicroserviceBase, KeyValidation):
    """
    Validates microservice requests.
    """

    def __init__(self, request):
        """
        Initialize MicroserviceRequestValidation with the provided request.
        """
        super().__init__(request)
        self.logger = get_logger(__name__)

    def is_valid_key(self):
        """
        Check if the microservice request key is valid.

        Returns:
            Tuple: A tuple containing a boolean indicating key validity and a JSON response if invalid.
        """
        if self.microservice_request_id and self.microservice_request_key:
            is_valid_key = self.validate_key(
                request_id=self.microservice_request_id,
                received_key=self.microservice_request_key,
            )
            if is_valid_key:
                self.logger.info("Microservice request key is valid")
                return True, None
        return False, JsonResponse(
            {"error": "Invalid microservice request key"}, status=401
        )
