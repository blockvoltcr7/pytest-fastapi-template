import allure
import pytest


# @pytest.mark.skip(reason="Test disabled")
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