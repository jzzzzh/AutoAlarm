# auto-alarm

<p>

[![PyPI Version](https://img.shields.io/pypi/v/auto-alarm.svg)](https://pypi.org/project/auto-alarm/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/auto-alarm)](https://pypi.org/project/auto-alarm/)
[![Python Version](https://img.shields.io/pypi/pyversions/auto-alarm)](https://pypi.org/project/auto-alarm/)
[![License](https://img.shields.io/pypi/l/auto-alarm)](https://github.com/yourusername/auto-alarm/blob/main/LICENSE)

</p>

A Python package that automatically sends email notifications when functions fail. Perfect for monitoring long-running tasks, ML training jobs, and background processes.

## Why auto-alarm?

- Simple decorator-based API - just add one line of code
- Works with any Python function
- Supports multiple email providers (Gmail, QQ, Outlook, etc.)
- Flexible configuration options
- Lightweight, zero dependencies

## Installation

```bash
pip install auto-alarm
```

Or install from source:

```bash
pip install -e .
```

## Quick Start

```python
from auto_alarm import init_notifier, notify_on_failure

# Initialize with SMTP settings
init_notifier(
    host='smtp.qq.com',
    port=465,
    username='your_email@qq.com',
    password='your_auth_code',
    from_email='your_email@qq.com',
    use_ssl=True
)

# Use decorator to monitor function
@notify_on_failure('recipient@example.com')
def train_model(epochs):
    if epochs > 100:
        raise ValueError("Epochs cannot exceed 100")
    return f"Model trained for {epochs} epochs"

# Function fails - email will be sent automatically
result = train_model(150)
```

When the function raises an exception, you'll receive an email with:
- Function name and module
- Error type and message
- Full traceback
- Execution timestamp

## Configuration

### Dictionary Configuration

```python
from auto_alarm import init_notifier

init_notifier(
    host='smtp.gmail.com',
    port=587,
    username='your_email@gmail.com',
    password='your_app_password',
    from_email='your_email@gmail.com',
    use_tls=True
)
```

### JSON Configuration

```json
// config.json
{
    "host": "smtp.qq.com",
    "port": 465,
    "username": "your_email@qq.com",
    "password": "your_auth_code",
    "from_email": "your_email@qq.com",
    "use_ssl": true
}
```

```python
from auto_alarm import init_from_config
import json

with open('config.json') as f:
    config = json.load(f)

init_from_config(config)
```

### Environment Variables

```bash
export AUTO_ALARM_HOST=smtp.qq.com
export AUTO_ALARM_PORT=465
export AUTO_ALARM_USERNAME=your_email@qq.com
export AUTO_ALARM_PASSWORD=your_auth_code
export AUTO_ALARM_FROM_EMAIL=your_email@qq.com
export AUTO_ALARM_USE_SSL=true
```

```python
from auto_alarm import init_from_config, Config

config = Config.from_env()
init_from_config(config)
```

## API Reference

### `init_notifier(host, port, username, password, from_email, use_tls=True, use_ssl=False)`

Initialize the global email notifier.

### `init_from_config(config)`

Initialize from Config object or dictionary.

### `@notify_on_failure(to_emails, notify_on_success=False, success_message=None)`

Decorator that sends email notification on function failure.

**Parameters:**
- `to_emails`: Recipient email address(es) (str or list)
- `notify_on_success`: Send notification on success (default: False)
- `success_message`: Custom message for success notifications

## SMTP Examples

### QQ Mail

```python
init_notifier(
    host='smtp.qq.com',
    port=465,
    username='your_email@qq.com',
    password='your_auth_code',
    from_email='your_email@qq.com',
    use_ssl=True
)
```

> Note: For QQ Mail, enable SMTP service in settings and generate an authorization code.

### Gmail

```python
init_notifier(
    host='smtp.gmail.com',
    port=587,
    username='your_email@gmail.com',
    password='your_app_password',
    from_email='your_email@gmail.com',
    use_tls=True
)
```

> Note: For Gmail, enable 2-Step Verification and create an App Password.

### Outlook

```python
init_notifier(
    host='smtp.office365.com',
    port=587,
    username='your_email@outlook.com',
    password='your_password',
    from_email='your_email@outlook.com',
    use_tls=True
)
```

## License

MIT License - see [LICENSE](LICENSE) for details.
