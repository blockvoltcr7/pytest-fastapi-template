Perfect! Using the official ElevenLabs SDK is much cleaner. Let's update the voice service to use the SDK instead of raw HTTP requests.

## 📋 **Step 1: Update Requirements**

First, add the ElevenLabs SDK to your requirements:

```bash
# Add to requirements.in
elevenlabs
python-dotenv
```

Then update your requirements:
```bash
uv pip compile requirements.in
uv pip sync requirements.txt
```

## 📋 **Step 2: Updated Voice Service with SDK**

```python
# app/services/voice_service.py
import os
import aiofiles
from typing import Optional
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from app.core.config import settings

class VoiceService:
    def __init__(self):
        self.client = ElevenLabs(api_key=settings.elevenlabs_api_key)
    
    async def generate_speech(
        self, 
        text: str, 
        voice_id: str, 
        output_filename: str,
        tone_adjustments: Optional[dict] = None
    ) -> Optional[str]:
        """
        Generate speech audio using ElevenLabs SDK
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
            output_filename: Name for the output file (e.g., "scene_0_baby1.mp3")
            tone_adjustments: Optional voice settings adjustments
        
        Returns:
            Path to the generated audio file, or None if failed
        """
        if not settings.elevenlabs_api_key:
            raise ValueError("ElevenLabs API key not configured")
        
        try:
            # Create voice settings based on tone
            voice_settings = self._create_voice_settings(tone_adjustments)
            
            # Generate audio using SDK
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
                voice_settings=voice_settings
            )
            
            # Save audio file
            output_path = os.path.join(settings.audio_dir, output_filename)
            
            # Write audio bytes to file
            with open(output_path, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None
    
    def _create_voice_settings(self, tone_adjustments: Optional[dict] = None) -> VoiceSettings:
        """
        Create voice settings based on baby profile tone
        """
        # Default settings for baby voices
        default_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        # Apply tone-specific adjustments
        if tone_adjustments:
            if tone_adjustments.get("tone") == "warm, inviting":
                default_settings["stability"] = 0.6
                default_settings["style"] = 0.2
            elif tone_adjustments.get("tone") == "curious, thoughtful":
                default_settings["stability"] = 0.4
                default_settings["style"] = 0.1
        
        return VoiceSettings(**default_settings)
    
    async def test_connection(self) -> bool:
        """Test if ElevenLabs API connection works"""
        if not settings.elevenlabs_api_key:
            return False
            
        try:
            # Try to get user info to test connection
            user = self.client.user.get()
            return user is not None
        except:
            return False
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            voices = self.client.voices.get_all()
            return [{"voice_id": v.voice_id, "name": v.name} for v in voices.voices]
        except Exception as e:
            print(f"Error fetching voices: {str(e)}")
            return []
```

## 📋 **Step 3: Enhanced Configuration**

Update your config to handle voice ID mapping:

```python
# app/core/config.py
from pydantic import BaseSettings
from typing import Optional, Dict
import os

class Settings(BaseSettings):
    # App settings
    app_name: str = "Baby Podcast GenAI"
    debug: bool = False
    
    # AI Service API Keys
    elevenlabs_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    hedra_api_key: Optional[str] = None
    
    # Voice ID mappings (you can update these with actual voice IDs)
    default_baby_voices: Dict[str, str] = {
        "baby_voice_1": "pNInz6obpgDQGcFmaJgB",  # Default voice 1
        "baby_voice_2": "ErXwobaYiN019PkySvjV",  # Default voice 2
    }
    
    # Local storage paths
    output_dir: str = "output"
    audio_dir: str = "output/audio"
    images_dir: str = "output/images"
    videos_dir: str = "output/videos"
    final_dir: str = "output/final"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Create output directories on startup
def create_output_directories():
    """Create local output directories if they don't exist"""
    dirs = [
        settings.output_dir,
        settings.audio_dir,
        settings.images_dir,
        settings.videos_dir,
        settings.final_dir
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
```

## 📋 **Step 4: Enhanced Campaign Models**

Let's improve the campaign models to better handle voice configuration:

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
        if len(v) > 1000:  # Reasonable limit for TTS
            raise ValueError('Text too long (max 1000 characters)')
        return v

class MediaScene(BaseModel):
    type: Literal["media"]
    media_kind: str
    description: str

