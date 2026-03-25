from __future__ import annotations

from app.db.session import SessionLocal
from app.db.models.enums import JobStatus
from app.services.analysis_pipeline import process_analysis_job
from app.services.redis_state import set_job_status
from app.workers.celery_app import celery_app


@celery_app.task(name="healthcheck.ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


@celery_app.task(name="analysis.run_market_analysis")
def run_market_analysis(job_id: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        result = process_analysis_job(db, job_id)
        return {"job_id": job_id, "report_id": result["report_id"]}
    except Exception as exc:
        from app.db.crud.job import get_job

        job = get_job(db, job_id=job_id)
        if job is not None:
            job.status = JobStatus.FAILED.value
            job.progress = 100
            job.step = "failed"
            job.error = str(exc)[:500]
            db.add(job)
            db.commit()
            set_job_status(job_id, status=job.status, progress=job.progress, step=job.step, extra={"error": job.error})
        raise
    finally:
        db.close()
