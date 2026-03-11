"""Configuration management for auto-alarm."""

import os
from typing import Optional
from pathlib import Path
import json


class Config:
    """Configuration manager for auto-alarm."""

    DEFAULT_CONFIG_KEYS = {
        'host',
        'port',
        'username',
        'password',
        'from_email',
    }

    def __init__(self, config: Optional[dict] = None):
        """Initialize configuration.

        Args:
            config: Dictionary containing SMTP configuration.
        """
        self._config = config or {}

    @classmethod
    def from_dict(cls, config: dict) -> 'Config':
        """Create Config from dictionary.

        Args:
            config: Dictionary containing SMTP configuration.

        Returns:
            Config instance.
        """
        return cls(config)

    @classmethod
    def from_json(cls, path: str) -> 'Config':
        """Create Config from JSON file.

        Args:
            path: Path to JSON configuration file.

        Returns:
            Config instance.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            json.JSONDecodeError: If config file is not valid JSON.
        """
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        return cls(config)

    @classmethod
    def from_env(cls, prefix: str = 'AUTO_ALARM_') -> 'Config':
        """Create Config from environment variables.

        Environment variables:
            {prefix}HOST: SMTP server host
            {prefix}PORT: SMTP server port
            {prefix}USERNAME: SMTP username
            {prefix}PASSWORD: SMTP password
            {prefix}FROM_EMAIL: Sender email address

        Args:
            prefix: Prefix for environment variables.

        Returns:
            Config instance.
        """
        config = {}

        env_mapping = {
            f'{prefix}HOST': 'host',
            f'{prefix}PORT': 'port',
            f'{prefix}USERNAME': 'username',
            f'{prefix}PASSWORD': 'password',
            f'{prefix}FROM_EMAIL': 'from_email',
            f'{prefix}USE_TLS': 'use_tls',
            f'{prefix}USE_SSL': 'use_ssl',
        }

        for env_key, config_key in env_mapping.items():
            value = os.environ.get(env_key)
            if value is not None:
                if config_key in ('port',):
                    try:
                        config[config_key] = int(value)
                    except ValueError:
                        continue
                elif config_key in ('use_tls', 'use_ssl'):
                    config[config_key] = value.lower() in ('true', '1', 'yes')
                else:
                    config[config_key] = value

        return cls(config)

    def get(self, key: str, default=None):
        """Get configuration value.

        Args:
            key: Configuration key.
            default: Default value if key not found.

        Returns:
            Configuration value.
        """
        return self._config.get(key, default)

    def validate(self) -> bool:
        """Validate that all required keys are present.

        Returns:
            True if configuration is valid.
        """
        return all(key in self._config for key in self.DEFAULT_CONFIG_KEYS)

    def to_dict(self) -> dict:
        """Convert configuration to dictionary.

        Returns:
            Configuration dictionary.
        """
        return self._config.copy()
