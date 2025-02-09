from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_URI: SecretStr
    SECRET_KEY: SecretStr
    ALGORITHM: SecretStr
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY.get_secret_value(), "algorithm": settings.ALGORITHM.get_secret_value()}