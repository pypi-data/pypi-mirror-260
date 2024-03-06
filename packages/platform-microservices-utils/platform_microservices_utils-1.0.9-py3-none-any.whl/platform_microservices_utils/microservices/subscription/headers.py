# Python Imports

# Django Imports

# Third-Party Imports

# Project-Specific Imports
from common_utils.logger import get_logger
from platform_microservices_utils.base.headers import HeaderBuilder

# Relative Import
from .properties import Identifiers

class MicroserviceAdminHeaders(HeaderBuilder):
    """A class for generating tenant db config headers."""

    logger = get_logger(__name__)

    def __init__(self,tenant_identifier=None):
        super().__init__(
            tenant_identifier=Identifiers.ADMIN_IDENTIFER,
            microservice_token=True,
            microservice_request_key=True,
            microservice_request_id=True,
        )
