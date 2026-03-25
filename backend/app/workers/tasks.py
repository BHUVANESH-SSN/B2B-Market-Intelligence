from app.services.analysis_pipeline import process_analysis_job
from app.workers.celery_app import celery_app


@celery_app.task(name="healthcheck.ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


@celery_app.task(name="analysis.run_market_analysis")
def run_market_analysis(job_id: str) -> dict[str, str]:
    result = process_analysis_job(job_id)
    return {"job_id": job_id, "report_id": result["report_id"]}
