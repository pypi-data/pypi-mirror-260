from typing import Optional
from pydantic import BaseModel


class Interval(BaseModel):
    date: str
    driver_number: int
    gap_to_leader: Optional[float]
    interval: Optional[float]
    meeting_key: int
    session_key: int
