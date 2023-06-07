from fastapi import FastAPI, Depends, HTTPException
from fastapi import Request
from sqlalchemy.orm import Session
from . import crud_utils, models, schemas

# from .models import User,File,Job,QueueJob,Worker
from .database import SessionLocal, engine
from .schemas import UserCreate, FileCreate, JobCreate, QueueJobCreate, WorkerCreate
from db.schemas import User,File,Job,QueueJob,Worker
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from config import python_dir, project_root_path, static_path, favicon_path, templates_path

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(templates_path)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
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



# Create operations
@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/files")
def create_file(file: File, db: Session = Depends(get_db)):
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


@app.post("/jobs")
def create_job(job: Job, db: Session = Depends(get_db)):
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@app.post("/queuejobs")
def create_queue_job(queue_job: QueueJob, db: Session = Depends(get_db)):
    db.add(queue_job)
    db.commit()
    db.refresh(queue_job)
    return queue_job


@app.post("/workers")
def create_worker(worker: Worker, db: Session = Depends(get_db)):
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


# Read operations
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/files")
def get_files(db: Session = Depends(get_db)):
    files = db.query(models.File).all()
    return files


@app.get("/jobs")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(Job.id == job_id).first()
    if job:
        return job
    else:
        raise HTTPException(status_code=404, detail="Job not found")


@app.get("/queuejobs")
def get_queue_jobs(db: Session = Depends(get_db)):
    queue_jobs = db.query(models.QueueJob).all()
    return queue_jobs


@app.get("/workers")
def get_workers(db: Session = Depends(get_db)):
    workers = db.query(models.Worker).all()
    return workers


# Update operations
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(User.id == user_id).first()
    if existing_user:
        existing_user.property = user.property  # Update the desired properties
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/files/{file_id}")
def update_file(file_id: int, file: File, db: Session = Depends(get_db)):
    existing_file = db.query(models.File).filter(File.id == file_id).first()
    if existing_file:
        existing_file.property = file.property  # Update the desired properties
        db.commit()
        db.refresh(existing_file)
        return existing_file
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.put("/jobs/{job_id}")
def update_job(job_id: int, job: Job, db: Session = Depends(get_db)):
    existing_job = db.query(models.Job).filter(Job.id == job_id).first()
    if existing_job:
        existing_job.property = job.property  # Update the desired properties
        db.commit()
        db.refresh(existing_job)
        return existing_job
    else:
        raise HTTPException(status_code=404, detail="Job not found")


@app.put("/queuejobs/{queue_job_id}")
def update_queue_job(queue_job_id: int, queue_job: QueueJob, db: Session = Depends(get_db)):
    existing_queue_job = db.query(models.QueueJob).filter(QueueJob.job_id == queue_job_id).first()
    if existing_queue_job:
        existing_queue_job.property = queue_job.property  # Update the desired properties
        db.commit()
        db.refresh(existing_queue_job)
        return existing_queue_job
    else:
        raise HTTPException(status_code=404, detail="Queue Job not found")


@app.put("/workers/{worker_id}")
def update_worker(worker_id: int, worker: Worker, db: Session = Depends(get_db)):
    existing_worker = db.query(models.Worker).filter(Worker.id == worker_id).first()
    if existing_worker:
        existing_worker.property = worker.property  # Update the desired properties
        db.commit()
        db.refresh(existing_worker)
        return existing_worker
    else:
        raise HTTPException(status_code=404, detail="Worker not found")


# Delete operations
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(models.File).filter(File.id == file_id).first()
    if file:
        db.delete(file)
        db.commit()
        return {"message": "File deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(Job.id == job_id).first()
    if job:
        db.delete(job)
        db.commit()
        return {"message": "Job deleted"}
    else:
        raise HTTPException(status_code=404, detail="Job not found")


@app.delete("/queuejobs/{queue_job_id}")
def delete_queue_job(queue_job_id: int, db: Session = Depends(get_db)):
    queue_job = db.query(models.QueueJob).filter(QueueJob.job_id == queue_job_id).first()
    if queue_job:
        db.delete(queue_job)
        db.commit()
        return {"message": "Queue Job deleted"}
    else:
        raise HTTPException(status_code=404, detail="Queue Job not found")


@app.delete("/workers/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(models.Worker).filter(Worker.id == worker_id).first()
    if worker:
        db.delete(worker)
        db.commit()
        return {"message": "Worker deleted"}
    else:
        raise HTTPException(status_code=404, detail="Worker not found")




models.Base.metadata.create_all(bind=engine)