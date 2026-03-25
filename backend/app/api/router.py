from fastapi import APIRouter

from app.api.routes.analysis import router as analysis_router
from app.api.routes.auth import router as auth_router
from app.api.routes.competitors import router as competitors_router
from app.api.routes.health import router as health_router
from app.api.routes.insights import router as insights_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.reports import router as reports_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(competitors_router, prefix="/competitors", tags=["competitors"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
api_router.include_router(insights_router, prefix="/insights", tags=["insights"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(health_router, tags=["health"])