Scene = Union[DialogueScene, MediaScene]

class BabyProfile(BaseModel):
    tone: str
    voice_id: str
    
    # Optional voice customization
    voice_settings: Optional[Dict] = None

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
    
    @validator('baby_profiles')
    def validate_baby_profiles(cls, v):
        if "Baby 1" not in v or "Baby 2" not in v:
            raise ValueError('Both Baby 1 and Baby 2 profiles are required')
        return v

class SceneResult(BaseModel):
    scene_index: int
    scene_type: str
    status: Literal["success", "failed"]
    output_file: Optional[str] = None
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None

class CampaignResponse(BaseModel):
    job_id: UUID
    status: Literal["queued", "processing", "completed", "failed"]
    scenes_total: int
    scenes_completed: int = 0
    message: str
    results: List[SceneResult] = []
```

## 📋 **Step 5: Updated Campaign Processing**

```python
# app/api/v1/endpoints/campaigns.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List
from uuid import uuid4
import time
from app.models.campaign import CampaignRequest, CampaignResponse, DialogueScene, SceneResult
from app.services.voice_service import VoiceService
from app.core.config import create_output_directories, settings

router = APIRouter()

# Store campaign results in memory (in production, use database)
campaign_store: Dict[str, CampaignResponse] = {}

@router.post("/generate", response_model=CampaignResponse)
async def generate_campaign(
    campaign: CampaignRequest, 
    background_tasks: BackgroundTasks
) -> CampaignResponse:
    """Generate baby podcast from campaign JSON"""
    try:
        create_output_directories()
        
        job_id = uuid4()
        
        # Create initial response
        response = CampaignResponse(
            job_id=job_id,
            status="processing",
            scenes_total=len(campaign.script),
            scenes_completed=0,
            message=f"Campaign '{campaign.campaign_id}' started processing {len(campaign.script)} scenes"
        )
        
        # Store in memory
        campaign_store[str(job_id)] = response
        
        # Start background processing
        background_tasks.add_task(process_campaign_scenes, campaign, job_id)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to start campaign processing: {str(e)}"
        )

@router.get("/{job_id}/status", response_model=CampaignResponse)
async def get_campaign_status(job_id: str) -> CampaignResponse:
    """Get campaign processing status"""
    if job_id not in campaign_store:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return campaign_store[job_id]

