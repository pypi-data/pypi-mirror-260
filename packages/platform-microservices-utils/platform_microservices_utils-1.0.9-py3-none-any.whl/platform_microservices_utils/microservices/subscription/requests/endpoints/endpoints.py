# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import
from ....base.endpoints.core import BaseEndpoint


class IsSubscribedEndpoint(BaseEndpoint):
    """Class for managing subscription status endpoints."""

    def __init__(self, endpoint_config_manager):
        """Initialize the IsSubscribedEndpoint instance."""        
        BaseEndpoint.__init__(self, endpoint_config_manager)

    def get_endpoint(self):
        """Get the subscription status endpoint."""        
        return self.endpoint_config.is_subscribed

class IncreaseUsageEndpoint(BaseEndpoint):
    """Class for managing subscription status endpoints."""

    def __init__(self, endpoint_config_manager):
        """Initialize the IsSubscribedEndpoint instance."""        
        BaseEndpoint.__init__(self, endpoint_config_manager)

    def get_endpoint(self):
        """Get the subscription status endpoint."""        
        return self.endpoint_config.increase_usage_count


class EndpointIdEndpoint(BaseEndpoint):
    """Class for managing subscription status endpoints."""

    def __init__(self, endpoint_config_manager):
        """Initialize the IsSubscribedEndpoint instance."""        
        BaseEndpoint.__init__(self, endpoint_config_manager)

    def get_endpoint(self):
        """Get the subscription status endpoint."""        
        return self.endpoint_config.increase_usage_count

