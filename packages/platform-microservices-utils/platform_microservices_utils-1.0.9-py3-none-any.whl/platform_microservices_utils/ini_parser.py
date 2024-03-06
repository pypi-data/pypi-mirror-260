# Python Imports
import configparser

# Third-Party Imports

# Django Imports

# Project-Specific Imports

# Relative Import


class EndpointConfig:
    """Class for mapping configuration settings from a file to attributes."""

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self._map_config()

    def _map_config(self):
        """Map configuration settings to attributes."""
        for section in self.config.sections():
            for key, value in self.config[section].items():
                setattr(self, key.lower(), value)


endpoint_config = EndpointConfig("microservices.ini")
