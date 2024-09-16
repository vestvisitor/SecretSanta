from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import computed_field


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT : int
    DB_NAME : str
    DB_USER : str
    DB_PASS : str

    DB_SQLITE_NAME: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"sqlite:///{self.DB_SQLITE_NAME}.db"

    SECRET_KEY : str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file="src/core/.env"
    )


settings = Settings()
