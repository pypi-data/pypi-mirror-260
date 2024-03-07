from typing import TypedDict


class Timings(TypedDict):
    total: float


class StreamTimings(TypedDict):
    avg: float
    first: float
    max: float
    min: float
    total: float
