from typing import Optional
from pydantic import BaseModel


class Lap(BaseModel):
    date_start: Optional[str]
    driver_number: int
    duration_sector_1: Optional[float]
    duration_sector_2: Optional[float]
    duration_sector_3: Optional[float]
    i1_speed: Optional[int]
    i2_speed: Optional[int]
    is_pit_out_lap: bool
    lap_duration: Optional[float]
    lap_number: int
    meeting_key: int
    segments_sector_1: list[Optional[int]]
    segments_sector_2: list[Optional[int]]
    segments_sector_3: list[Optional[int]]
    session_key: int
    st_speed: Optional[int]
