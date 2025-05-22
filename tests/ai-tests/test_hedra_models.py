import allure
import pytest
import requests
import os
from typing import List, Optional
from pydantic import BaseModel, Field

# Define the model schema based on the API response
class HedraModel(BaseModel):
    id: str
    name: str
    description: str
    type: str
    requires_start_frame: Optional[bool] = Field(default=False)
    requires_audio_input: Optional[bool] = Field(default=False)
    custom_resolution: Optional[bool] = Field(default=False)

@allure.epic("AI Services")
@allure.feature("Hedra API")
class TestHedraModels:
    
    @pytest.fixture
    def api_key(self):
        """Get Hedra API key from environment variables."""
        with allure.step("Get Hedra API key"):
            api_key = os.environ.get("HEDRA_API_KEY")
            if not api_key:
                pytest.skip("HEDRA_API_KEY environment variable not set")
            return api_key
    
    @pytest.fixture
    def hedra_base_url(self):
        """Return the base URL for Hedra API."""
        return "https://api.hedra.com"
    
    @allure.story("Model Listing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_models(self, session, hedra_base_url, api_key):
        """Test that we can successfully list available models from Hedra API."""
        
        with allure.step("Set up API request headers"):
            session.headers.update({
                "X-API-Key": api_key
            })
        
        with allure.step("Send request to list models"):
            endpoint = f"{hedra_base_url}/web-app/public/models"
            response = session.get(endpoint)
            
            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Verify response status code"):
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        with allure.step("Verify response content type"):
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"Expected application/json content type, got {content_type}"
        
        with allure.step("Verify response contains models"):
            models_data = response.json()
            assert isinstance(models_data, list), "Response should be a list of models"
            assert len(models_data) > 0, "No models returned in the response"
            
            # Validate the first model against our schema
            if models_data:
                model = models_data[0]
                
                # Log the received model data for debugging
                allure.attach(
                    str(model),
                    name="Raw Model Data",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                validated_model = HedraModel(
                    id=model.get("id"),
                    name=model.get("name"),
                    description=model.get("description"),
                    type=model.get("type"),
                    requires_start_frame=model.get("requires_start_frame"),
                    requires_audio_input=model.get("requires_audio_input"),
                    custom_resolution=model.get("custom_resolution")
                )
                
                allure.attach(
                    str(validated_model.model_dump()),
                    name="Validated Model",
                    attachment_type=allure.attachment_type.JSON
                )
                
                assert validated_model.id, "Model ID should not be empty"
                assert validated_model.name, "Model name should not be empty"
                assert validated_model.type, "Model type should not be empty" 