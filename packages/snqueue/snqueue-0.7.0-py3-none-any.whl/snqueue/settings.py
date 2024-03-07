from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
  SNQUEUE_ENV: Literal['dev', 'prod'] = 'prod'

settings = Settings()