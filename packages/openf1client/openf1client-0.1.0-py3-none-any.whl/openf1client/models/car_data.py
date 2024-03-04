from pydantic import BaseModel


class CarData(BaseModel):
    brake: int
    date: str
    driver_number: int
    drs: int
    meeting_key: int
    n_gear: int
    rpm: int
    session_key: int
    speed: int
    throttle: int
