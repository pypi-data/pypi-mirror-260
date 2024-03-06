# Python Imports
import hashlib
import hmac

# Django Imports

# Third-Party Imports
from decouple import config

# Project-Specific Imports
from platform_microservices_utils.logger import get_logger

# Relative Import






class MicroserviceTokenValidator:
    """
    TokenValidator class provides methods to validate tokens using HMAC algorithm.
    """

    @classmethod
    def validate_token(cls, hashed_token):
        """
        Validates the token using HMAC algorithm.
        """
        secret_key = config("MICROSERVICE_SECRET_KEY")
        logger = get_logger(__name__)

        if not isinstance(hashed_token, str):
            logger.error("Invalid input: hashed_token must be a string")
            raise ValueError("Invalid input: hashed_token must be a string")

        try:
            # Use HMAC algorithm to recreate the hashed token based on the secret key
            recreated_hashed_token = hmac.new(
                secret_key.encode(), None, hashlib.sha256
            ).hexdigest()
        except Exception as e:
            logger.exception("Error occurred while generating hash")
            raise RuntimeError("Error occurred while generating hash") from e

        # Compare the recreated hashed token with the received hashed token
        is_valid = hmac.compare_digest(recreated_hashed_token, hashed_token)

        if is_valid:
            logger.info("Token validation successful")
        else:
            logger.warning("Token validation failed")

        return is_valid


