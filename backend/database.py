from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class CPUMetric(Base):
    __tablename__ = "cpu_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[str] = mapped_column(nullable=False, index=True)
    value: Mapped[float] = mapped_column(nullable=False)


data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(exist_ok=True)
print(data_dir)

engine = create_engine(
    f"sqlite:///{data_dir}/metrics.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
