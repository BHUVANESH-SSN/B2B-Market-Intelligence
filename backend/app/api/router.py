from fastapi import APIRouter

from app.api.routes import analysis, auth, competitors, health, insights, jobs, reports


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(competitors.router, prefix="/competitors", tags=["competitors"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
