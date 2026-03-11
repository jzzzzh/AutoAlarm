"""
auto-alarm: A Python package for automatic email notifications on function failure.

This package provides a simple way to monitor function execution and send
email notifications when functions fail (or optionally on success).

Usage:
    from auto_alarm import init_notifier, notify_on_failure

    # Initialize with SMTP settings
    init_notifier(
        host='smtp.gmail.com',
        port=587,
        username='your_email@gmail.com',
        password='your_app_password',
        from_email='your_email@gmail.com'
    )

    # Use decorator to monitor function
    @notify_on_failure('recipient@example.com')
    def your_function():
        # function logic
        pass
"""

from .config import Config
from .notifier import EmailNotifier, ErrorNotificationBuilder
from .decorator import (
    init_notifier,
    init_from_config,
    get_notifier,
    set_notifier,
    notify_on_failure,
)

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    # Config
    "Config",
    # Notifier
    "EmailNotifier",
    "ErrorNotificationBuilder",
    # Decorator
    "init_notifier",
    "init_from_config",
    "get_notifier",
    "set_notifier",
    "notify_on_failure",
]
