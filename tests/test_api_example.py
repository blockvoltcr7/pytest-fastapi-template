import allure
import requests
import pytest

@allure.epic("API Testing")
@allure.feature("Sample API")
@pytest.mark.api
class TestSampleAPI:
    
    @pytest.mark.skip(reason="Test disabled")
    @allure.story("Status Endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_status_endpoint(self, session, api_base_url):
        """Test API health endpoint returns 200 OK"""
        with allure.step(f"Send request to status endpoint at {api_base_url}"):
            response = session.get(f'{api_base_url}/status/200')
        
        with allure.step("Verify successful status code"):
            assert response.status_code == 200
    
    @pytest.mark.skip(reason="Test disabled")
    @allure.story("JSON Response")
    @allure.severity(allure.severity_level.NORMAL)
    def test_json_response(self, session, api_base_url):
        """Test API returns expected JSON structure"""
        with allure.step(f"Send request to JSON endpoint at {api_base_url}"):
            response = session.get(f'{api_base_url}/json')
        
        with allure.step("Verify successful status code"):
            assert response.status_code == 200
        
        with allure.step("Parse JSON response"):
            data = response.json()
        
        with allure.step("Verify JSON structure"):
            assert "slideshow" in data
            
            # Attach response data to the report
            allure.attach(
                str(data), 
                name="Response JSON",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @pytest.mark.skip(reason="Test disabled")
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    def test_not_found_response(self, session, api_base_url):
        """Test API handles 404 errors correctly"""
        with allure.step(f"Send request to non-existent endpoint at {api_base_url}"):
            response = session.get(f'{api_base_url}/status/404')
        
        with allure.step("Verify 404 status code"):
            assert response.status_code == 404
            
    @pytest.mark.skip(reason="Test disabled")
    @allure.story("Authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("auth_type", ["basic", "bearer"])
    def test_auth_endpoint(self, session, api_base_url, auth_type):
        """Test API authentication endpoints"""
        allure.dynamic.title(f"Test {auth_type} authentication")
        
        with allure.step(f"Configure {auth_type} authentication"):
            if auth_type == "basic":
                auth = ("user", "passwd")
                url = f"{api_base_url}/basic-auth/user/passwd"
            else:  # bearer
                session.headers["Authorization"] = "Bearer test-token"
                url = f"{api_base_url}/headers"
        
        with allure.step(f"Send authenticated request to {url}"):
            if auth_type == "basic":
                response = session.get(url, auth=auth)
            else:
                response = session.get(url)
                
        with allure.step("Verify successful status code"):
            assert response.status_code == 200
            
        with allure.step("Verify response data"):
            data = response.json()
            allure.attach(
                str(data),
                name=f"{auth_type.capitalize()} Auth Response",
                attachment_type=allure.attachment_type.TEXT
            ) 