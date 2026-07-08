from datetime import datetime

from pydantic import BaseModel, Field


class CPUStatsResponse(BaseModel):
    min_load: float
    max_load: float
    avg_load: float
    median_load: float
    seconds_above_threshold: int


class CPUMetricResponse(BaseModel):
    timestamp: datetime = Field(..., examples=["2026-07-06T00:44:49"])
    value: float | None = Field(None, examples=[89.49, 9.0])
