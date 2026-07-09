from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
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
def get_root():
    """
    Перенаправление на документацию /docs
    """
    return RedirectResponse("/docs")


class CPULoadType(str, Enum):
    instant = "instant"
    average = "average"


@app.get("/api/cpu/load", response_model=list[CPUMetricResponse])
def get_cpu_load(
    type: CPULoadType = CPULoadType.instant, db: Session = Depends(get_db)
):
    """
    Получить данные нагрузки процессора

    Возвращает массив объектов с полями:\n
        timestamp - строка, содержащая время в формате ISO8601\n
        value - значение нагрузки в %\n
    """
    handlers = {
        CPULoadType.instant: get_cpu_instant,
        CPULoadType.average: get_cpu_average,
    }

    return handlers[type](db)


@app.get("/api/cpu/stats", response_model=CPUStatsResponse)
def get_cpu_stats(threshold: float = 80, db: Session = Depends(get_db)):
    """
    Получить статистику о нагрузке процессора за последний час

    Возвращает объект с полями:\n
        min_load - минимальная нагрузка\n
        max_load - максимальная нагрузка\n
        avg_load - средняя нагрузка\n
        median_load - медианная нагрузка (меньше подвержена выпадам, чем усредненная)\n
        seconds_above_threshold - сколько секунд нагрузка превышала пороговое значение\n
    """
    return get_cpu_load_stats(db, threshold)


@app.delete("/api/db/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_database(db: Session = Depends(get_db)):
    """
    Очистить базу данных

    Удаляет из базы данных все записи позднее последнего часа
    """
    clear_db(db)
