"""
This is just a sample test showing how to use Allure annotations to generate a report.

Please replace this test with your own test code.

Allure annotations are used to generate a test report that provides detailed information
about the test, including the test's name, description, steps, and attachments.

The report can be served with the Allure server, which can be started with the following command:

    $ allure serve

This will start the Allure server and open a web browser to view the report.

For more information about Allure, see the Allure documentation: https://docs.qameta.io/allure/
"""

import allure
import pytest


@pytest.mark.skip(reason="Test disabled")
@allure.epic("Core API")
@allure.feature("API Tests")
@allure.suite("smoke_tests")
@allure.story("Basic Testing")
@pytest.mark.api
@pytest.mark.smoke
def test_hello_world():
    with allure.step("Create hello world message"):
        message = "Hello, world!"

    with allure.step("Verify message content"):
        assert message == "Hello, world!"
        allure.attach(message, name="Greeting Message", attachment_type=allure.attachment_type.TEXT)
