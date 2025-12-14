import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_subscription_email(
    to_email: str,
    user_name: str,
    products: list[dict],
    total_amount: int,
    start_date: str,
):
    subject = "Subscription Payment Successful 🎉"

    product_lines = ""
    for p in products:
        product_lines += f"- {p['name']} (₹{p['price']})\n"

    body = f"""
Hi {user_name},

Your subscription payment was successful ✅

Subscribed Products:
{product_lines}

Total Paid: ₹{total_amount}
Subscription Start Date: {start_date}

Thank you for subscribing 🙏
"""

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
