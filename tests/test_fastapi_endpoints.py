import allure
import pytest
import requests

@allure.epic("Core API")
@allure.feature("API Tests")
@allure.suite("smoke_tests")
@pytest.mark.api
@pytest.mark.smoke
class TestFastAPIEndpoints:

    @allure.story("Root Endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_root_endpoint(self, session, api_base_url):
        """Test the root endpoint returns the correct welcome message"""

        with allure.step(f"Send GET request to root endpoint {api_base_url}/"):
            response = session.get(f"{api_base_url}/")

        with allure.step("Verify successful status code"):
            assert response.status_code == 200
            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Parse JSON response"):
            data = response.json()
            allure.attach(
                str(data),
                name="Response JSON",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify correct welcome message"):
            assert "message" in data
            assert data["message"] == "GenAI API"


    @allure.story("Hello World Endpoint")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hello_endpoint(self, session, api_base_url):
        """Test the hello endpoint returns the correct greeting message"""

        with allure.step(f"Send GET request to hello endpoint {api_base_url}/api/v1/hello"):
            response = session.get(f"{api_base_url}/api/v1/hello")

        with allure.step("Verify successful status code"):
            assert response.status_code == 200
            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Parse JSON response"):
            data = response.json()
            allure.attach(
                str(data),
                name="Response JSON",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify correct hello message"):
            assert "message" in data
            assert data["message"] == "Hello World"