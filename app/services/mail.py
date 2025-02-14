import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class Mailer:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_mail = settings.SMTP_MAIL
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS

        if not all([self.smtp_server, self.smtp_port, self.smtp_mail, self.smtp_password]):
            raise ValueError("SMTP settings are not set, so mail can't be sent")

    def __enter__(self):
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        if self.smtp_tls:
            self.server.starttls()
        self.server.login(self.smtp_mail, self.smtp_password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.quit()
        return False

    def send_mail(self, to: str, subject: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_mail
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        self.server.sendmail(self.smtp_mail, to, msg.as_string())
