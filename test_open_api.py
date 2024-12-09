from bphis.application.services import hitOpenApi

data = {
  'systolic': 120,
  'diastolic': 90,
  'pulserate': 75,
  'meanarterialpressure': 100
}

result = hitOpenApi(data)

print(f"result {result}")
