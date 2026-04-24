# app/services/telemetry_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional
from app.models.telemetry import Telemetry
from app.models.device import Device
from app.schemas.telemetry import TelemetryCreate, TelemetryStats


def _verify_ownership(db: Session, device_id: int, owner_id: int) -> Device:
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.owner_id == owner_id
    ).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device


def add_telemetry(db: Session, device_id: int, owner_id: int, data: TelemetryCreate) -> Telemetry:
    _verify_ownership(db, device_id, owner_id)
    kwargs = {"device_id": device_id, "value": data.value, "unit": data.unit}
    if data.timestamp:
        kwargs["timestamp"] = data.timestamp
    reading = Telemetry(**kwargs)
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


def get_telemetry(
    db: Session,
    device_id: int,
    owner_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100
) -> List[Telemetry]:
    _verify_ownership(db, device_id, owner_id)
    query = db.query(Telemetry).filter(Telemetry.device_id == device_id)
    if start_time:
        query = query.filter(Telemetry.timestamp >= start_time)
    if end_time:
        query = query.filter(Telemetry.timestamp <= end_time)
    return query.order_by(Telemetry.timestamp.desc()).limit(limit).all()


def get_telemetry_stats(db: Session, device_id: int, owner_id: int) -> TelemetryStats:
    _verify_ownership(db, device_id, owner_id)
    result = db.query(
        func.count(Telemetry.id).label("count"),
        func.avg(Telemetry.value).label("average"),
        func.min(Telemetry.value).label("minimum"),
        func.max(Telemetry.value).label("maximum"),
        Telemetry.unit
    ).filter(Telemetry.device_id == device_id).group_by(Telemetry.unit).first()

    if not result or result.count == 0:
        raise HTTPException(status_code=404, detail="No telemetry found for this device")

    return TelemetryStats(
        device_id=device_id,
        count=result.count,
        average=round(result.average, 2),
        minimum=result.minimum,
        maximum=result.maximum,
        unit=result.unit
    )