from libs.latest_announcement import fetch_latest_announcement
from libs.send_mail import send_email_welcome
import psycopg2
from dotenv import load_dotenv

load_dotenv()

import os

def get_connection():
  return psycopg2.connect(
    database=os.getenv("DB_CLOUD_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
  )


def init_db():
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS emails (
      id SERIAL PRIMARY KEY,
      email TEXT NOT NULL,
      last_seen TEXT
  )                             
  """)

  conn.commit()
  conn.close()

def register_email(email):
  try:
    conn = get_connection()
    cursor = conn.cursor()
    
    email_exists = cursor.execute("SELECT * FROM emails WHERE email = %s", (email,))

    if email_exists:
      raise Exception("Email ya registrado")

    latest_announcement = fetch_latest_announcement()

    cursor.execute("INSERT INTO emails (email, last_seen) VALUES (%s, %s)", (email, latest_announcement,))

    print("Sending welcome email to", email)

    send_email_welcome(email)

    conn.commit()
    conn.close()


    return True
  except Exception as e:
    raise e

def get_users():
  conn = get_connection()
  cursor = conn.cursor()

  users = cursor.execute("SELECT * FROM emails")
  users = cursor.fetchall()

  print(users)

  conn.close()

  return users

def update_last_seen(email, last_seen):
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("UPDATE emails SET last_seen = %s WHERE email = %s", (last_seen, email,))

  conn.commit()
  conn.close()