import os
from os.path import dirname, realpath, dirname, join
from functools import lru_cache
from typing import *
from pathlib import Path

from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import aiofiles

from datetime import datetime
from .config import Settings

from pathlib import Path

python_dir = dirname(realpath(__file__)) # python folder
project_root_path = dirname(python_dir) # project root
static_path = join(python_dir, 'static')
favicon_path = join(python_dir, 'favicon.ico')
templates_path = join(python_dir, 'templates')
print(static_path)

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(templates_path)

@lru_cache()
def get_settings():
    s = Settings()
    if not os.path.isabs(s.ORIGINAL_VID_DIR):
        s.ORIGINAL_VID_DIR = Path(s.ORIGINAL_VID_DIR).resolve()
    if not os.path.isabs(s.PROCESSED_VID_DIR):
        s.PROCESSED_VID_DIR = Path(s.PROCESSED_VID_DIR).resolve()

    return s

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """
    Homepage: Users can upload a video on this page
    Posts video as binary data to /uploadfile API
    If all worker machines are busy, tell users their job is pending
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
def dashboard():
    """
    Dashboard: Returns number of worker machines and their current job status
    """
    return "This is dashboard"

@app.post("/upload_file")
async def upload_file(file: UploadFile, settings: Annotated[Settings, Depends(get_settings)]):
    """
    """
    async with aiofiles.open(os.path.join(settings.ORIGINAL_VID_DIR, file.filename), 'wb') as out_file:
        while content := await file.read(settings.WRITE_CHUNK_SIZE):  # async read chunk
            await out_file.write(content)  # async write chunk

    job_id = '' # to be generated
    start_time = datetime.now()
    return {
        "filename": file.filename,
        "job_id": job_id,
        "start_time": str(start_time)
    }

@app.post("/job_status/{job_id}")
async def job_status(job_id: int):
    """
    Returns status of job_id, -1 if job_id does not exist
    """
    if job_id: # check if job id exosts
        # if job_id is not assigned, return pending
        # if job_id assigned, get worker_id and check status with (worker_id, job_id)
        ...
    return -1 # Return job id not foud
