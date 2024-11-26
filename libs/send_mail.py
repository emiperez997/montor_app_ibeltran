import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_mail_announcement(to_email, announcement):
  try:
    global SMTP_SERVER, SMTP_PORT, EMAIL, PASSWORD

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    subject = "Subject: Nuevo anuncio"
    body = f"""Se ha detectado un nuevo anuncio: <br>
    <b>{announcement}</b>"""

    message = MIMEText(body, "html")
    message["Subject"] = subject
    message["From"] = EMAIL

    server.sendmail(EMAIL, to_email, message.as_string())

    server.quit()
    
    return True
  except Exception as e:
    print(e)
    return False

def send_email_welcome(to_email):
  try:
    global SMTP_SERVER, SMTP_PORT, EMAIL, PASSWORD


    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    subject = "Subject: Bienvenido"
    body = f"""Gracias por registrarte en nuestro servicio de monitoreo de anuncios"""

    message = MIMEText(body, "html")
    message["Subject"] = subject
    message["From"] = "Anuncios Instituto Beltrán"

    server.sendmail(EMAIL, to_email, message.as_string())

    server.quit()
    
    return True
  except Exception as e:
    print(e)
    return False