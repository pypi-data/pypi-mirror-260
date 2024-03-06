# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import
from ..core.base import KeyDerivationBase, KeyGenerationUtility


class KeyValidation(KeyDerivationBase, KeyGenerationUtility):
    """
    Utility class for key validation.
    """

    @classmethod
    def validate_key(cls, request_id, received_key):
        """
        Validate a derived key against the provided parameters.
        """
        expected_key = cls.derive_key(
            request_id=request_id, secret_key=cls.get_secret_key()
        )
        return received_key == expected_key
