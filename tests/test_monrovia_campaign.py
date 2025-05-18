import pytest
import allure
from app.models.campaign import CampaignRequest

@allure.epic("Models")
@allure.feature("Campaign Model")
class TestMonRoviaCampaign:
    
    @pytest.fixture
    def monrovia_json(self):
        """The exact Mon Rovîa JSON structure"""
        return {
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
                    "type": "dialogue",
                    "speaker": "Baby 1",
                    "text": "It's this soulful blend of folk and introspection. Think gentle guitar strums and lyrics that make you reflect. Here, let me play a snippet."
                },
                {
                    "type": "media",
                    "media_kind": "music_clip",
                    "description": "Clip of Mon Rovîa's 'Crooked the Road'"
                },
                {
                    "type": "dialogue",
                    "speaker": "Baby 2",
                    "text": "Wow, that's deep. It's like he's narrating a journey through life's ups and downs."
                },
                {
                    "type": "dialogue",
                    "speaker": "Baby 1",
                    "text": "Exactly! His songs touch on themes of healing and finding one's path."
                },
                {
                    "type": "dialogue",
                    "speaker": "Baby 2",
                    "text": "I'm definitely adding him to my playlist. For those tuning in, check out Mon Rovîa on Spotify and let his music guide your day."
                }
            ],
            "baby_profiles": {
                "Baby 1": {"tone": "warm, inviting", "voice_id": "baby_voice_1"},
                "Baby 2": {"tone": "curious, thoughtful", "voice_id": "baby_voice_2"}
            }
        }
    
    @allure.story("Basic Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_monrovia_campaign_validation(self, monrovia_json):
        """Test that Mon Rovîa JSON is properly parsed"""
        with allure.step("Parse JSON into campaign model"):
            campaign = CampaignRequest(**monrovia_json)
        
        with allure.step("Verify campaign properties"):
            assert campaign.campaign_id == "monroviaboy_baby_podcast_001"
            assert len(campaign.script) == 7
            assert campaign.script[0].type == "dialogue"
            assert campaign.script[3].type == "media"
            assert campaign.baby_profiles["Baby 1"].tone == "warm, inviting" 