from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from backend.database import CPUMetric
from backend.util import build_series, floor_datetime


def get_cpu_instant(db: Session):
    current_time = floor_datetime(datetime.now(), 5)
    hour_ago = current_time - timedelta(hours=1)

    query = db.query(CPUMetric).filter(CPUMetric.timestamp > hour_ago.isoformat()).all()
    dict_query = {m.timestamp: m.value for m in query}

    return build_series(
        dict_query,
        hour_ago,
        current_time,
        timedelta(seconds=5),
    )


def get_cpu_average(db: Session):
    current_time = floor_datetime(datetime.now(), 60)
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
    # query - список кортежей, 0 - строка minute, 1 - значение avg_load
    dict_query = {m[0]: m[1] for m in query}

    return build_series(
        dict_query,
        hour_ago,
        current_time,
        timedelta(minutes=1),
    )
