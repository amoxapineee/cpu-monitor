from asyncio import to_thread
from datetime import UTC, datetime

from psutil import cpu_percent

from backend.database import CPUMetric, SessionLocal
from backend.util import floor_datetime


async def collect_cpu_metrics():
    while True:
        try:
            load_percent = await to_thread(cpu_percent, 5)
            timestamp = floor_datetime(datetime.now(UTC), 5).isoformat()

            db = SessionLocal()

            try:
                db.add(CPUMetric(timestamp=timestamp, value=load_percent))
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Ошибка записи в бд: {e}")
            finally:
                db.close()

        except Exception as e:
            print(f"Ошибка сбора метрики: {e}")
