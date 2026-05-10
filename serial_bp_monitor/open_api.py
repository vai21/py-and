"""Optional POST to HIS-style endpoint (same shape as bphis/application/services.py)."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def hit_open_api(data: dict[str, Any], url: str, device_id: str = "AND-01") -> requests.Response | None:
    """POST vital signs. Mirrors services.hitOpenApi field names."""
    created = data.get("date")
    if isinstance(created, datetime):
        created_val = created.isoformat(timespec="seconds")
    else:
        created_val = created

    payload = {
        "systolic": data.get("systolic"),
        "diastolic": data.get("diastolic"),
        "pulserate": data.get("pulserate"),
        "ihb": data.get("ihb"),
        # services.py used data.get('map'); helpers used meanarterialpressure — send both
        "meanarterialpressure": data.get("meanarterialpressure") or data.get("map"),
        "map": data.get("meanarterialpressure") or data.get("map"),
        "is_user_move": data.get("is_user_move"),
        "retest": data.get("retest"),
        "measurement_time": data.get("measurement_time"),
        "created_at": created_val,
        "device_id": device_id,
    }
    logger.debug("POST %s payload=%s", url, payload)
    try:
        result = requests.post(url, data=payload, timeout=10)
        result.raise_for_status()
    except RequestException as e:
        logger.warning("Open API POST failed: %s", e)
        return None
    return result
