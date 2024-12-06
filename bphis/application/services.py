import requests


def hitOpenApi(data):
  # url open api
  url = 'http://192.168.74.211:30507/api/bp/'

  systolic, diastolic, pulse_rate, date, ihb, map, is_user_move, retest, measurement_time  = data
  r = requests.post(url, data={
    'systolic': systolic,
    'diastolic': diastolic,
    'pulserate': pulse_rate,
    'ihb': ihb,
    'meanarterialpressure': map,
    'is_user_move': is_user_move,
    'retest': retest,
    'measurement_time': measurement_time,
    'created_at': date
  })
  
  print(r.text)
