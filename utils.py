from typing import Any, List
import requests
from requests.adapters import HTTPAdapter
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data
import pandas as pd
from urllib3 import Retry

HOURLY = [
    "temperature_2m",
    "apparent_temperature",
    "precipitation_probability",
    "windspeed_10m",
    "uv_index",
]


class OpenMeteoAPIConnection(ExperimentalBaseConnection[requests.Session]):
    """Streamlit experimental_connection implementation for Open-Meteo API"""

    def __init__(
        self,
        connection_name: str,
        base_url: str = "https://api.open-meteo.com/v1/forecast",
        total_retries: int = 5,
        backoff_factor: float = 0.25,
        status_forcelist: List[int] = None,
        **kwargs,
    ) -> None:
        self.base_url = base_url

        if status_forcelist is None:
            status_forcelist = [500, 502, 503, 504]

        self.retries = Retry(
            total=total_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )

        super().__init__(connection_name, **kwargs)

    def _connect(self, **kwargs: Any) -> requests.Session:
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=self.retries))
        return session

    def cursor(self):
        return self._connect()

    def query_hourly_forecast(
        self,
        latitude: float,
        longitude: float,
        cache_time: int = 3600,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Queries the hourly temperature forecast API and returns a DataFrame."""

        @cache_data(ttl=cache_time)
        def _query_hourly_forecast(
            latitude: float,
            longitude: float,
            hourly: List = HOURLY,
            **kwargs: Any,
        ) -> pd.DataFrame:
            url = self.base_url
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": hourly,
                **kwargs,
            }

            try:
                response = self._instance.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # Create a DataFrame from the JSON response
                result = pd.DataFrame(data)

                return result

            except Exception as query_error:
                print(f"An error occurred: {query_error}")
                return None

        return _query_hourly_forecast(latitude, longitude, **kwargs)


def create_hourly_df(data):
    temperature_df = pd.DataFrame(
        data={
            "Temperature": data["hourly"]["temperature_2m"],
            "Apparent Temperature": data["hourly"]["apparent_temperature"],
        },
        index=data["hourly"]["time"],
    )

    precipitation_df = pd.DataFrame(
        data={
            "Precipitation Probability": data["hourly"]["precipitation_probability"],
        },
        index=data["hourly"]["time"],
    )

    wind_df = pd.DataFrame(
        data={
            "Wind Speed(10m)": data["hourly"]["windspeed_10m"],
        },
        index=data["hourly"]["time"],
    )

    uv_df = pd.DataFrame(
        data={
            "UV Index": data["hourly"]["uv_index"],
        },
        index=data["hourly"]["time"],
    )

    return temperature_df, precipitation_df, wind_df, uv_df
