# IoT Device Management & Telemetry API

A production-grade REST API for managing connected IoT devices and ingesting
sensor telemetry data. Built with Python, FastAPI, PostgreSQL, and Docker.

![CI](https://github.com/dzecro/iot-device-api/actions/workflows/ci.yml/badge.svg)

---

## Architecture
 
```
Client → FastAPI (Port 8000) → Service Layer → SQLAlchemy ORM → PostgreSQL
                ↑
         JWT Auth Middleware
```
 
## Quick Start
 
**Requirements:** Docker Desktop, Git
 
```bash
git clone https://github.com/dzecro/iot-device-api.git
cd iot-device-api
docker compose up --build
```
 
Open http://localhost:8000/docs for the interactive API documentation.
 
## API Endpoints
 
### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Login and receive a JWT token |
 
### Devices
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/devices` | Register a new IoT device |
| GET | `/devices` | List all your devices |
| GET | `/devices/{id}` | Get a specific device |
| PATCH | `/devices/{id}` | Update device details |
| DELETE | `/devices/{id}` | Delete a device |
 
### Telemetry
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/devices/{id}/telemetry` | Submit a sensor reading |
| GET | `/devices/{id}/telemetry` | Query readings (time-filterable) |
| GET | `/devices/{id}/telemetry/stats` | Get avg, min, max, count |
 
## Authentication
 
All device and telemetry endpoints require a Bearer token:
```
Authorization: Bearer <your_jwt_token>
```
 
## Running Tests
 
```cmd
venv\Scripts\activate
pytest -v
```
 
## Tech Stack
 
- **FastAPI** — High-performance Python web framework
- **PostgreSQL** — Relational database for persistent storage
- **SQLAlchemy** — Python ORM for database interactions
- **Docker & Docker Compose** — Containerized deployment
- **JWT** — Stateless token-based authentication
- **Pytest** — Automated test suite
- **GitHub Actions** — CI pipeline
```
 
