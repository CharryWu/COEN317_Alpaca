from typing import *
from datetime import datetime
from functools import lru_cache

from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models_mem import JobStatus, WorkerStatus, Job, Worker, File, QueueJob

from file_util import save_to_disk
from master_handle import ( queue, init_queue, add_file, remove_file, add_job,
    transmit_file, get_file_url_by_id, get_job_with_id, get_file_url_with_queuejob,
    assign_job,
)


from config import Settings
from config import python_dir, project_root_path, static_path, favicon_path, templates_path


app = FastAPI()
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(templates_path)

@lru_cache()
def get_settings():
    return Settings()

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
    try:
        write_url = await save_to_disk(
            file, settings.ORIGINAL_VID_DIR, file.filename, settings.WRITE_CHUNK_SIZE
        )

        myfile = File(write_url)
        if not queue:
            init_queue(settings.DEFAULT_QUEUE_CAPACITY)
        queuejob = add_job(myfile)

        return {
            "status": 0,
            "msg": f"Upload Success! QueueJob(id={queuejob.job_id}) created"
        }
    except Exception as e:
        return {
            "status": 1,
            "msg": str(e)
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
