from pydantic import BaseModel


class TeamRadio(BaseModel):
    date: str
    driver_number: int
    meeting_key: int
    recording_url: str
    session_key: int
