
Let's start simple and build one piece at a time, with tests for each step.

## 📋 **Step 1: Enhanced Models for Mon Rovîa Input**

Let's first improve your existing `app/models/campaign.py` to handle the exact Mon Rovîa JSON:

```python
# app/models/campaign.py
from pydantic import BaseModel, validator
from typing import List, Dict, Literal, Optional, Union
from uuid import UUID, uuid4
from datetime import datetime

class DialogueScene(BaseModel):
    type: Literal["dialogue"]
    speaker: Literal["Baby 1", "Baby 2"]
    text: str
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty')
        return v

class MediaScene(BaseModel):
    type: Literal["media"]
    media_kind: str
    description: str

# Union type for scenes
Scene = Union[DialogueScene, MediaScene]

class BabyProfile(BaseModel):
    tone: str
    voice_id: str

class CampaignRequest(BaseModel):
    campaign_id: str
    topic: str
    script: List[Scene]
    baby_profiles: Dict[Literal["Baby 1", "Baby 2"], BabyProfile]
    
    @validator('script')
    def script_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Script must contain at least one scene')
        return v

class CampaignResponse(BaseModel):
    job_id: UUID
    status: Literal["queued", "processing", "completed", "failed"]
    scenes_total: int
    message: str
```

## 📋 **Step 2: Simple Test First**

Let's create a test that validates the Mon Rovîa JSON:

```python
# tests/test_monrovia_campaign.py
import pytest
from app.models.campaign import CampaignRequest

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
    
    def test_monrovia_campaign_validation(self, monrovia_json):
        """Test that Mon Rovîa JSON is properly parsed"""
        campaign = CampaignRequest(**monrovia_json)
        
        assert campaign.campaign_id == "monroviaboy_baby_podcast_001"
        assert len(campaign.script) == 7
        assert campaign.script[0].type == "dialogue"
        assert campaign.script[3].type == "media"
        assert campaign.baby_profiles["Baby 1"].tone == "warm, inviting"
        
        print("✅ Mon Rovîa JSON validation passed!")
```

**Test this first:**
```bash
pytest tests/test_monrovia_campaign.py -v
```

## 📋 **Step 3: Create Simple Campaign Endpoint**

Now let's add a basic endpoint that accepts the Mon Rovîa JSON:

```python
# app/api/v1/endpoints/campaigns.py
from fastapi import APIRouter, HTTPException
from typing import Dict
from uuid import uuid4
from app.models.campaign import CampaignRequest, CampaignResponse

router = APIRouter()

@router.post("/generate", response_model=CampaignResponse)
async def generate_campaign(campaign: CampaignRequest) -> CampaignResponse:
    """
    Generate baby podcast from campaign JSON
    
    For now, just validates input and returns a job ID
    """
    try:
        # For now, we just validate and return success
        job_id = uuid4()
        
        return CampaignResponse(
            job_id=job_id,
            status="queued",
            scenes_total=len(campaign.script),
            message=f"Campaign '{campaign.campaign_id}' queued for processing with {len(campaign.script)} scenes"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process campaign: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "ok", "service": "campaign_processor"}
```

## 📋 **Step 4: Register the Router**

Update your API router registration:

```python
# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1.endpoints import items, campaigns

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
```

Update main.py if needed:
```python
# app/main.py (make sure this includes the v1 router)
from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(title="Baby Podcast GenAI", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Baby Podcast GenAI API"}
```

## 📋 **Step 5: Test the API Endpoint**

```python
# tests/test_campaign_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

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
    
    def test_campaign_generation_endpoint(self, client, monrovia_json):
        """Test that the campaign endpoint accepts Mon Rovîa JSON"""
        response = client.post("/api/v1/campaigns/generate", json=monrovia_json)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "job_id" in data
        assert data["status"] == "queued"
        assert data["scenes_total"] == 2
        assert "Campaign 'monroviaboy_baby_podcast_001' queued" in data["message"]
        
        print("✅ Campaign API endpoint working!")
    
    def test_campaign_validation_error(self, client):
        """Test validation errors"""
        invalid_data = {
            "campaign_id": "test",
            "topic": "test",
            "script": [],  # Empty script should fail
            "baby_profiles": {}
        }
        
        response = client.post("/api/v1/campaigns/generate", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_health_check(self, client):
        """Test health endpoint"""
        response = client.get("/api/v1/campaigns/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
```

## 🧪 **Test Everything So Far**

Run these tests to make sure we have a solid foundation:

```bash
# Test the models
pytest tests/test_monrovia_campaign.py -v

# Test the API
pytest tests/test_campaign_api.py -v

# Start the server and test manually
uvicorn app.main:app --reload
```

## 📋 **Step 6: Manual Test with cURL**

Create a file `monrovia_test.json`:
```json
{
  "campaign_id": "monroviaboy_baby_podcast_001",
  "topic": "Mon Rovîa music reaction",
  "script": [
    {
      "type": "dialogue",
      "speaker": "Baby 1",
      "text": "Yo, I just stumbled upon this artist, Mon Rovîa."
    }
  ],
  "baby_profiles": {
    "Baby 1": {"tone": "warm, inviting", "voice_id": "baby_voice_1"},
    "Baby 2": {"tone": "curious, thoughtful", "voice_id": "baby_voice_2"}
  }
}
```

Test with cURL:
```bash
curl -X POST "http://localhost:8000/api/v1/campaigns/generate" \
     -H "Content-Type: application/json" \
     -d @monrovia_test.json
```

## 🎯 **Checkpoint 1 Complete**

Once all these tests pass, we'll have:
- ✅ Models that handle Mon Rovîa JSON
- ✅ API endpoint that accepts the input
- ✅ Basic validation and error handling
- ✅ Test coverage for the foundation

**Next steps will be:**
1. Add configuration for API keys
2. Create a simple voice service
3. Test with real ElevenLabs API
4. Add image generation
5. And so on...

Can you run these tests first and confirm everything works? Then we'll add the next piece step by step.