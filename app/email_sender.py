import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to_email, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email credentials missing in .env")

    if not to_email:
        raise ValueError("Recipient email missing")

    print("Connecting to SMTP...")

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("SMTP Login Successful")
            server.send_message(msg)
            print("Email Sent Successfully")

    except smtplib.SMTPAuthenticationError:
        raise ValueError(
            "SMTP Authentication Failed. Check Gmail App Password.")

    except Exception as e:
        raise ValueError(f"SMTP Error: {str(e)}")
