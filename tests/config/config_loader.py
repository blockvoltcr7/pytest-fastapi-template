"""
Configuration loader for test environments.
"""
import os
import importlib
from typing import Optional

class ConfigLoader:
    """
    Handles loading of environment-specific configurations.
    """
    VALID_ENVIRONMENTS = ['dev', 'uat', 'prod']
    DEFAULT_ENV = 'dev'

    @classmethod
    def load_config(cls) -> object:
        """
        Load the configuration for the specified environment.
        Environment is determined by the TEST_ENV environment variable.
        """
        env = os.getenv('TEST_ENV', cls.DEFAULT_ENV).lower()
        
        if env not in cls.VALID_ENVIRONMENTS:
            raise ValueError(
                f"Invalid environment: {env}. "
                f"Must be one of: {', '.join(cls.VALID_ENVIRONMENTS)}"
            )
        
        try:
            config_module = importlib.import_module(f'tests.config.environments.{env}')
            return config_module
        except ImportError as e:
            raise ImportError(f"Failed to load configuration for environment: {env}") from e

    @classmethod
    def get_current_env(cls) -> str:
        """Get the current environment name."""
        return os.getenv('TEST_ENV', cls.DEFAULT_ENV).lower()

# Create a singleton instance
config = ConfigLoader.load_config() 