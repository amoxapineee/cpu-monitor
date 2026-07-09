from datetime import datetime

from backend.schemas import CPUMetricResponse


def floor_datetime(dt: datetime, divider) -> datetime:
    seconds = dt.second
    remainder = seconds % divider
    return dt.replace(second=seconds - remainder, microsecond=0, tzinfo=None)


def build_series(
    data_dict: dict[str, float], start_time, end_time, interval
) -> list[dict[str, None]]:
    series = list()
    current = start_time
    while current < end_time:
        series.append(
            CPUMetricResponse(
                timestamp=current.isoformat(),
                value=data_dict.get(current.isoformat()),
            )
        )
        current += interval
    return series
