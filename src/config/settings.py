from typing import List


from pydantic import (
    AnyHttpUrl,
    BaseSettings
)


class Settings(BaseSettings):

    server_host: str
    server_port: int
    
    origins: List[AnyHttpUrl] = ['http://0.0.0.0:8000']

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'



