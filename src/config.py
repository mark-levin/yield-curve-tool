import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    fred_api_key: str
    db_url: str = "sqlite:///yield_curves.db"

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.
        """
        api_key = os.getenv("FRED_API_KEY")
        if not api_key:
            raise RuntimeError("FRED_API_KEY not set in environment")
        db_url = os.getenv("DB_URL", "sqlite:///yield_curves.db")
        return cls(fred_api_key=api_key, db_url=db_url)
