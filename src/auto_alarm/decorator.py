"""Decorator module for auto-alarm."""

import functools
import traceback
from datetime import datetime
from typing import Callable, List, Union, Optional, Any

from .notifier import EmailNotifier, ErrorNotificationBuilder
from .config import Config


_global_notifier: Optional[EmailNotifier] = None


def init_notifier(
    host: str,
    port: int,
    username: str,
    password: str,
    from_email: str,
    use_tls: bool = True,
    use_ssl: bool = False,
) -> EmailNotifier:
    """Initialize the global email notifier.

    This function must be called before using the notify_on_failure decorator.

    Args:
        host: SMTP server host.
        port: SMTP server port.
        username: SMTP username.
        password: SMTP password.
        from_email: Sender email address.
        use_tls: Whether to use TLS (default: True).
        use_ssl: Whether to use SSL (default: False, for port 465).

    Returns:
        EmailNotifier instance.
    """
    global _global_notifier
    _global_notifier = EmailNotifier(
        host=host,
        port=port,
        username=username,
        password=password,
        from_email=from_email,
        use_tls=use_tls,
        use_ssl=use_ssl,
    )
    return _global_notifier


def init_from_config(config: Union[dict, Config]) -> EmailNotifier:
    """Initialize the global notifier from a Config object or dictionary.

    Args:
        config: Config object or dictionary with SMTP settings.

    Returns:
        EmailNotifier instance.
    """
    if isinstance(config, Config):
        config_dict = config.to_dict()
    else:
        config_dict = config

    return init_notifier(
        host=config_dict['host'],
        port=config_dict['port'],
        username=config_dict['username'],
        password=config_dict['password'],
        from_email=config_dict['from_email'],
        use_tls=config_dict.get('use_tls', True),
        use_ssl=config_dict.get('use_ssl', False),
    )


def get_notifier() -> Optional[EmailNotifier]:
    """Get the global email notifier instance.

    Returns:
        EmailNotifier instance or None if not initialized.
    """
    return _global_notifier


def set_notifier(notifier: EmailNotifier) -> None:
    """Set the global email notifier instance.

    Args:
        notifier: EmailNotifier instance to use.
    """
    global _global_notifier
    _global_notifier = notifier


def notify_on_failure(
    to_emails: Union[str, List[str]],
    notify_on_success: bool = False,
    success_message: Optional[str] = None,
):
    """Decorator that sends email notification on function failure (or success).

    Args:
        to_emails: Recipient email address(es).
        notify_on_success: Whether to send notification on success (default: False).
        success_message: Custom message for success notifications.

    Returns:
        Decorated function.

    Raises:
        RuntimeError: If notifier is not initialized.

    Example:
        >>> init_notifier('smtp.gmail.com', 587, 'user@gmail.com', 'pass', 'user@gmail.com')
        >>>
        >>> @notify_on_failure('admin@example.com')
        ... def my_function():
        ...     # function logic
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            global _global_notifier

            if _global_notifier is None:
                raise RuntimeError(
                    "Notifier not initialized. Call init_notifier() first."
                )

            start_time = datetime.now()
            success = False
            error_info = None

            try:
                result = func(*args, **kwargs)
                success = True
                return result
            except Exception as e:
                error_info = {
                    'type': type(e).__name__,
                    'message': str(e),
                    'traceback': traceback.format_exc(),
                }
                raise
            finally:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                if success and not notify_on_success:
                    return

                if success and notify_on_success:
                    subject = f"[Success] {func.__module__}.{func.__name__} completed"
                    body = success_message or f"""Function Execution Report
{'=' * 50}

Timestamp: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Function: {func.__module__}.{func.__name__}
Status: Success
Duration: {duration:.2f} seconds

This is an automated notification from auto-alarm.
"""
                elif error_info:
                    builder = ErrorNotificationBuilder(
                        func_name=func.__name__,
                        func_module=func.__module__,
                        error_type=error_info['type'],
                        error_message=error_info['message'],
                        traceback=error_info['traceback'],
                        timestamp=end_time,
                    )
                    subject = builder.build_subject()
                    body = builder.build_body()

                try:
                    _global_notifier.send(subject, body, to_emails)
                except Exception as e:
                    print(f"Failed to send notification email: {e}")

        return wrapper
    return decorator
