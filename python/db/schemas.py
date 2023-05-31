from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FileBase(BaseModel):
    pass


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    url: str
    hash: str
    is_active: bool

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    pass


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    status: int
    input_file_id: int
    input_file: File
    output_file_id: int
    output_file: File
    frame_rate: str
    num_frames: int
    duration: float
    user_id: int
    created_time: datetime
    process_start_time: datetime
    process_end_time: datetime

    class Config:
        orm_mode = True


class QueueJobBase(BaseModel):
    pass


class QueueJobCreate(QueueJobBase):
    pass


class QueueJob(QueueJobBase):
    job_id: int
    video_link: str
    enqueue_time: datetime

    class Config:
        orm_mode = True


class WorkerBase(BaseModel):
    pass


class WorkerCreate(WorkerBase):
    pass


class Worker(WorkerBase):
    id: int
    status: int
    worker_ip: str
    masters_ip: str
    cur_job_id: Job
    started_time: datetime
    heartbeat_time: datetime
    heartbeat_msg: str

    class Config:
        orm_mode = True


