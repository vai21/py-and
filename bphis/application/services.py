import requests


def hitOpenApi(data):
  # url open api
  url = 'https://localhost:8000/api/bp'

  systolic, diastolic, pulse_rate, date, ihb, map, is_user_move, measurement_time  = data
  r = requests.post(url, data={
    'systolic': systolic,
    'diastolic': diastolic,
    'pulse_rate': pulse_rate,
    'ihb': ihb,
    'meanarterialpressure': map,
    'is_user_move': is_user_move,
    'measurement_time': measurement_time,
    'date': date
  })
  
  print(r.text)
