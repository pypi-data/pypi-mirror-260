from pydantic import BaseModel


class Session(BaseModel):
    circuit_key: int
    circuit_short_name: str
    country_code: str
    country_key: int
    country_name: str
    date_end: str
    date_start: str
    gmt_offset: str
    location: str
    meeting_key: int
    session_key: int
    session_name: str
    # TODO: This should be an enum
    session_type: str
    year: int
