from pydantic_settings import BaseSettings
from typing import List

from environs import Env

env = Env()
env.read_env()

class Settings(BaseSettings):
    APP_NAME: str = env.str('APP_NAME')
    ENVIRONMENT: str = env.str('ENVIRONMENT')

    PROXY_USER: str = env.str('PROXY_USER', '')
    PROXY_PWD: str = env.str('PROXY_PWD', '')
    PROXY_HOST: str = env.str('PROXY_HOST', '')
    PROXY_PORT: str = env.str('PROXY_PORT', '')

    AWS_ACCESS_KEY_ID: str = env.str('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = env.str('AWS_SECRET_ACCESS_KEY', '')

    OPENAI_API_KEY: str = env.str('OPENAI_API_KEY', '')


config = Settings()
