from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base 
# from .schemas import UserSchema


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True) # Self-incrementing ID of file
    url = Column(String, unique=True, index=True) # url to file, could be linux file schema, or http schema
    hash = Column(String, unique=True) # md5 hash of file, used for checking duplication
    is_active = Column(Boolean, default=True) # if inactive, file is not accessible/visible


class Job(Base):
    """
    Job represents a single video to be processed.
    It has a status, a reference to the video file, as well as metadata of the video.
    """
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True) # Self-incrementing ID of job
    status = Column() # UNASSIGNED = 0, ASSIGNED_PENDING = 1, PROCESSING = 2, COMPLETED = 3, FAIL = 4
    input_file_id = Column(Integer, ForeignKey("files.id"))
    output_file_id = Column(Integer, ForeignKey("files.id"))
    frame_rate = Column(String) # Frame rate of video, stored as string to allow fractional frame rate (“25/1” and “25” represent the same frame rate)
    num_frames = Column(Integer) # Total number of frames of video
    duration = Column(Float) # Duration of video, in seconds
    user_id = Column(Integer, ForeignKey("users.id")) # Foreign Key to the user table. The user id who created the job. For MVP, all jobs have uid=1.
    worker_id = Column(Integer, ForeignKey("workers.id")) # Foreign Key to the assigned worker id. Null if job is pending assignment
    created_time = Column(DateTime) # Time when this job gets created
    process_start_time = Column(DateTime) # Time when a worker machine starts processing this job
    process_end_time = Column(DateTime) # Time when a worker machine fully processed this job


class QueueJob(Base):
    """
    Queue table dynamically maintains all jobs currently in the queue.
    New jobs are added to the table while completed/failed jobs are removed constantly.
    Upon failure, the rebooted master process can be re-instantiated from this queuejob table. It has the following schema:
    """
    __tablename__ = "queuejobs"

    job_id = Column(Integer, ForeignKey(Job.id), primary_key=True) # Id of the job in queue. Primary Key of this table, also Foreign Key to Job table
    video_link = Column(String) # Generated download link for processed vid. Null until processed vid is stored on master machine available for download
    enqueue_time = Column(DateTime) # Time when this job gets into the queue

class Worker(Base):
    """
    Worker is a table on **master machine** that tracks the status of each worker.
    It will be periodically updated by heartbeat messages sent from worker.
    The worker table has the following schema:
    """
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True) # Self-incrementing worker machine
    status = Column() # Idle=0, Running=1, Fail=2, Complete=3
    worker_ip = Column(String)
    masters_ip = Column(String)
    output_file_id = Column(Integer, ForeignKey("jobs.id"))
    started_time = Column(DateTime)
    heartbeat_time = Column(DateTime)
    # Message content of last heartbeat, in string JSON format.
    # Worker machine can use the heartbeat message to report any anomalies in machine conditions or job status. Useful for debug & analytics report
    heartbeat_msg = Column(String)


