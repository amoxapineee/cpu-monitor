from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from enum import Enum

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.clear_database import clear_db
from backend.database import get_db
from backend.fetch_database import get_cpu_average, get_cpu_instant, get_cpu_load_stats
from backend.metric_collector import collect_cpu_metrics
from backend.schemas import CPUMetricResponse, CPUStatsResponse


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


@app.get("/")
def root():
    return {
        "message": "cpu monitoring is running",
        "cpu_load": 'GET /api/cpu/load[?type="instant|average"]',
        "cpu_load_stats": "GET /api/cpu/stats",
        "clear_db": 'DELETE /api/db/clear[?type="all|keep_last_hour"',
    }


class CPULoadType(str, Enum):
    instant = "instant"
    average = "average"


@app.get("/api/cpu/load", response_model=list[CPUMetricResponse])
def get_cpu_load(
    type: CPULoadType = CPULoadType.instant, db: Session = Depends(get_db)
):
    handlers = {
        CPULoadType.instant: get_cpu_instant,
        CPULoadType.average: get_cpu_average,
    }

    return handlers[type](db)


@app.get("/api/cpu/stats", response_model=CPUStatsResponse)
def get_cpu_stats(treshold: float = 80, db: Session = Depends(get_db)):
    return get_cpu_load_stats(db, treshold)


class DBClearMode(str, Enum):
    all = "all"
    keep_last_hour = "keep_last_hour"


@app.delete("/api/db/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_database(
    mode: DBClearMode = DBClearMode.keep_last_hour, db: Session = Depends(get_db)
):
    modes = {
        DBClearMode.all: datetime.now(),
        DBClearMode.keep_last_hour: datetime.now() - timedelta(hours=1),
    }

    clear_db(db, modes[mode])
