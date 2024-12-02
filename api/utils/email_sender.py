from flask_mail import Mail, Message
from decouple import config
from flask import render_template

mail = Mail()


def init_mail(current_app):
    """
    Initializes Flask-Mail with the given current_app.
    """
    current_app.config["MAIL_SERVER"] = config("MAIL_SERVER", default="smtp.gmail.com")
    current_app.config["MAIL_PORT"] = config("MAIL_PORT", default=587, cast=int)
    current_app.config["MAIL_USE_TLS"] = config("MAIL_USE_TLS", default=True, cast=bool)
    current_app.config["MAIL_USE_SSL"] = config(
        "MAIL_USE_SSL", default=False, cast=bool
    )
    current_app.config["MAIL_USERNAME"] = config("MAIL_USERNAME")
    current_app.config["MAIL_PASSWORD"] = config("MAIL_PASSWORD")
    current_app.config["MAIL_SENDER"] = config(
        "MAIL_SENDER", default="MAIL_DEFAULT_SENDER"
    )

    mail.init_app(current_app)


def send_reset_email(user, reset_link):
    """Sends a password reset link to user email."""

    email_html = render_template(
        "email/template/password-reset.html", user=user, url=reset_link
    )

    # Create and send email
    mail_sender = config("MAIL_DEFAULT_SENDER")

    msg = Message(
        subject="Reset Your Password",
        sender=(mail_sender, "MAIL_DEFAULT_SENDER"),
        recipients=[user.email],
        html=email_html,
    )
    try:
        with mail.connect() as conn:
            conn.send(msg)
            print("Password reset email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
