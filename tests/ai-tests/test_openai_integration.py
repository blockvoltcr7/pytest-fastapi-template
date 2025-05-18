import allure
import pytest
import os
from openai import OpenAI

@allure.epic("AI Integration")
@allure.feature("OpenAI API")
class TestOpenAIIntegration:
    
    @pytest.fixture
    def openai_client(self):
        """Create an OpenAI client for testing."""
        with allure.step("Initialize OpenAI client"):
            client = OpenAI()
            return client
    
    @allure.story("Basic API Response")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_openai_response(self, openai_client):
        """Test that OpenAI API returns a valid response."""
        
        prompt = "hello world"
        
        with allure.step(f"Send request to OpenAI with prompt: '{prompt}'"):
            try:
                response = openai_client.responses.create(
                    model="gpt-4.1",
                    input=prompt
                )
                
                allure.attach(
                    str(response),
                    name="Raw Response Object",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                allure.attach(
                    str(e),
                    name="API Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.fail(f"OpenAI API request failed: {str(e)}")
        
        with allure.step("Verify response contains output text"):
            assert hasattr(response, "output_text"), "Response missing output_text attribute"
            
            output_text = response.output_text
            allure.attach(
                output_text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert isinstance(output_text, str), "Output text is not a string"
            assert len(output_text) > 0, "Output text is empty"
            
            print(f"OpenAI Response: {output_text}") 