from datetime import timedelta
from typing import Union

from aws_cdk import Duration


def to_duration(time: Union[timedelta, Duration, int]):
    return (
        Duration.seconds(time.total_seconds()) if isinstance(time, timedelta) else
        Duration.seconds(time) if isinstance(time, int) else
        time if isinstance(time, Duration) else
        None
    )