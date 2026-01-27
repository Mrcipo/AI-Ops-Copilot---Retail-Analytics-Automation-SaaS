import logging

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .core.config import settings
from .db import get_db


def configure_logging() -> None:
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


configure_logging()
logger = logging.getLogger("api")

app = FastAPI(title="AI Ops Copilot API")


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Starting API (env=%s)", settings.app_env)


@app.get("/api/v1/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/api/v1/db/ping")
def db_ping(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
