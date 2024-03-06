from decouple import config

class SecretKeyProvider:
    """
    Utility class to provide the microservice secret key.
    """

    @classmethod
    def get_secret_key(cls):
        """
        Retrieves the microservice secret key from the configuration.
        """
        return config("MICROSERVICE_SECRET_KEY")
