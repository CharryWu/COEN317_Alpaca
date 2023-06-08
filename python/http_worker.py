from typing import *
from functools import lru_cache
from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from .config import Settings

app = FastAPI()

@lru_cache()
def get_settings():
    return Settings()

@app.post("/receive_file", response_class=HTMLResponse)
async def receive_file(file: UploadFile, settings: Annotated[Settings, Depends(get_settings)]):

    return None