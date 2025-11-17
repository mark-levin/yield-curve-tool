from typing import Dict, List
import pandas as pd

from .api_client import ApiClient
from .config import Config


class FredClient:
    """
    Thin wrapper around the FRED API for rate series.
    """

    def __init__(self, config: Config):
        self._config = config
        self._client = ApiClient("https://api.stlouisfed.org")

    def get_series(
        self,
        series_id: str,
        start_date: str = "1900-01-01",
        end_date: str = "9999-12-31",
    ) -> pd.DataFrame:
        """
        Download a single time series as a DataFrame with columns: ['date', 'value'].
        """
        params: Dict[str, str] = {
            "series_id": series_id,
            "api_key": self._config.fred_api_key,
            "file_type": "json",
            "observation_start": start_date,
            "observation_end": end_date,
        }
        data = self._client.get("/fred/series/observations", params=params)
        obs = data["observations"]

        df = pd.DataFrame(obs)[["date", "value"]]
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["value"])
        return df

    def get_curve(
        self,
        series_map: Dict[float, str],
        start_date: str = "1900-01-01",
        end_date: str = "9999-12-31",
    ) -> pd.DataFrame:
        """
        Download multiple series (by tenor) and merge into a 'long' curve DataFrame:

        columns: ['date', 'tenor_years', 'yield']
        """
        dfs: List[pd.DataFrame] = []
        for tenor, series_id in series_map.items():
            s = self.get_series(series_id, start_date, end_date)
            s["tenor_years"] = tenor
            s.rename(columns={"value": "yield"}, inplace=True)
            dfs.append(s[["date", "tenor_years", "yield"]])

        curve_df = pd.concat(dfs, ignore_index=True)
        return curve_df.sort_values(["date", "tenor_years"])
