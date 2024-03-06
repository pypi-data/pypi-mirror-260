# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import
from ....base.endpoints.core import BaseEndpoint


class AuthPassEndpoint(BaseEndpoint):
    """Class for managing authentication endpoints."""

    def __init__(self, endpoint_config_manager):
        """Initialize the AuthPassEndpoint instance."""
        # Call the parent class's __init__ method directly
        BaseEndpoint.__init__(self, endpoint_config_manager)

    def get_endpoint(self):
        """Get the authentication endpoint."""
        return self.endpoint_config.auth_pass


class ValidateTokenEndpoint(BaseEndpoint):
    """Class for managing token validation endpoints."""

    def __init__(self, endpoint_config_manager):
        """Initialize the ValidateTokenEndpoint instance."""
        # Call the parent class's __init__ method directly
        BaseEndpoint.__init__(self, endpoint_config_manager)

    def get_endpoint(self):
        """Get the token validation endpoint."""
        return self.endpoint_config.validate_token


class HasPermEndpoint(BaseEndpoint):
    """Class for managing endpoints related to permission validation."""

    def __init__(self, endpoint_config_manager):
        """Initialize the HasPermEndpoint instance."""
        # Call the parent class's __init__ method directly
        BaseEndpoint.__init__(self, endpoint_config_manager)

    def get_endpoint(self):
        """Get the permission validation endpoint."""
        return self.endpoint_config.has_perm
