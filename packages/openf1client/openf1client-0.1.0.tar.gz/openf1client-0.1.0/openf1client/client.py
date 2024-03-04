import requests
from openf1client.models.driver import Driver
from openf1client.models.car_data import CarData
from openf1client.models.interval import Interval
from openf1client.models.lap import Lap
from openf1client.models.location import Location
from openf1client.models.meeting import Meeting
from openf1client.models.pit import Pit
from openf1client.models.position import Position
from openf1client.models.race_control import RaceControl
from openf1client.models.session import Session
from openf1client.models.stint import Stint
from openf1client.models.team_radio import TeamRadio
from openf1client.models.weather import Weather


class OpenF1Client:
    def __init__(self, base_url="https://api.openf1.org/v1"):
        self.base_url = base_url

    def get_car_data(
        self,
        driver_number: int = None,
        meeting_key: int = None,
        session_key: int = None,
    ) -> list[CarData]:
        url = f"{self.base_url}/car_data"
        params = {
            "driver_number": driver_number,
            "meeting_key": meeting_key,
            "session_key": session_key,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [CarData(**car_data) for car_data in response.json()]

    def get_drivers(
        self,
        country_code: str = None,
        driver_number: int = None,
        first_name: str = None,
        full_name: str = None,
        last_name: str = None,
        meeting_key: int = None,
        session_key: int = None,
        team_name: str = None,
    ) -> list[Driver]:
        url = f"{self.base_url}/drivers"
        params = {
            "country_code": country_code,
            "driver_number": driver_number,
            "first_name": first_name,
            "full_name": full_name,
            "last_name": last_name,
            "meeting_key": meeting_key,
            "session_key": session_key,
            "team_name": team_name,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Driver(**driver) for driver in response.json()]

    # Driver number doesn't work: When providing a driver number AND a session key, the API returns an empty list
    def get_intervals(
        self,
        meeting_key: int = None,
        session_key: int = None,
    ) -> list[Interval]:
        url = f"{self.base_url}/intervals"
        params = {
            "meeting_key": meeting_key,
            "session_key": session_key,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        print(url)
        response = requests.get(url)
        return [Interval(**interval) for interval in response.json()]

    def get_laps(
        self,
        meeting_key: int = None,
        session_key: int = None,
        driver_number: int = None,
        lap_number: int = None,
    ) -> list[Lap]:
        url = f"{self.base_url}/laps"
        params = {
            "meeting_key": meeting_key,
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Lap(**lap) for lap in response.json()]

    def get_locations(
        self,
        session_key: int = None,
        meeting_key: int = None,
        driver_number: int = None,
    ) -> list[Location]:
        url = f"{self.base_url}/location"
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Location(**location) for location in response.json()]

    def get_meetings(
        self,
        year: int = None,
        country_code: str = None,
        country_name: str = None,
        circuit_key: int = None,
        circuit_short_name: str = None,
        meeting_key: int = None,
    ) -> list[Meeting]:
        url = f"{self.base_url}/meetings"
        params = {
            "year": year,
            "country_code": country_code,
            "country_name": country_name,
            "circuit_key": circuit_key,
            "circuit_short_name": circuit_short_name,
            "meeting_key": meeting_key,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Meeting(**meeting) for meeting in response.json()]

    def get_pits(
        self,
        meeting_key: int = None,
        session_key: int = None,
        driver_number: int = None,
        lap_number: int = None,
    ) -> list[Pit]:
        url = f"{self.base_url}/pit"
        params = {
            "meeting_key": meeting_key,
            "session_key": session_key,
            "driver_number": driver_number,
            "lap_number": lap_number,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Pit(**pit) for pit in response.json()]

    def get_positions(
        self,
        session_key: int = None,
        meeting_key: int = None,
        driver_number: int = None,
    ) -> list[Position]:
        url = f"{self.base_url}/position"
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Position(**location) for location in response.json()]

    def get_race_control(
        self,
        meeting_key: int = None,
        session_key: int = None,
        lap_number: int = None,
        driver_number: int = None,
    ) -> list[RaceControl]:
        url = f"{self.base_url}/race_control"
        params = {
            "meeting_key": meeting_key,
            "session_key": session_key,
            "lap_number": lap_number,
            "driver_number": driver_number,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [RaceControl(**race_control) for race_control in response.json()]

    def get_sessions(
        self,
        circuit_key: int = None,
        circuit_short_name: str = None,
        country_code: str = None,
        country_key: int = None,
        country_name: str = None,
        meeting_key: int = None,
        session_key: int = None,
        session_name: str = None,
        session_type: str = None,
        year: int = None,
    ) -> list[Session]:
        url = f"{self.base_url}/sessions"
        params = {
            "circuit_key": circuit_key,
            "circuit_short_name": circuit_short_name,
            "country_code": country_code,
            "country_key": country_key,
            "country_name": country_name,
            "meeting_key": meeting_key,
            "session_key": session_key,
            "session_name": session_name,
            "session_type": session_type,
            "year": year,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Session(**session) for session in response.json()]

    def get_stints(
        self,
        compound: str = None,
        driver_number: int = None,
        meeting_key: int = None,
        session_key: int = None,
        stint_number: int = None,
    ) -> list[Stint]:
        url = f"{self.base_url}/stints"
        params = {
            "compound": compound,
            "driver_number": driver_number,
            "meeting_key": meeting_key,
            "session_key": session_key,
            "stint_number": stint_number,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Stint(**stint) for stint in response.json()]

    def get_team_radios(
        self,
        driver_number: int = None,
        meeting_key: int = None,
        session_key: int = None,
    ) -> list[TeamRadio]:
        url = f"{self.base_url}/team_radio"
        params = {
            "driver_number": driver_number,
            "meeting_key": meeting_key,
            "session_key": session_key,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [TeamRadio(**team_radio) for team_radio in response.json()]

    def get_weather(
        self,
        meeting_key: int = None,
        session_key: int = None,
    ) -> list[Weather]:
        url = f"{self.base_url}/weather"
        params = {
            "meeting_key": meeting_key,
            "session_key": session_key,
        }
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

        response = requests.get(url)
        return [Weather(**weather) for weather in response.json()]
