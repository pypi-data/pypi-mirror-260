# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Import section |--->
# -------------------------------------------------------------------------------------------------------------------- #
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


# -------------------------------------------------------------------------------------------------------------------- #
# <---| * Class Definition |--->
# -------------------------------------------------------------------------------------------------------------------- #
class Credentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    username: str | None
    password: str | None
    client_id: str | None
    client_secret: str | None

    @staticmethod
    def init_none():
        return Credentials(**{
            'username': None,
            'password': None,
            'client_id': None,
            'client_secret': None
        })

    @staticmethod
    def from_environment():
        """

        :return: Credentials
        """

        return Credentials(**{
            'username': os.getenv('RYGHT_USERNAME', 'no_username'),
            'password': os.getenv('RYGHT_PASSWORD', 'no_password_found'),
            'client_id': os.getenv('RYGHT_CLIENT_ID', 'no_client_id_found'),
            'client_secret': os.getenv('RYGHT_CLIENT_SECRET', 'no_client_secret_found')
        })

# -------------------------------------------------------------------------------------------------------------------- #
