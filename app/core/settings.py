from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    database_url: str

    secret_key: str

    algorithm: str

    access_token_expire_minutes: int

    redis_host: str

    redis_port: int

    class Config:

        env_file = ".env"


settings = Settings()