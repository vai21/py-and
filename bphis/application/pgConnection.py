import psycopg2

def connect():
  mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123456",
    database="bpmonitor",
    port="5432"
  )

  return mydb
