# app/db/database.py
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base    -removed .ext declarative import (deprecated)
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

# Module-level variables — not created until get_engine() is called
_engine = None
_SessionLocal = None


def get_engine():
    """
    Creates the engine on first call only.
    Reads DATABASE_URL at call time, not at import time.
    This allows tests to set DATABASE_URL before the engine is created.
    """
    global _engine
    if _engine is None:
        database_url = os.environ.get("DATABASE_URL", "")
        if not database_url:
            from app.core.config import settings
            database_url = settings.DATABASE_URL

        connect_args = {}
        if database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        _engine = create_engine(database_url, connect_args=connect_args)
    return _engine


def get_session_local():
    """Creates the SessionLocal factory on first call only."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return _SessionLocal


def get_db():
    """
    Provides a database session for each request.
    Automatically closes the session when the request is done.
    """
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()