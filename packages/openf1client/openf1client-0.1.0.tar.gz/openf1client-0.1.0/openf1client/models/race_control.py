from typing import Optional
from pydantic import BaseModel


class RaceControl(BaseModel):
    # TODO: This should be an enum
    category: str
    date: str
    driver_number: Optional[int]
    # TODO: This should be an enum
    flag: Optional[str]
    lap_number: Optional[int]
    meeting_key: int
    message: str
    # TODO: This should be an enum
    scope: Optional[str]
    sector: Optional[int]
    session_key: int
