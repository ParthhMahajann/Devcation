from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    tg_host: str = "http://127.0.0.1"
    tg_username: str = "tigergraph"
    tg_password: str = "tigergraph"
    tg_graph: str = "MedGraph"
    tg_restpp_port: str = "9000"
    tg_gs_port: str = "14240"
    tg_api_token: str = ""
    tg_secret: str = ""

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
