import requests


def hitOpenApi(data):
  # url open api
  url = 'http://localhost:8000/api/bp/'

  result = requests.post(url, data={
    'systolic': data.systolic,
    'diastolic': data.diastolic,
    'pulserate': data.pulse_rate,
    'ihb': data.ihb or None,
    'meanarterialpressure': data.map or None,
    'is_user_move': data.is_user_move or None,
    'retest': data.retest or None,
    'measurement_time': data.measurement_time or None,
    'created_at': data.date or None
  })
  
  print(result.text)
