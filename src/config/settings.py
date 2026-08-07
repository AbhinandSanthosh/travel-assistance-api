from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_env: str
    debug: bool

    host: str
    port: int

    database_url: str
    secret_key: str
    access_token_expire_minutes: int

    redis_url: str = "redis://localhost:6379/0"


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()