# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import Base, get_engine
from app.api.endpoints import auth, devices, telemetry


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates all database tables on startup
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(
    title="IoT Device Management API",
    description="Backend API for managing IoT devices and sensor telemetry.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(telemetry.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "iot-device-api"}