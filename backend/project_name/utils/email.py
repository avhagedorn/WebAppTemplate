import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from project_name.configs import SUPPORT_EMAIL
from project_name.configs import SUPPORT_EMAIL_APP_PASSWORD
from project_name.configs import WEB_URL


def _send_email(email_to: str, msg: MIMEMultipart):
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(SUPPORT_EMAIL, SUPPORT_EMAIL_APP_PASSWORD)
    smtpserver.sendmail(SUPPORT_EMAIL, email_to, msg.as_string())
    smtpserver.close()


def _create_email_message(email_to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = SUPPORT_EMAIL
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    return msg


def _create_email_message_with_attachments(
    email_to: str,
    subject: str,
    body: str,
    attachments: List[bytes],
    attachment_names: List[str],
):
    msg = _create_email_message(email_to, subject, body)

    for attachment, attachment_name in zip(attachments, attachment_names):
        attachment_part = MIMEApplication(attachment, Name=attachment_name)
        attachment_part["Content-Disposition"] = (
            f'attachment; filename="{attachment_name}"'
        )
        msg.attach(attachment_part)

    return msg


def send_data_request_email(email_to: str, attachment: bytes):
    subject = "Your Data Request"
    body = (
        "Thank you for your data request. We have processed "
        "your request and attached the data file to this email."
        "\n\nBest,\nproject_title Team"
    )
    msg = _create_email_message_with_attachments(
        email_to, subject, body, [attachment], ["data.json"]
    )
    _send_email(email_to, msg)


def send_reset_password_email(email_to: str, request_uuid: str):
    reset_password_link = f"{WEB_URL}/auth/reset-password/{request_uuid}"

    subject = "Reset Your Password"
    body = (
        "Please click the link below to reset your password. This request will expire in one hour."
        "\nIf you did not request a password reset, please ignore this email."
        f"\n\n{reset_password_link}\n\nBest,\nproject_title Team"
    )
    msg = _create_email_message(email_to, subject, body)
    _send_email(email_to, msg)
