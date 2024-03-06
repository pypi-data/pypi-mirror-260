# Python Imports
from typing import Optional

# Django Imports

# Third-Party Imports

# Project-Specific Imports
from platform_microservices_utils.security.core.base import (
    KeyDerivationBase,
    KeyGenerationUtility,
)

# Relative Import


class KeyDerivation(KeyDerivationBase, KeyGenerationUtility):
    """
    Utility class for key derivation using PBKDF2.
    """

    @classmethod
    def generate_key(cls, request_id: Optional[str]) -> str:
        """Derive a key using PBKDF2."""
        secret_key = cls.get_secret_key()
        if request_id:
            return cls.derive_key(secret_key=secret_key, request_id=request_id)
        return cls.derive_key(secret_key=secret_key, request_id=cls.get_request_id())
