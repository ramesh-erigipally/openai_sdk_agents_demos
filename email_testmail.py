# test_send.py

from email_sender import send_email

send_email(
    subject="Hello from Module",
    body="This email was sent using a reusable Python module.",
    to_email="openaidemotest@mailinator.com"
)
