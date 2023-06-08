from typing import *
from datetime import datetime
from functools import lru_cache

from fastapi import Body, FastAPI, UploadFile, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from models_mem import JobStatus, WorkerStatus, Job, Worker, File, QueueJob

from file_util import save_response_to_disk, save_to_disk
from master_handle import ( get_file_by_id, queue, init_queue, add_file, remove_file, add_job,
    transmit_file, get_file_url_by_id, get_job_by_id, get_file_url_by_queuejob,
    assign_job, get_worker_by_id, get_worker_by_ip, is_file_exist, add_worker
)


from config import Settings
from config import python_dir, project_root_path, static_path, favicon_path, templates_path
from log_util import log

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
    return templates.TemplateResponse("index_test.html", {"request": request})

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

        myfile = File(url=write_url, filename=file.filename)
        if not queue:
            init_queue(settings.DEFAULT_QUEUE_CAPACITY)
        if is_file_exist(myfile):
            return {
                "status": 1,
                "msg": f"Video file {file.filename} exists"
            }
        myfile = add_file(myfile)
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

@app.post("/worker_heartbeat")
async def worker_heartbeat(request: Request, settings: Annotated[Settings, Depends(get_settings)]):
    heartbeat = await request.json()
    worker_ip = heartbeat['worker_ip']
    worker_port = heartbeat['worker_port']
    status = heartbeat['status']
    processing_filename = heartbeat['processing_filename']
    msg = heartbeat['msg']
    worker = get_worker_by_ip(worker_ip)

    if not worker:
        worker = add_worker(worker_ip, worker_port)
    worker.status = WorkerStatus(status)
    worker.heartbeat_time = datetime.now()
    worker.heartbeat_msg = msg

    log(worker.cur_job_id)

    # deque next job
    if worker.status == WorkerStatus.IDLE:
        qj = assign_job(worker)
        if qj:
            log('Job assigned, file url =' + get_file_url_by_queuejob(qj))
    elif worker.status == WorkerStatus.COMPLETE:
        response = requests.get(f'http://{worker_ip}:{worker_port}/retrieve_file')
        j = get_job_by_id(worker.cur_job_id)
        f = get_file_by_id(j.input_file_id)
        j.output_file_id = f.filename

        save_response_to_disk(response.content, settings.PROCESSED_VID_DIR, f.filename)
        worker.cur_job_id = None
