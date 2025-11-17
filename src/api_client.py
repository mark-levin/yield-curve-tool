import logging
from typing import Any, Dict, Optional

import requests

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


class ApiClient:
    """
    Simple REST client with basic error handling.
    """

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.debug("GET %s params=%s", url, params)
        resp = requests.get(url, params=params, timeout=self.timeout)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error("HTTP error for %s: %s", url, e)
            raise
        return resp.json()
