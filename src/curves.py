from typing import Dict

from .config import Config
from .fred_client import FredClient
from .storage import df_to_db


# Map tenors to FRED series IDs (UST)
UST_SERIES_MAP: Dict[float, str] = {
    1.0: "DGS1",
    2.0: "DGS2",
    5.0: "DGS5",
    10.0: "DGS10",
    30.0: "DGS30",
}


def download_and_store_ust_curve(
    start_date: str,
    end_date: str,
    config: Config,
    curve_name: str = "UST",
) -> None:
    """
    High-level function:
    - pulls UST yield curve data from FRED
    - writes to DB.
    """
    fred = FredClient(config)
    df = fred.get_curve(UST_SERIES_MAP, start_date=start_date, end_date=end_date)
    df_to_db(df, curve_name=curve_name, config=config)
