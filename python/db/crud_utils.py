from sqlalchemy.orm import Session
from .models import User, File, Job, QueueJob, Worker
from .schemas import UserCreate, FileCreate, JobCreate, QueueJobCreate, WorkerCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_file(db: Session, file: FileCreate):
    db_file = File(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()


def create_job(db: Session, job: JobCreate):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def create_queue_job(db: Session, queue_job: QueueJobCreate):
    db_queue_job = QueueJob(**queue_job.dict())
    db.add(db_queue_job)
    db.commit()
    db.refresh(db_queue_job)
    return db_queue_job


def get_queue_job(db: Session, queue_job_id: int):
    return db.query(QueueJob).filter(QueueJob.job_id == queue_job_id).first()


def create_worker(db: Session, worker: WorkerCreate):
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def get_worker(db: Session, worker_id: int):
    return db.query(Worker).filter(Worker.id == worker_id).first()









    
    