# app/api/endpoints/telemetry.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse, TelemetryStats
from app.services import telemetry_service

router = APIRouter(prefix="/devices/{device_id}/telemetry", tags=["Telemetry"])


@router.post("", response_model=TelemetryResponse, status_code=201)
def ingest_telemetry(
    device_id: int,
    data: TelemetryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return telemetry_service.add_telemetry(db, device_id, current_user.id, data)


@router.get("", response_model=List[TelemetryResponse])
def get_telemetry(
    device_id: int,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return telemetry_service.get_telemetry(
        db, device_id, current_user.id, start_time, end_time, limit
    )


@router.get("/stats", response_model=TelemetryStats)
def get_stats(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return telemetry_service.get_telemetry_stats(db, device_id, current_user.id)