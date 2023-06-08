from pydantic import BaseSettings
from pathlib import Path
from os.path import dirname, realpath, dirname, join, isabs

python_dir = dirname(realpath(__file__)) # python folder
project_root_path = dirname(python_dir) # project root
static_path = join(python_dir, 'static')
favicon_path = join(python_dir, 'favicon.ico')
templates_path = join(python_dir, 'templates')

class Settings(BaseSettings):
    ORIGINAL_VID_DIR: str
    PROCESSED_VID_DIR: str
    DEFAULT_QUEUE_CAPACITY = 1024
    WRITE_CHUNK_SIZE:int = 8192

    DEFAULT_MASTER_PORT = 8000
    DEFAULT_WORKER_PORT = 8000

    class Config:
        env_file = join(project_root_path, ".env")

    def __init__(self):
        super().__init__()

        if not isabs(self.ORIGINAL_VID_DIR):
            self.ORIGINAL_VID_DIR = Path(self.ORIGINAL_VID_DIR).resolve()
        if not isabs(self.PROCESSED_VID_DIR):
            self.PROCESSED_VID_DIR = Path(self.PROCESSED_VID_DIR).resolve()