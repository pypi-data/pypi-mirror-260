from pydantic import BaseModel


class Weather(BaseModel):
    air_temperature: float
    date: str
    humidity: int
    meeting_key: int
    pressure: float
    rainfall: int
    session_key: int
    track_temperature: float
    wind_direction: int
    wind_speed: float
