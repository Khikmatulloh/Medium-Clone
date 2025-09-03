import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from app.tasks.celery_config import celery_app
load_dotenv()
EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
SMTP_SERVER=os.getenv("SMTP_SERVER")
SMTP_PORT=os.getenv("SMTP_PORT")



@celery_app.task
def send_email(to_email: str, subject: str, body: str):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    
    return f"Email sent to {to_email}"
