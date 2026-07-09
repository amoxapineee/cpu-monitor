from datetime import UTC, datetime, timedelta
from statistics import mean, median

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from backend.database import CPUMetric
from backend.schemas import CPUStatsResponse
from backend.util import build_series, floor_datetime


def get_cpu_instant(db: Session):
    current_time = floor_datetime(datetime.now(UTC), 5)
    hour_ago = current_time - timedelta(hours=1)

    query = db.query(CPUMetric).filter(CPUMetric.timestamp > hour_ago.isoformat()).all()
    dict_query = {row.timestamp: row.value for row in query}

    return build_series(
        dict_query,
        hour_ago,
        current_time,
        timedelta(seconds=5),
    )


def get_cpu_average(db: Session):
    current_time = floor_datetime(datetime.now(UTC), 60)
    hour_ago = current_time - timedelta(hours=1)

    query = (
        db.query(
            func.strftime("%Y-%m-%dT%H:%M:00", CPUMetric.timestamp).label("minute"),
            func.round(func.avg(CPUMetric.value), 2).label("avg_value"),
        )
        .filter(CPUMetric.timestamp > hour_ago.isoformat())
        .group_by("minute")
        .all()
    )
    dict_query = {row[0]: row[1] for row in query}

    return build_series(
        dict_query,
        hour_ago,
        current_time,
        timedelta(minutes=1),
    )


def get_cpu_load_stats(db: Session, treshold: float = 80):
    current_time = floor_datetime(datetime.now(UTC), 60)
    hour_ago = current_time - timedelta(hours=1)

    query = (
        db.query(CPUMetric.value)
        .filter(CPUMetric.timestamp > hour_ago.isoformat())
        .all()
    )
    values = [row[0] for row in query]

    if not values:
        return CPUStatsResponse(
            min_load=0.0,
            max_load=0.0,
            avg_load=0.0,
            median_load=0.0,
            seconds_above_threshold=0,
        )

    return CPUStatsResponse(
        min_load=min(values),
        max_load=max(values),
        avg_load=round(mean(values), 2),
        median_load=round(median(values), 2),
        seconds_above_threshold=sum(5 for value in values if value > treshold),
    )
