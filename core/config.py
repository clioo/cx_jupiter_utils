from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    LANDING_PROD_DRIVER: str
    LANDING_PROD_SERVER: str
    LANDING_PROD_DATABASE: str
    LANDING_PROD_UID: str
    LANDING_PROD_PWD: str

    LANDING_QA_DRIVER: str
    LANDING_QA_SERVER: str
    LANDING_QA_DATABASE: str
    LANDING_QA_UID: str
    LANDING_QA_PWD: str

    RMX_QA_DRIVER: str
    RMX_QA_SERVER: str
    RMX_QA_DATABASE: str
    RMX_QA_UID: str
    RMX_QA_PWD: str
    RMX_DECOUPLED_QA_DRIVER: str
    RMX_DECOUPLED_QA_SERVER: str
    RMX_DECOUPLED_QA_DATABASE: str
    RMX_DECOUPLED_QA_UID: str
    RMX_DECOUPLED_QA_PWD: str

    class Config:
        env_file = ".env"


APP_VERSION = '0.1.0'


@lru_cache()
def get_settings():
    """Using cache to avoid multiple initializations."""
    return Settings()
