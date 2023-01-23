from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_URL: str

    REDIS_PORT: int = 6379

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
