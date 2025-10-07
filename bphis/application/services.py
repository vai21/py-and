import requests


def hitOpenApi(data):
  # url open api
  url = 'http://172.16.0.201:8000/api/add-vital' # Alamat API Rumah Sakit (HIS)
  print(f"payload data: {data}")
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
  })
  print(f"result {result.text}")
