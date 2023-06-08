from pathlib import Path
from typing import *
import requests
from functools import lru_cache
from fastapi import FastAPI, UploadFile, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi_utils.tasks import repeat_every
from config import Settings
from models_mem import WorkerStatus
from cv_util import draw_points_all
from file_util import remove_files_by_suffix, remove_files_in_dir, save_to_disk
from video_util import get_frame_rate, get_total_frames, images2video, video2images
from file_util import get_path
from worker_handle import process, worker_reset, processing_filename, processed_filename, failure
from log_util import log

app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()

@app.on_event("startup")
@repeat_every(seconds=10)  # 10
def heartbeat() -> None:
    try:
        settings = get_settings()
        msg = ""
        status = WorkerStatus.IDLE
        if processing_filename:
            if processed_filename:
                status = WorkerStatus.COMPLETE
            else:
                status = WorkerStatus.RUNNING
        if failure:
            status = WorkerStatus.FAIL
        log(f'heartbeat, status={status}')
        r = requests.post(f"http://{settings.MASTER_IP}:{str(settings.MASTER_PORT)}/worker_heartbeat", json={
            "worker_ip": settings.THIS_MACHINE_IP,
            "worker_port": settings.THIS_WORKER_MACHINE_PORT,
            "status": status.value,
            "processing_filename": processing_filename,
            "msg": msg
        })
    except Exception as e:
        log(e)
        log(r.json())

@app.post("/receive_file")
async def receive_file(file: UploadFile, settings: Annotated[Settings, Depends(get_settings)]):
    if processing_filename:
        return {
            "status": 1,
            "msg": "Worker not idle, can't take in new file"
        }

    try:
        write_url = await save_to_disk(
            file, settings.WORKER_DIR, file.filename, settings.WRITE_CHUNK_SIZE
        )
        process(write_url, file.filename)
    except Exception as e:
        print(e)
        return {
            "status": 11,
            "msg": "Worker failed with exception: " + str(e)
        }

    return {
        "status": 0,
        "msg": f"Worker successfully processed {file.filename}"
    }

@app.get("/retrieve_file", response_class=FileResponse)
async def retrieve_file(settings: Annotated[Settings, Depends(get_settings)]):
    if not processed_filename:
        return {
            "status": 1,
            "msg": f"Error: file is not ready"
        }
    if failure:
        return {
            "status": 11,
            "msg": f"Encounter Failure"
        }
    worker_reset()

    return get_path(settings.WORKER_DIR, processed_filename)