async def process_campaign_scenes(campaign: CampaignRequest, job_id: uuid4):
    """Background task to process campaign scenes"""
    voice_service = VoiceService()
    job_id_str = str(job_id)
    
    # Get stored campaign response
    if job_id_str not in campaign_store:
        return
    
    campaign_response = campaign_store[job_id_str]
    
    try:
        for i, scene in enumerate(campaign.script):
            start_time = time.time()
            
            if isinstance(scene, DialogueScene):
                # Get baby profile
                baby_profile = campaign.baby_profiles[scene.speaker]
                
                # Resolve voice ID (check if it's a mapped name)
                voice_id = baby_profile.voice_id
                if voice_id in settings.default_baby_voices:
                    voice_id = settings.default_baby_voices[voice_id]
                
                # Generate speech
                output_filename = f"{campaign.campaign_id}_scene_{i}_{scene.speaker.lower().replace(' ', '_')}.mp3"
                
                audio_path = await voice_service.generate_speech(
                    text=scene.text,
                    voice_id=voice_id,
                    output_filename=output_filename,
                    tone_adjustments={"tone": baby_profile.tone}
                )
                
                # Create scene result
                if audio_path:
                    duration_ms = int((time.time() - start_time) * 1000)
                    scene_result = SceneResult(
                        scene_index=i,
                        scene_type="dialogue",
                        status="success",
                        output_file=audio_path,
                        duration_ms=duration_ms
                    )
                    print(f"✅ Generated audio for scene {i}: {audio_path}")
                else:
                    scene_result = SceneResult(
                        scene_index=i,
                        scene_type="dialogue",
                        status="failed",
                        error_message="Failed to generate audio"
                    )
                    print(f"❌ Failed to generate audio for scene {i}")
                
                # Update campaign response
                campaign_response.results.append(scene_result)
                campaign_response.scenes_completed += 1
                
            else:  # Media scene
                # For now, just mark as completed
                scene_result = SceneResult(
                    scene_index=i,
                    scene_type="media",
                    status="success",
                    output_file=None  # Will be implemented later
                )
                campaign_response.results.append(scene_result)
                campaign_response.scenes_completed += 1
                print(f"📝 Processed media scene {i} (placeholder)")
        
        # Mark campaign as completed
        campaign_response.status = "completed"
        campaign_response.message = f"Campaign '{campaign.campaign_id}' completed successfully!"
        
        print(f"✅ Campaign {campaign.campaign_id} processing complete!")
        
    except Exception as e:
        # Mark campaign as failed
        campaign_response.status = "failed"
        campaign_response.message = f"Campaign failed: {str(e)}"
        print(f"❌ Error processing campaign {campaign.campaign_id}: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check with voice service test"""
    voice_service = VoiceService()
    voice_connection = await voice_service.test_connection()
    
    return {
        "status": "ok",
        "service": "campaign_processor",
        "elevenlabs_connected": voice_connection,
        "api_key_configured": settings.elevenlabs_api_key is not None
    }

@router.get("/voices")
async def get_available_voices():
    """Get available ElevenLabs voices"""
    voice_service = VoiceService()
    voices = voice_service.get_available_voices()
    return {
        "voices": voices,
        "default_mappings": settings.default_baby_voices
    }
```

## 📋 **Step 6: Updated Tests**

```python
# tests/test_voice_service_sdk.py
import pytest
import os
from app.services.voice_service import VoiceService
from app.core.config import settings, create_output_directories

class TestVoiceServiceSDK:
    
    @pytest.fixture(autouse=True)
    def setup_dirs(self):
        """Ensure output directories exist"""
        create_output_directories()
    
    @pytest.fixture
    def voice_service(self):
        return VoiceService()
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.elevenlabs_api_key,
        reason="ElevenLabs API key not configured"
    )
    async def test_speech_generation_with_sdk(self, voice_service):
        """Test speech generation using ElevenLabs SDK"""
        test_text = "Yo, I just stumbled upon this artist, Mon Rovîa."
        voice_id = "pNInz6obpgDQGcFmaJgB"  # Free voice
        output_filename = "test_monrovia_scene.mp3"
        
        audio_path = await voice_service.generate_speech(
            text=test_text,
            voice_id=voice_id,
            output_filename=output_filename,
            tone_adjustments={"tone": "warm, inviting"}
        )
        
        assert audio_path is not None
        assert os.path.exists(audio_path)
        
        # Check file size
        file_size = os.path.getsize(audio_path)
        assert file_size > 0
        
        print(f"✅ Generated Mon Rovîa scene audio: {audio_path} ({file_size} bytes)")
        
        # Cleanup
        os.remove(audio_path)
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.elevenlabs_api_key,
        reason="ElevenLabs API key not configured"
    )
    async def test_api_connection_sdk(self, voice_service):
        """Test API connection using SDK"""
        result = await voice_service.test_connection()
        assert result is True
        print("✅ ElevenLabs SDK connection successful!")
    
    @pytest.mark.skipif(
        not settings.elevenlabs_api_key,
        reason="ElevenLabs API key not configured"
    )
    def test_get_voices(self, voice_service):
        """Test getting available voices"""
        voices = voice_service.get_available_voices()
        assert isinstance(voices, list)
        if voices:  # If voices are returned
            assert "voice_id" in voices[0]
            assert "name" in voices[0]
            print(f"✅ Found {len(voices)} available voices")
```

## 🧪 **Test the Updated Voice Service**

```bash
# Test the SDK-based voice service
pytest tests/test_voice_service_sdk.py -v -s

# Test the full campaign API
curl -X POST "http://localhost:8000/api/v1/campaigns/generate" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'

# Check status (replace with actual job_id from response)
curl -X GET "http://localhost:8000/api/v1/campaigns/{job_id}/status"

# Check available voices
curl -X GET "http://localhost:8000/api/v1/campaigns/voices"
```

## 🎯 **Checkpoint 3 Complete**

Now we have:
- ✅ ElevenLabs SDK integration (much cleaner than raw HTTP)
- ✅ Voice ID mapping and configuration
- ✅ Tone-based voice settings
- ✅ Background processing with status tracking
- ✅ Proper error handling and file management
- ✅ Real audio generation from Mon Rovîa dialogue

The voice generation is now much more robust and easier to maintain! Ready to add the next component?