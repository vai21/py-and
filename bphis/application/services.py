import requests

def hitOpenApi(data):
  url = 'https://localhost:8000/api'
  systolic, diastolic, pulse_rate, date = data
  r = requests.post(url, data={
    'systolic': systolic,
    'diastolic': diastolic,
    'pulse_rate': pulse_rate,
    'date': date
  })
  print(r.text)
