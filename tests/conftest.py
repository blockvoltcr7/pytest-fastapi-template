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
import time
import subprocess
import signal
import socket
from contextlib import closing
from datetime import datetime

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

# Helper function to check if a port is available
def is_port_available(port):
    """Check if a port is available."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex(('localhost', port)) != 0

# FastAPI server fixture for testing
@pytest.fixture(scope="session")
def fastapi_server():
    """
    Start a FastAPI server for testing and clean it up after tests.

    This fixture starts the FastAPI server on port 8080 before running tests,
    and ensures it's properly shut down after tests complete.
    """
    port = 8080

    # Check if the port is already in use
    if not is_port_available(port):
        pytest.skip(f"Port {port} is already in use, skipping FastAPI tests")

    with allure.step("Start FastAPI server for testing"):
        process = subprocess.Popen(
            ["uvicorn", "app.main:app", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Use process group for proper cleanup
        )

        # Give the server time to start
        time.sleep(2)

        # Check if the server started successfully
        if process.poll() is not None:
            # Server failed to start
            stdout, stderr = process.communicate()
            allure.attach(
                stdout.decode('utf-8'),
                name="Server stdout",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                stderr.decode('utf-8'),
                name="Server stderr",
                attachment_type=allure.attachment_type.TEXT
            )
            pytest.fail("FastAPI server failed to start")

        yield process

    with allure.step("Stop FastAPI server"):
        # Kill the server and its process group
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=5)
        except:
            # If it didn't terminate gracefully, force kill
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except:
                pass