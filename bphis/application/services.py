import logging
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def hitOpenApi(data):
  # url open api
  url = 'http://127.0.0.1/api/add-vital' # Alamat API Rumah Sakit (HIS)
  logger.debug("payload data: %s", data)
  try:
    result = requests.post(url, data={
      'systolic': data.get('systolic'),
      'diastolic': data.get('diastolic'),
      'pulserate': data.get('pulserate'),
      'ihb': data.get('ihb') or None,
      'meanarterialpressure': data.get('map') or None,
      'is_user_move': data.get('is_user_move') or None,
      'retest': data.get('retest') or None,
      'measurement_time': data.get('measurement_time') or None,
      'created_at': data.get('date') or None,
      'device_id': 'AND-01' # Device ID
    }, timeout=10)
    result.raise_for_status()
  except RequestException as e:
    logger.exception("Failed to POST to open API %s", e)
    # Return None to indicate failure (preserve previous behavior of no explicit return)
    return None

  # safe access to text property and debug log
  try:
    text = result.text
  except Exception:
    text = ''
  logger.debug("result %s", text)
  return result
