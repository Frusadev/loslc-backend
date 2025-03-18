import smtplib
import ssl
from email.message import EmailMessage

from app.env import APP_EMAIL_ADDRESS, GOOGLE_APP_PASSWORD


def send_email(email: str, subject: str, message: str):
    email_message = EmailMessage()
    email_message["From"] = APP_EMAIL_ADDRESS
    email_message["To"] = email
    email_message["Subject"] = subject
    email_message.set_content(message)
    ssl_context = ssl.create_default_context()

    if not APP_EMAIL_ADDRESS or not GOOGLE_APP_PASSWORD:
        raise ValueError("Origin email and password not set")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
        server.login(APP_EMAIL_ADDRESS, GOOGLE_APP_PASSWORD)
        try:
            server.send_message(email_message)
        except Exception as e:
            print(e)
            raise ValueError("Email not sent")
