from pydantic import BaseSettings

class Settings(BaseSettings):
    ORIGINAL_VID_DIR: str
    PROCESSED_VID_DIR: str
    WRITE_CHUNK_SIZE:int = 8192
    class Config:
        env_file = "../.env"