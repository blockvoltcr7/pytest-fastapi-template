import pytest
import allure
from fastapi.testclient import TestClient
from app.main import app

@allure.epic("API")
@allure.feature("Campaign Endpoints")
class TestCampaignAPI:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def monrovia_json(self):
        """Mon Rovîa test data"""
        return {
            "campaign_id": "monroviaboy_baby_podcast_001",
            "topic": "Mon Rovîa music reaction",
            "script": [
                {
                    "type": "dialogue",
                    "speaker": "Baby 1",
                    "text": "Yo, I just stumbled upon this artist, Mon Rovîa."
                },
                {
                    "type": "media",
                    "media_kind": "music_clip",
                    "description": "Clip of Mon Rovîa's 'Crooked the Road'"
                }
            ],
            "baby_profiles": {
                "Baby 1": {"tone": "warm, inviting", "voice_id": "baby_voice_1"},
                "Baby 2": {"tone": "curious, thoughtful", "voice_id": "baby_voice_2"}
            }
        }
    
    @allure.story("Campaign Generation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_campaign_generation_endpoint(self, client, monrovia_json):
        """Test that the campaign endpoint accepts Mon Rovîa JSON"""
        with allure.step("Post campaign request to API"):
            response = client.post("/api/v1/campaigns/generate", json=monrovia_json)
        
        with allure.step("Verify successful response"):
            assert response.status_code == 200
            data = response.json()
            
            assert "job_id" in data
            assert data["status"] == "queued"
            assert data["scenes_total"] == 2
            assert "Campaign 'monroviaboy_baby_podcast_001' queued" in data["message"]
    
    @allure.story("Validation Error")
    @allure.severity(allure.severity_level.NORMAL)
    def test_campaign_validation_error(self, client):
        """Test validation errors"""
        invalid_data = {
            "campaign_id": "test",
            "topic": "test",
            "script": [],  # Empty script should fail
            "baby_profiles": {
                "Baby 1": {"tone": "test", "voice_id": "test"},
                "Baby 2": {"tone": "test", "voice_id": "test"}
            }
        }
        
        with allure.step("Post invalid campaign request"):
            response = client.post("/api/v1/campaigns/generate", json=invalid_data)
        
        with allure.step("Verify validation error response"):
            assert response.status_code == 422  # Validation error
    
    @allure.story("Health Check")
    @allure.severity(allure.severity_level.NORMAL)
    def test_health_check(self, client):
        """Test health endpoint"""
        with allure.step("Request health endpoint"):
            response = client.get("/api/v1/campaigns/health")
        
        with allure.step("Verify health response"):
            assert response.status_code == 200
            assert response.json()["status"] == "ok" 