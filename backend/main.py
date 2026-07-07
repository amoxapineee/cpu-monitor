from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.fetch_metric import get_cpu_average, get_cpu_instant
from backend.metric_collector import collect_cpu_metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = create_task(collect_cpu_metrics())

    yield

    task.cancel()
    try:
        await task
    except CancelledError:
        pass


app = FastAPI(title="CPU monitoring", lifespan=lifespan)

# Прослойка для разрешения кросс-доменных запросов при разработке
# Фронт (react) - http://localhost:5173/
# Бэк (python) - http://localhost:8000/
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CPUMetricResponse(BaseModel):
    timestamp: datetime = Field(..., examples=["2026-07-06T00:44:49"])
    value: float | None = Field(None, examples=[89.49, 9.0])


@app.get("/")
def root():
    return {
        "message": "cpu monitoring is running",
        "cpu_load": "/api/cpu",
    }


@app.get("/api/cpu/instant", response_model=list[CPUMetricResponse])
def get_cpu_load_instant(db: Session = Depends(get_db)):
    return get_cpu_instant(db)


@app.get("/api/cpu/average", response_model=list[CPUMetricResponse])
def get_cpu_load_average(db: Session = Depends(get_db)):
    return get_cpu_average(db)
