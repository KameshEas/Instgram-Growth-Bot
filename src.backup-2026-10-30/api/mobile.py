from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import uuid4
from datetime import datetime
import json
import asyncio

from src.database.connection import async_session
from src.models.database import MobileJob
from src.agents.orchestrator import ContentOrchestratorAgent

router = APIRouter()

# Simple request/response models
class GenerateRequest(BaseModel):
    task: str
    params: Optional[dict] = {}

class JobResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# Orchestrator will be set at app startup to allow using the real bot instance
ORCHESTRATOR = None

def set_orchestrator(orchestrator: ContentOrchestratorAgent):
    global ORCHESTRATOR
    ORCHESTRATOR = orchestrator

async def _process_job(job_id: str):
    """Background job worker: execute orchestrator and update DB."""
    async with async_session() as session:
        # load job
            job = await session.get(MobileJob, job_id)
            if not job:
            return

        job.started_at = datetime.utcnow()
        job.status = "running"
        session.add(job)
        await session.commit()

        try:
            # Input data frame for orchestrator
            input_data = {}
            try:
                input_data = json.loads(job.params) if job.params else {}
            except Exception:
                input_data = {"raw": job.params}

            # Add a command field from task (if not already present)
            if input_data.get("command") is None:
                input_data["command"] = job.task

            # Ensure orchestrator is available
            if ORCHESTRATOR is None:
                raise RuntimeError("Orchestrator not configured for mobile API")
            # Run orchestrator
            result = await ORCHESTRATOR.execute(input_data)

            job.result = json.dumps(result)
            job.status = "done"
            job.completed_at = datetime.utcnow()
            session.add(job)
            await session.commit()
        except Exception as e:
            job.error = str(e)
            job.status = "failed"
            job.completed_at = datetime.utcnow()
            session.add(job)
            await session.commit()


@router.post("/generate", response_model=JobResponse)
async def mobile_generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    """Create a mobile generation job and run it in background."""
    job_id = str(uuid4())
    job = MobileJob(
        job_id=job_id,
        task=req.task,
        params=json.dumps(req.params or {}),
        status="queued",
    )
    async with async_session() as session:
        session.add(job)
        await session.commit()

    # schedule background processing
    loop = asyncio.get_running_loop()
    loop.create_task(_process_job(job_id))

    return {"job_id": job_id}


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def mobile_status(job_id: str):
    async with async_session() as session:
        job = await session.get(MobileJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        result = None
        try:
            result = json.loads(job.result) if job.result else None
        except Exception:
            result = job.result

        return JobStatusResponse(
            job_id=job.job_id,
            status=job.status,
            result=result,
            error=job.error,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
        )


@router.get("/jobs", response_model=List[JobStatusResponse])
async def mobile_list_jobs(limit: int = 50):
    async with async_session() as session:
        q = await session.execute("SELECT * FROM mobile_jobs ORDER BY created_at DESC LIMIT :limit", {"limit": limit})
        rows = q.fetchall()
        out = []
        for r in rows:
            # r is a Row object; map to model fields
            rec = r._asdict()
            try:
                res = json.loads(rec.get("result")) if rec.get("result") else None
            except Exception:
                res = rec.get("result")
            out.append(JobStatusResponse(
                job_id=rec.get("job_id"),
                status=rec.get("status"),
                result=res,
                error=rec.get("error"),
                created_at=rec.get("created_at"),
                started_at=rec.get("started_at"),
                completed_at=rec.get("completed_at"),
            ))
        return out


@router.get("/health")
async def mobile_health():
    return {"status": "healthy", "source": "mobile-api"}
