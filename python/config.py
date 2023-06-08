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
    WORKER_DIR: str
    MASTER_IP: str
    MASTER_PORT: int
    THIS_MACHINE_IP: str
    THIS_WORKER_MACHINE_PORT: int
    DEFAULT_QUEUE_CAPACITY = 1024
    WRITE_CHUNK_SIZE:int = 8192

    DEFAULT_MASTER_IP_ADDRESS = "127.0.0.1"
    DEFAULT_IP_ADDRESS = "127.0.0.1"
    DEFAULT_MASTER_PORT = 8000
    DEFAULT_WORKER_PORT = 3000

    class Config:
        env_file = join(project_root_path, ".env")

    def __init__(self):
        super().__init__()

        if not self.MASTER_IP:
            self.MASTER_IP = self.DEFAULT_MASTER_IP_ADDRESS
        if not self.THIS_MACHINE_IP:
            self.THIS_MACHINE_IP = self.DEFAULT_IP_ADDRESS
        if not self.MASTER_PORT:
            self.MASTER_PORT = self.DEFAULT_MASTER_PORT
        if not self.THIS_WORKER_MACHINE_PORT:
            self.THIS_WORKER_MACHINE_PORT = self.DEFAULT_WORKER_PORT

        if not isabs(self.ORIGINAL_VID_DIR):
            self.ORIGINAL_VID_DIR = Path(self.ORIGINAL_VID_DIR).resolve()
        if not isabs(self.PROCESSED_VID_DIR):
            self.PROCESSED_VID_DIR = Path(self.PROCESSED_VID_DIR).resolve()