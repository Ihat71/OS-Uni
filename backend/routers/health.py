"""
routers/health.py
Simple health-check endpoint — useful for verifying the server is alive.
"""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()


@router.get("/health", summary="Health check")
async def health():
    return {
        "status": "ok",
        "server_time_utc": datetime.now(timezone.utc).isoformat(),
        "project": "OS Interactive Web Portfolio",
    }
