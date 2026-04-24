# app/schemas/device.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeviceCreate(BaseModel):
    name: str
    device_type: str
    location: Optional[str] = None
    description: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    device_type: str
    location: Optional[str]
    description: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes":  True}