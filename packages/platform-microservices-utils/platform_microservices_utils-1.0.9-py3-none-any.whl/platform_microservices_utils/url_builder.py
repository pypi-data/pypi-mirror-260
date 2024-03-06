# Python Imports
from enum import Enum

# Third-Party Imports
from decouple import config

# Django Imports

# Project-Specific Imports

# Relative Import


class MicroserviceEnv(Enum):
    """Enumeration for microservice environments."""

    PROD = "PROD"
    UAT = "UAT"


class MicroserviceConfig:
    """Class representing microservice configuration."""

    def __init__(self, env):
        self.env = env
        self.host = config(f"MICROSERVICE_{env}_HOST")
        self.port = config(f"MICROSERVICE_{env}_PORT")


class BuildUrl:
    """Class for constructing URLs based on microservice configuration."""

    @classmethod
    def construct_url(cls, endpoint):
        """Constructs a URL based on the specified endpoint."""
        microservice_env = config("MICROSERVICE_ENV")
        if microservice_env not in ("PROD", "UAT"):
            raise ValueError("Invalid MICROSERVICE_ENV value")

        microservice_config = MicroserviceConfig(microservice_env)
        if not microservice_config.host or not microservice_config.port:
            raise ValueError(f"Missing host or port for {microservice_env}")

        return (
            f"http://{microservice_config.host}:{microservice_config.port}/{endpoint}"
        )
