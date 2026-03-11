"""Email notification module for auto-alarm."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Union, Optional
from datetime import datetime


class EmailNotifier:
    """Email notifier for sending error notifications."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        from_email: str,
        use_tls: bool = True,
        use_ssl: bool = False,
    ):
        """Initialize email notifier.

        Args:
            host: SMTP server host.
            port: SMTP server port.
            username: SMTP username.
            password: SMTP password.
            from_email: Sender email address.
            use_tls: Whether to use TLS (default: True).
            use_ssl: Whether to use SSL (default: False, for port 465).
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.use_tls = use_tls
        self.use_ssl = use_ssl

    def send(
        self,
        subject: str,
        body: str,
        to_emails: Union[str, List[str]],
    ) -> bool:
        """Send email notification.

        Args:
            subject: Email subject.
            body: Email body content.
            to_emails: Recipient email address(es).

        Returns:
            True if email was sent successfully.

        Raises:
            smtplib.SMTPException: If email sending fails.
        """
        if isinstance(to_emails, str):
            to_emails = [to_emails]

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_emails)

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP_SSL(self.host, self.port) if self.use_ssl else smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls and not self.use_ssl:
                server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.from_email, to_emails, msg.as_string())

        return True


class ErrorNotificationBuilder:
    """Builder for error notification content."""

    def __init__(
        self,
        func_name: str,
        func_module: str,
        error_type: str,
        error_message: str,
        traceback: str,
        timestamp: Optional[datetime] = None,
    ):
        """Initialize error notification builder.

        Args:
            func_name: Function name.
            func_module: Function module.
            error_type: Error type.
            error_message: Error message.
            traceback: Full traceback.
            timestamp: Error timestamp (default: now).
        """
        self.func_name = func_name
        self.func_module = func_module
        self.error_type = error_type
        self.error_message = error_message
        self.traceback = traceback
        self.timestamp = timestamp or datetime.now()

    def build_subject(self) -> str:
        """Build email subject."""
        return f"[Error] {self.func_module}.{self.func_name} failed"

    def build_body(self) -> str:
        """Build email body."""
        return f"""Function Error Report
{'=' * 50}

Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Function: {self.func_module}.{self.func_name}
Error Type: {self.error_type}
Error Message: {self.error_message}

Full Traceback:
{'-' * 50}
{self.traceback}
{'-' * 50}

This is an automated notification from auto-alarm.
"""

    def send(self, notifier: EmailNotifier, to_emails: Union[str, List[str]]) -> bool:
        """Send error notification email.

        Args:
            notifier: Email notifier instance.
            to_emails: Recipient email address(es).

        Returns:
            True if email was sent successfully.
        """
        subject = self.build_subject()
        body = self.build_body()
        return notifier.send(subject, body, to_emails)
