from enum import Enum
from datetime import datetime

class JobStatus(Enum):
    UNASSIGNED = 0
    ASSIGNED_PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAIL = 4

class WorkerStatus(Enum):
    IDLE = 0
    RUNNING = 1
    FAIL = 2
    COMPLETE = 3

class User():
    __tablename__ = "users"
    _serial_id = 0

    def __init__(self):
        self.id = User._serial_id
        User._serial_id += 1


class File():
    __tablename__ = "files"
    _serial_id = 0

    def __init__(self, url="", filename="", hash="", is_active=True):
        self.id = File._serial_id
        File._serial_id += 1
        self.url = url
        self.filename = filename
        if hash:
            self.hash = hash
        elif url:
            self.hash = self.generate_hash(url)
        self.is_active = is_active

    def generate_hash(self, url):
        return url # TODO: change logic to calculate md5 hash


class Job():
    __tablename__ = "jobs"
    _serial_id = 0

    def __init__(self, status=JobStatus.UNASSIGNED, file_name='', input_file_id=None, output_file_id=None, frame_rate="25", num_frames=0,
                 duration=0.0, user_id=None, worker_id=None, created_time=None, process_start_time=None,
                 process_end_time=None):
        self.id = Job._serial_id
        Job._serial_id += 1
        self.status = status
        self.file_name = file_name
        self.input_file_id = input_file_id # Foreign key file id
        self.output_file_id = output_file_id # Foreign key file id
        self.frame_rate = frame_rate
        self.num_frames = num_frames
        self.duration = duration
        self.user_id = user_id
        self.worker_id = worker_id # Foreign key worker id
        self.created_time = created_time # datetime object
        self.process_start_time = process_start_time # datetime object
        self.process_end_time = process_end_time # datetime object


class QueueJob():
    __tablename__ = "queuejobs"

    def __init__(self, job_id=None, video_link="", enqueue_time=None):
        self.job_id = job_id # ForeignKey(Job.id)
        self.video_link = video_link
        self.enqueue_time = enqueue_time # datetime object


class Worker():
    __tablename__ = "workers"
    _serial_id = 0

    def __init__(self, status=WorkerStatus.IDLE, worker_ip="", worker_port=3000, master_ip="", master_port=8000, started_time=None,
                 heartbeat_time=None, heartbeat_msg=""):
        self.id = Worker._serial_id
        Worker._serial_id += 1
        self.status = status
        self.worker_ip = worker_ip
        self.worker_port = worker_port
        self.master_ip = master_ip
        self.worker_port = master_port
        self.cur_job_id = None # ForeignKey("jobs.id")
        self.started_time = started_time
        self.heartbeat_time = heartbeat_time
        self.heartbeat_msg = heartbeat_msg
