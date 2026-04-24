# app/services/device_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


def create_device(db: Session, device_data: DeviceCreate, owner_id: int) -> Device:
    device = Device(**device_data.model_dump(), owner_id=owner_id)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_devices(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Device]:
    return db.query(Device).filter(Device.owner_id == owner_id).offset(skip).limit(limit).all()


def get_device(db: Session, device_id: int, owner_id: int) -> Device:
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.owner_id == owner_id
    ).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device


def update_device(db: Session, device_id: int, owner_id: int, updates: DeviceUpdate) -> Device:
    device = get_device(db, device_id, owner_id)
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int, owner_id: int) -> None:
    device = get_device(db, device_id, owner_id)
    db.delete(device)
    db.commit()