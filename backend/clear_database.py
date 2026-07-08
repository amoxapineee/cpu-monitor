from datetime import datetime

from sqlalchemy.orm import Session

from backend.database import CPUMetric
from backend.util import floor_datetime


def clear_db(db: Session, time: datetime | None = None):
    if time is None:
        time = datetime.now()
    current_time = floor_datetime(time, 1)
    db.query(CPUMetric).filter(CPUMetric.timestamp <= current_time.isoformat()).delete()
    db.commit()
