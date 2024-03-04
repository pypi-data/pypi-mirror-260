from pydantic import BaseModel


class Stint(BaseModel):
    # TODO: This should be an enum
    compound: str
    driver_number: int
    lap_end: int
    lap_start: int
    meeting_key: int
    session_key: int
    stint_number: int
    tyre_age_at_start: int
