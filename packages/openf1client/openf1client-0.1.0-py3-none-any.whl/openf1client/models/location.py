from pydantic import BaseModel


class Location(BaseModel):
    date: str
    driver_number: int
    meeting_key: int
    session_key: int
    x: float
    y: float
    z: float
