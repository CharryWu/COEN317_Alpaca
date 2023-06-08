from datetime import datetime
from functools import lru_cache
import requests
from models_mem import JobStatus, WorkerStatus, Job, Worker, File, QueueJob
from queue_utils import CircularQueue
from log_util import log, bcolors
from video_util import get_frame_rate, get_total_frames, get_duration
from config import Settings

files = []
jobs = []
workers = []
queue = None

@lru_cache()
def get_settings():
    return Settings()

def init_queue(capacity):
    global queue
    queue = CircularQueue(capacity)

def add_file(file: File):
    found = False
    for f in files:
        if f.url == file.url:
            found = True
    if not found:
        files.append(file)
    else:
        log(f'File {file.url} already exists', bcolors.WARNING)

def remove_file(url: str):
    for i, f in enumerate(files):
        if f.url == url:
            idx = i
    if idx >= 0:
        files.remove(idx)
    else:
        log(f'File {url} already exists', bcolors.WARNING)

def get_file_url_by_id(fid: str) -> str:
    for f in files:
        if f.id == fid:
            return f.url
    return None

def get_job_with_id(id: str) -> Job:
    for job in jobs:
        if job.id == id:
            return job
    return None

def get_worker_with_id(id: str) -> Worker:
    for worker in workers:
        if worker.id == id:
            return worker
    return None

def get_file_url_with_queuejob(qj: QueueJob) -> str:
    j = get_job_with_id(qj.job_id)
    if j:
        return get_file_url_by_id(j.input_file_id)
    return None


def add_job(file: File) -> QueueJob:
    """
    Init jobs and add to queue
    """
    if not queue:
        log('Error: Queue has not been initialized. Stop.')
        return
    j, qj = None, None
    try:
        now = datetime.now()
        j = Job(
            input_file_id=file.id,
            frame_rate=get_frame_rate(file.url),
            num_frames=get_total_frames(file.url),
            duration=get_duration(file.url),
            created_time=now,
        )
        qj = QueueJob(job_id=j.id, enqueue_time=now)
        return qj
    except Exception as e:
        log(e, bcolors.WARNING)

    if j and qj and not queue.isFull():
        jobs.append(j)
        queue.enqueue(qj)
    return qj


def assign_job(worker: Worker) -> QueueJob:
    """
    Assign a job to worker once the worker sends an "idle" heartbeat message
    """
    global queue
    if not queue or queue.isEmpty():
        return None
    qj = None
    try:
        qj = queue.get_front()
        j = get_job_with_id(qj.job_id)
        if not j:
            return None
        ## Transmit file to worker over network
        url = get_file_url_by_id(j.input_file_id)
        if not url:
            return None
        transmit_file(worker, url)
        queue.dequeue()
        j.worker_id = worker.id
        j.status = JobStatus.ASSIGNED_PENDING
        worker.cur_job_id = j.id
    except Exception as e:
        log(e, bcolors.WARNING)
        return None
    return qj

def transmit_file(worker: Worker, video_url: str) -> bool:
    try:
        with open(video_url) as vid:
            requests.post(f"{worker.worker_ip}:{str(Settings.DEFAULT_WORKER_PORT)}/receive_file", files={'video': vid})
        return True
    except Exception as e:
        log(e, bcolors.WARNING)
        return False