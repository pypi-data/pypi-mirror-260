from typing import Optional, Union
from pydantic import BaseModel


class Driver(BaseModel):
    broadcast_name: str
    country_code: Optional[str]
    driver_number: int
    first_name: Optional[str]
    full_name: str
    headshot_url: Optional[str]
    last_name: Optional[str]
    meeting_key: int
    name_acronym: str
    session_key: int
    team_colour: Optional[Union[str, float]]
    team_name: Optional[str]
