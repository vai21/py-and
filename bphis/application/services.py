import requests

def hitOpenApi(data):
  url = 'https://api.github.com/events'
  systolic, diastolic, pulse_rate, date = data
  r = requests.post(url, data={
    'systolic': systolic,
    'diastolic': diastolic,
    'pulse_rate': pulse_rate,
    'date': date
  })
  return r.text
