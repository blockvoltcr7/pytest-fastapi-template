import pytest
import allure
from app.models.campaign import CampaignRequest

@allure.epic("Core Functionality")
@allure.feature("Data Validation")
class TestBasicParsing:
    
    @allure.story("JSON Parsing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mon_rovia_json_parsing(self):
        """Just test that we can parse the exact Mon Rovîa JSON"""
        
        with allure.step("Prepare Mon Rovîa test data"):
            # This is your exact JSON
            mon_rovia_data = {
                "campaign_id": "monroviaboy_baby_podcast_001",
                "topic": "Mon Rovîa music reaction",
                "script": [
                    {
                        "type": "dialogue",
                        "speaker": "Baby 1",
                        "text": "Yo, I just stumbled upon this artist, Mon Rovîa. His music feels like a warm hug on a cold day."
                    },
                    {
                        "type": "dialogue",
                        "speaker": "Baby 2",
                        "text": "Mon Rovîa? Can't say I've heard of him. What's his vibe?"
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
        
        with allure.step("Parse data with Pydantic model"):
            # Can we parse it without errors?
            campaign = CampaignRequest(**mon_rovia_data)
        
        with allure.step("Verify basic data structure"):
            # Basic assertions
            assert campaign.campaign_id == "monroviaboy_baby_podcast_001"
            assert len(campaign.script) == 3
            assert campaign.script[0]["type"] == "dialogue"
            assert campaign.script[2]["type"] == "media"
            
            print("✅ We can parse the Mon Rovîa JSON!") 