from datetime import datetime


def floor_datetime(dt: datetime, divider) -> datetime:
    seconds = dt.second
    remainder = seconds % divider
    return dt.replace(second=seconds - remainder, microsecond=0)


def build_series(
    data_dict: dict[str, float], start_time, end_time, interval
) -> list[dict[str, None]]:
    series = list()
    current = start_time
    while current < end_time:
        series.append(
            {
                "timestamp": current.isoformat(),
                "value": data_dict.get(current.isoformat()),
            }
        )
        current += interval
    return series
