#!/usr/bin/env python3

import smtplib

try:
    # Use port 587 for TLS
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # Login to the server
    server.login("eeomo007@gmail.com", "upnz xlch pzgt xfvs")

    # Compose and send the email
    server.sendmail(
        from_addr="eeomo007@gmail.com",
        to_addrs="recipient@example.com",
        msg="Subject: Test Email\n\nThis is a test email.",
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    # Ensure the server quits properly
    if "server" in locals():
        server.quit()
