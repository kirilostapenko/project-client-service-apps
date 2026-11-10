import uuid
import threading
import time

JOBS_DB = {}

def create_background_job(data=None):
    job_id = str(uuid.uuid4())
    JOBS_DB[job_id] = {"status": "pending", "data": data}
    thread = threading.Thread(target=process_job, args=(job_id,))
    thread.daemon = True
    thread.start()
    
    return job_id

def process_job(job_id):
    JOBS_DB[job_id]["status"] = "processing"
    time.sleep(3) 
    JOBS_DB[job_id]["status"] = "done"

def get_job_status(job_id):
    job = JOBS_DB.get(job_id)
    if not job:
        return None
    return job["status"]

def update_job_status(job_id, status):
    if job_id in JOBS_DB:
        JOBS_DB[job_id]["status"] = status