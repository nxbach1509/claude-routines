#!/usr/bin/env python3
"""Send BDS Daily report via Gmail SMTP."""
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

RECIPIENT = os.environ.get("RECIPIENT_EMAIL", "nxbach1509@gmail.com")
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]

today = datetime.now().strftime("%d/%m/%Y")
subject = f"BĐS Daily — {today}"

html_body = sys.stdin.read()
if not html_body.strip():
    print("ERROR: empty report body", file=sys.stderr)
    sys.exit(1)

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = GMAIL_USER
msg["To"] = RECIPIENT
msg.attach(MIMEText(html_body, "html", "utf-8"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, RECIPIENT, msg.as_bytes())

print(f"Email sent: '{subject}' → {RECIPIENT}")
