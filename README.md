# auto-alarm

A Python package that automatically sends email notifications when functions fail.

## Features

- Simple decorator-based API
- Configurable via dictionary, JSON file, or environment variables
- Support for multiple recipients
- Optional success notifications
- Full error traceback in email

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
    host='smtp.gmail.com',
    port=587,
    username='your_email@gmail.com',
    password='your_app_password',
    from_email='your_email@gmail.com'
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
    use_tls=True  # default
)
```

### JSON Configuration

```json
// config.json
{
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "your_email@gmail.com",
    "password": "your_app_password",
    "from_email": "your_email@gmail.com"
}
```

```python
from auto_alarm import init_from_config

with open('config.json') as f:
    config = json.load(f)

init_from_config(config)
```

### Environment Variables

Set these environment variables:
- `AUTO_ALARM_HOST`
- `AUTO_ALARM_PORT`
- `AUTO_ALARM_USERNAME`
- `AUTO_ALARM_PASSWORD`
- `AUTO_ALARM_FROM_EMAIL`

```python
from auto_alarm import init_from_config, Config

config = Config.from_env()
init_from_config(config)
```

## API Reference

### `init_notifier(host, port, username, password, from_email, use_tls=True)`

Initialize the global email notifier.

### `init_from_config(config)`

Initialize from Config object or dictionary.

### `@notify_on_failure(to_emails, notify_on_success=False, success_message=None)`

Decorator that sends email notification on function failure.

- `to_emails`: Recipient email address(es) (str or list)
- `notify_on_success`: Send notification on success (default: False)
- `success_message`: Custom message for success notifications

## SMTP Examples

### Gmail

```python
init_notifier(
    host='smtp.gmail.com',
    port=587,
    username='your_email@gmail.com',
    password='your_app_password',  # Use App Password, not your login password
    from_email='your_email@gmail.com'
)
```

Note: For Gmail, you need to enable 2-Step Verification and create an App Password.

### Outlook

```python
init_notifier(
    host='smtp.office365.com',
    port=587,
    username='your_email@outlook.com',
    password='your_password',
    from_email='your_email@outlook.com'
)
```

## License

MIT
