from pydantic import BaseModel


class Pit(BaseModel):
    date: str
    driver_number: int
    lap_number: int
    meeting_key: int
    pit_duration: float
    session_key: int
