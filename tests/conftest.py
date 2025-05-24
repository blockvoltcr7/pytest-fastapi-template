"""
This file (conftest.py) is a special configuration file for pytest that contains fixtures and hooks
that are automatically discovered and used by pytest. It's used to set up test infrastructure and
provide common functionality across all test files.

Key features:
- Configures Allure reporting environment
- Captures test failures and exceptions
- Provides reusable HTTP session for API testing
- Defines common test fixtures

The file is automatically loaded by pytest before running any tests.
"""

import os
import pytest
import allure
import requests
from datetime import datetime
from dotenv import load_dotenv
from tests.config.config_loader import config

# Load environment variables from .env file
load_dotenv()

# Environment info for the Allure report
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Set up the Allure environment information.

    This hook runs before any tests and creates an environment.properties file
    in the Allure results directory containing system and package information.
    This information is displayed in the Allure report.
    """
    allure_dir = config.getoption('--alluredir')
    if allure_dir:
        if not os.path.exists(allure_dir):
            os.makedirs(allure_dir)

        env_file = os.path.join(allure_dir, 'environment.properties')
        with open(env_file, 'w') as f:
            f.write(f'Python.Version={pytest.__version__}\n')
            f.write(f'Platform={os.name}\n')
            f.write(f'Timestamp={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Requests.Version={requests.__version__}\n')
            # Get package version for allure-pytest
            try:
                from importlib.metadata import version
                allure_version = version("allure-pytest")
                f.write(f'Allure.Version={allure_version}\n')
            except:
                pass

# Add an Allure step for each error log
@pytest.hookimpl(trylast=True)
def pytest_exception_interact(node, call, report):
    """
    Capture exceptions for Allure reporting.

    This hook runs when a test fails and attaches the exception details
    to the Allure report for better debugging and visibility.
    """
    if report.failed:
        allure.attach(
            str(call.excinfo.value),
            name="Exception",
            attachment_type=allure.attachment_type.TEXT
        )

# HTTP session fixture for API testing
@pytest.fixture
@allure.title("HTTP Session")
def session():
    """
    Create a requests session for API testing.

    This fixture provides a pre-configured requests.Session object with common headers
    for all API tests. The session is automatically closed after each test.

    Returns:
        requests.Session: A configured session object for making HTTP requests
    """
    with allure.step("Create requests session"):
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Allure-Pytest-API-Testing",
            "Accept": "application/json"
        })
        yield session

    # Cleanup step
    with allure.step("Close requests session"):
        session.close()

# API Base URL fixture using configuration
@pytest.fixture(scope="session")
@allure.title("API Base URL")
def api_base_url():
    """
    Get the API base URL from the current environment configuration.
    
    This fixture assumes the FastAPI server is already running and uses the
    configured base URL for the current test environment (dev/uat/prod).
    
    Returns:
        str: The base URL for the API server
    """
    base_url = getattr(config, 'API_BASE_URL', 'http://localhost:8000')
    
    with allure.step(f"Using API base URL: {base_url}"):
        allure.attach(
            base_url,
            name="API Base URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    return base_url

# OpenAI client fixture
@pytest.fixture(scope="session")
@allure.title("OpenAI Client")
def openai_client():
    """
    Create an OpenAI client with API key from environment variables.
    
    This fixture loads the OPENAI_API_KEY from the .env file and creates
    a properly configured OpenAI client for testing.
    
    Returns:
        OpenAI: A configured OpenAI client instance
    """
    from openai import OpenAI
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        pytest.skip("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")
    
    with allure.step("Initialize OpenAI client with API key from environment"):
        client = OpenAI(api_key=api_key)
        allure.attach(
            "OpenAI client initialized successfully",
            name="OpenAI Client Status",
            attachment_type=allure.attachment_type.TEXT
        )
    
    return client