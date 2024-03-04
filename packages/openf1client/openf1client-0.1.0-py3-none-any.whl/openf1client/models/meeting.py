from pydantic import BaseModel


class Meeting(BaseModel):
    circuit_key: int
    circuit_short_name: str
    country_code: str
    country_key: int
    country_name: str
    date_start: str
    gmt_offset: str
    location: str
    meeting_key: int
    meeting_name: str
    meeting_official_name: str
    year: int
