"""Basic usage examples for auto-alarm."""

from auto_alarm import init_notifier, notify_on_failure


def example_basic():
    """Example 1: Basic usage with dictionary config."""
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
        """Example training function."""
        if epochs > 100:
            raise ValueError("Epochs cannot exceed 100")
        print(f"Training for {epochs} epochs...")
        return f"Model trained for {epochs} epochs"

    # Call the function
    result = train_model(50)  # Success - no email
    print(result)

    # This will trigger email notification
    try:
        train_model(150)  # Will raise and send email
    except ValueError as e:
        print(f"Caught expected error: {e}")


def example_with_config_file():
    """Example 2: Load config from JSON file."""
    import json
    from auto_alarm import init_from_config, notify_on_failure

    # config.json should contain:
    # {
    #     "host": "smtp.gmail.com",
    #     "port": 587,
    #     "username": "your_email@gmail.com",
    #     "password": "your_app_password",
    #     "from_email": "your_email@gmail.com"
    # }

    with open('config.json') as f:
        config = json.load(f)

    init_from_config(config)

    @notify_on_failure('author@example.com')
    def data_pipeline():
        """Example data pipeline."""
        import random
        if random.random() < 0.5:
            raise RuntimeError("Random pipeline failure")
        return "Pipeline completed"

    data_pipeline()


def example_with_env():
    """Example 3: Load config from environment variables."""
    import os
    from auto_alarm import init_from_config, notify_on_failure, Config

    # Set environment variables:
    # AUTO_ALARM_HOST=smtp.gmail.com
    # AUTO_ALARM_PORT=587
    # AUTO_ALARM_USERNAME=your_email@gmail.com
    # AUTO_ALARM_PASSWORD=your_app_password
    # AUTO_ALARM_FROM_EMAIL=your_email@gmail.com

    config = Config.from_env()
    init_from_config(config)

    @notify_on_failure('admin@example.com')
    def batch_job():
        """Example batch job."""
        raise Exception("Batch job failed")

    try:
        batch_job()
    except Exception as e:
        print(f"Error: {e}")


def example_multiple_recipients():
    """Example 4: Send to multiple recipients."""
    from auto_alarm import init_notifier, notify_on_failure

    init_notifier(
        host='smtp.gmail.com',
        port=587,
        username='your_email@gmail.com',
        password='your_app_password',
        from_email='your_email@gmail.com'
    )

    # Send to multiple recipients
    @notify_on_failure(['dev@example.com', 'admin@example.com'])
    def critical_operation():
        """Example critical operation."""
        raise RuntimeError("Critical operation failed")

    try:
        critical_operation()
    except Exception as e:
        print(f"Error: {e}")


def example_notify_on_success():
    """Example 5: Also notify on success."""
    from auto_alarm import init_notifier, notify_on_failure

    init_notifier(
        host='smtp.gmail.com',
        port=587,
        username='your_email@gmail.com',
        password='your_app_password',
        from_email='your_email@gmail.com'
    )

    # Notify on both failure and success
    @notify_on_failure(
        to_emails='author@example.com',
        notify_on_success=True,
        success_message="Your long-running task completed successfully!"
    )
    def long_running_task():
        """Example long-running task."""
        import time
        time.sleep(2)
        return "Task completed"

    long_running_task()


if __name__ == '__main__':
    # Run basic example
    print("=" * 50)
    print("Example 1: Basic Usage")
    print("=" * 50)
    example_basic()
