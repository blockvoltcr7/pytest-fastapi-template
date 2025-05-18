import allure
import pytest
import requests

@allure.epic("FastAPI Application")
@allure.feature("API Endpoints")
@pytest.mark.api
class TestFastAPIEndpoints:
    
    @pytest.fixture
    def api_base_url(self):
        """Override the base URL to use the local FastAPI server"""
        return "http://localhost:8080"
    
    @allure.story("Root Endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_root_endpoint(self, session, api_base_url, fastapi_server):
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
            assert data["message"] == "Welcome to Baby Podcast GenAI API"
    
    @allure.story("Hello World Endpoint")
    @allure.severity(allure.severity_level.NORMAL)
    def test_hello_endpoint(self, session, api_base_url, fastapi_server):
        """Test the hello endpoint returns the correct greeting message"""
        
        with allure.step(f"Send GET request to hello endpoint {api_base_url}/api/v1/items/hello"):
            response = session.get(f"{api_base_url}/api/v1/items/hello")
        
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