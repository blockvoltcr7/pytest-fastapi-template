🐌 Step-by-Step Approach - Start Small
Let's start with just one simple thing: making sure we can process the Mon Rovîa JSON input and validate it properly.
Step 1: Just Parse and Validate the JSON (That's It!)
First, let's create the absolute minimum:
python# app/models/campaign.py
from pydantic import BaseModel
from typing import List, Dict, Literal

class DialogueScene(BaseModel):
    type: Literal["dialogue"]
    speaker: Literal["Baby 1", "Baby 2"]
    text: str

class MediaScene(BaseModel):
    type: Literal["media"]
    media_kind: str
    description: str

class BabyProfile(BaseModel):
    tone: str
    voice_id: str

class CampaignRequest(BaseModel):
    campaign_id: str
    topic: str
    script: List[dict]  # Let's keep it simple for now
    baby_profiles: Dict[str, BabyProfile]
Test just this one thing:
python# tests/test_basic_parsing.py
import pytest
from app.models.campaign import CampaignRequest

def test_mon_rovia_json_parsing():
    """Just test that we can parse the exact Mon Rovîa JSON"""
    
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
    
    # Can we parse it without errors?
    campaign = CampaignRequest(**mon_rovia_data)
    
    # Basic assertions
    assert campaign.campaign_id == "monroviaboy_baby_podcast_001"
    assert len(campaign.script) == 3
    assert campaign.script[0]["type"] == "dialogue"
    assert campaign.script[2]["type"] == "media"
    
    print("✅ We can parse the Mon Rovîa JSON!")
Let's test just this:
bashpytest tests/test_basic_parsing.py -v -s