from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.database import CPUMetric
from backend.util import floor_datetime


def clear_db(db: Session):
    current_time = floor_datetime(datetime.now(), 1) - timedelta(hours=1)
    db.query(CPUMetric).filter(CPUMetric.timestamp <= current_time.isoformat()).delete()
    db.commit()
