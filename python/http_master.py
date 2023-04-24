from typing import *

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI()

favicon_path = 'favicon.ico'

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/")
@app.get("/index")
@app.get("/home")
def home():
    """
    Homepage: Users can upload a video on this page
    Posts video as binary data to /uploadfile API
    If all worker machines are busy, tell users their job is pending
    """
    return {"Hello": "World"}

@app.get("/dashboard")
def dashboard():
    """
    Dashboard: Returns number of worker machines and their current job status
    """
    return "This is dashboard"

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    """
    """
    job_id = '' # to be generated
    start_time = datetime()
    return {"filename": file.filename, "job_id": job_id, start_time: str(start_time)}

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
