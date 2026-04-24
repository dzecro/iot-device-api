# app/schemas/telemetry.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class TelemetryCreate(BaseModel):
    value: float
    unit: str
    timestamp: Optional[datetime] = None


class TelemetryResponse(BaseModel):
    id: int
    device_id: int
    value: float
    unit: str
    timestamp: datetime

    model_config = {"from_attributes": True}


class TelemetryStats(BaseModel):
    device_id: int
    count: int
    average: float
    minimum: float
    maximum: float
    unit: str
    