import psycopg2
import sqlite3
import mysql.connector

def connect():
  mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123456",
    database="bpmonitor",
    port="5432"
  )
  return mydb

def connect_sqlite():
  conn = sqlite3.connect('bpmonitordb')
  return conn

def connect_mysql():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="bpmonitor"
  )
  return mydb
