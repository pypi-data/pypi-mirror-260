# Python Imports
import hmac
import hashlib

# Django Imports

# Third-Party Imports
from decouple import config

# Project-Specific Imports

# Relative Import


class MicroserviceTokenGenerator:
    """This class provides a method to generate a hashed token using HMAC algorithm."""

    @classmethod
    def generate_token(cls):
        """
        Generates a token and hashed token using HMAC algorithm.

        Returns:
            str: The hashed token.
        """
        try:
            # Retrieve secret key from configuration
            secret_key = config("MICROSERVICE_SECRET_KEY")
            if not secret_key:
                raise ValueError(
                    "Invalid configuration: MICROSERVICE_SECRET_KEY is not set"
                )

            # Use HMAC algorithm to create a token based on the secret key
            hashed_token = hmac.new(
                secret_key.encode(), None, hashlib.sha256
            ).hexdigest()
            return hashed_token
        except Exception as e:
            raise RuntimeError("Error occurred while generating token") from e
