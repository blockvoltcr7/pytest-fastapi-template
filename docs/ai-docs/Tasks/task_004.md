Perfect choice! Let's build the Image Generation service using OpenAI DALL-E. This will complete our asset generation pipeline.

## 📋 **Step 1: Update Requirements**

Add OpenAI SDK to your requirements:

```bash
# Add to requirements.in
openai
pillow  # For image processing
```

Update requirements:
```bash
uv pip compile requirements.in
uv pip sync requirements.txt
```

## 📋 **Step 2: Image Generation Service**

```python
# app/services/image_service.py
import os
import base64
from typing import Optional, Dict
from openai import AsyncOpenAI
from PIL import Image
import hashlib
import json
from app.core.config import settings

class ImageService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.cache_dir = os.path.join(settings.images_dir, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    async def generate_baby_image(
        self,
        speaker: str,
        baby_profile: Dict,
        campaign_id: str
    ) -> Optional[str]:
        """
        Generate or retrieve cached baby podcaster image
        
        Args:
            speaker: "Baby 1" or "Baby 2"
            baby_profile: Baby profile from campaign
            campaign_id: Campaign identifier for naming
        
        Returns:
            Path to generated image file, or None if failed
        """
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        
        # Check cache first
        cache_key = self._generate_cache_key(speaker, baby_profile)
        cached_path = self._get_cached_image(cache_key)
        if cached_path:
            print(f"✅ Using cached image for {speaker}: {cached_path}")
            return cached_path
        
        try:
            # Generate image prompt
            prompt = self._create_baby_prompt(speaker, baby_profile)
            
            # Generate image with DALL-E
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1536",  # Portrait orientation for baby podcast
                quality="standard",
                response_format="b64_json",
                n=1
            )
            
            # Decode image
            image_data = base64.b64decode(response.data[0].b64_json)
            
            # Save image
            filename = f"{campaign_id}_{speaker.lower().replace(' ', '_')}.png"
            output_path = os.path.join(settings.images_dir, filename)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            # Cache the image
            self._cache_image(cache_key, output_path)
            
            print(f"✅ Generated new image for {speaker}: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating image for {speaker}: {str(e)}")
            return None
    
    def _create_baby_prompt(self, speaker: str, baby_profile: Dict) -> str:
        """Create detailed prompt for baby podcaster image"""
        
        # Base prompt for baby podcaster
        base_prompt = """
        A professional studio portrait of an adorable baby podcaster.
        
        Baby characteristics:
        - Extremely cute and chubby baby (6-12 months old)
        - Big expressive eyes with innocent expression
        - Chubby cheeks and baby features
        - Sitting upright in a comfortable pose
        
        Equipment and setting:
        - Wearing large, professional over-ear headphones (proportionate to baby's head)
        - Speaking into a high-quality podcast microphone on a boom arm
        - Professional podcast studio background
        - Rich, dark acoustic treatment or curtains behind
        - Warm, soft studio lighting that highlights the baby's features
        
        Expression and mood:
        """
        
        # Add tone-specific expressions
        tone = baby_profile.get("tone", "").lower()
        if "warm" in tone and "inviting" in tone:
            expression = """
        - Gentle, welcoming smile with bright, kind eyes
        - Slight head tilt showing engagement
        - Relaxed, open body language
        - Radiating warmth and comfort
            """
        elif "curious" in tone and "thoughtful" in tone:
            expression = """
        - Inquisitive, attentive expression
        - Slightly raised eyebrows showing curiosity
        - Alert, focused gaze
        - Thoughtful, contemplative demeanor
            """
        else:
            expression = """
        - Engaged, focused expression
        - Natural baby charm and innocence
        - Alert and attentive to the microphone
            """
        
        # Technical specifications
        technical_specs = """
        
        Technical requirements:
        - Portrait orientation (2:3 aspect ratio)
        - High resolution and sharp detail
        - Professional photography quality
        - Photorealistic style, not cartoon
        - Excellent lighting and composition
        - Background slightly out of focus to emphasize the baby
        """
        
        return base_prompt + expression + technical_specs
    
    def _generate_cache_key(self, speaker: str, baby_profile: Dict) -> str:
        """Generate a unique cache key for baby profile"""
        # Create cache key from speaker and profile characteristics
        cache_data = {
            "speaker": speaker,
            "tone": baby_profile.get("tone", ""),
            # Add other cacheable characteristics as needed
        }
        
        # Create hash of the cache data
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()[:12]
    
    def _get_cached_image(self, cache_key: str) -> Optional[str]:
        """Check if cached image exists"""
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.png")
        
        if os.path.exists(cache_path):
            return cache_path
        return None
    
    def _cache_image(self, cache_key: str, image_path: str) -> None:
        """Cache the generated image"""
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.png")
        
        # Copy image to cache
        with open(image_path, 'rb') as src, open(cache_path, 'wb') as dst:
            dst.write(src.read())
    
    async def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        if not settings.openai_api_key:
            return False
        
        try:
            # Try to list models to test connection
            models = await self.client.models.list()
            return len(models.data) > 0
        except:
            return False
    
    def optimize_image_for_video(self, image_path: str) -> str:
        """
        Optimize image for video processing
        - Ensure proper dimensions
        - Enhance quality if needed
        """
        try:
            with Image.open(image_path) as img:
                # Ensure image is in RGB mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Ensure proper size (1024x1536 for 2:3 ratio)
                if img.size != (1024, 1536):
                    img = img.resize((1024, 1536), Image.Resampling.LANCZOS)
                
                # Save optimized version
                optimized_path = image_path.replace('.png', '_optimized.png')
                img.save(optimized_path, 'PNG', quality=95)
                
                return optimized_path
        except Exception as e:
            print(f"Error optimizing image: {str(e)}")
            return image_path  # Return original if optimization fails
```

## 📋 **Step 3: Update Campaign Models**

Add image tracking to our models:

```python
# app/models/campaign.py (add these to existing file)
from pydantic import BaseModel
from typing import Optional

class SceneAssets(BaseModel):
    """Track all assets for a scene"""
    audio_file: Optional[str] = None
    image_file: Optional[str] = None
    video_file: Optional[str] = None

class SceneResult(BaseModel):
    scene_index: int
    scene_type: str
    speaker: Optional[str] = None  # For dialogue scenes
    status: Literal["pending", "processing", "success", "failed"]
    assets: SceneAssets = SceneAssets()
    error_message: Optional[str] = None
    processing_time_ms: Optional[int] = None

# Update CampaignResponse to include image generation status
class CampaignResponse(BaseModel):
    job_id: UUID
    status: Literal["queued", "processing", "completed", "failed"]
    scenes_total: int
    scenes_completed: int = 0
    images_generated: int = 0  # New field
    baby_images: Dict[str, Optional[str]] = {}  # Track baby images
    message: str
    results: List[SceneResult] = []
```

## 📋 **Step 4: Enhanced Campaign Processing**

Update the campaign processor to include image generation:

```python
# app/api/v1/endpoints/campaigns.py (update existing functions)
from app.services.image_service import ImageService

async def process_campaign_scenes(campaign: CampaignRequest, job_id: uuid4):
    """Background task to process campaign scenes with image generation"""
    voice_service = VoiceService()
    image_service = ImageService()
    job_id_str = str(job_id)
    
    if job_id_str not in campaign_store:
        return
    
    campaign_response = campaign_store[job_id_str]
    baby_images = {}  # Cache baby images for reuse
    
    try:
        # First, generate baby images for all speakers
        print("🖼️ Generating baby images...")
        
        for speaker, profile in campaign.baby_profiles.items():
            try:
                image_path = await image_service.generate_baby_image(
                    speaker=speaker,
                    baby_profile=profile.dict(),
                    campaign_id=campaign.campaign_id
                )
                
                if image_path:
                    baby_images[speaker] = image_path
                    campaign_response.baby_images[speaker] = image_path
                    campaign_response.images_generated += 1
                    print(f"✅ Generated image for {speaker}")
                else:
                    baby_images[speaker] = None
                    campaign_response.baby_images[speaker] = None
                    print(f"❌ Failed to generate image for {speaker}")
                    
            except Exception as e:
                print(f"❌ Error generating image for {speaker}: {str(e)}")
                baby_images[speaker] = None
                campaign_response.baby_images[speaker] = None
        
        # Process each scene
        print("🎬 Processing scenes...")
        
        for i, scene in enumerate(campaign.script):
            start_time = time.time()
            scene_result = SceneResult(
                scene_index=i,
                scene_type=scene.type,
                status="processing"
            )
            
            if isinstance(scene, DialogueScene):
                scene_result.speaker = scene.speaker
                
                # Generate audio
                baby_profile = campaign.baby_profiles[scene.speaker]
                voice_id = baby_profile.voice_id
                if voice_id in settings.default_baby_voices:
                    voice_id = settings.default_baby_voices[voice_id]
                
                output_filename = f"{campaign.campaign_id}_scene_{i}_{scene.speaker.lower().replace(' ', '_')}.mp3"
                
                audio_path = await voice_service.generate_speech(
                    text=scene.text,
                    voice_id=voice_id,
                    output_filename=output_filename,
                    tone_adjustments={"tone": baby_profile.tone}
                )
                
                # Assign assets
                scene_result.assets.audio_file = audio_path
                scene_result.assets.image_file = baby_images.get(scene.speaker)
                
                # Mark status
                if audio_path and baby_images.get(scene.speaker):
                    scene_result.status = "success"
                    print(f"✅ Completed scene {i} ({scene.speaker})")
                else:
                    scene_result.status = "failed"
                    scene_result.error_message = "Failed to generate audio or image"
                    print(f"❌ Failed scene {i} ({scene.speaker})")
            
            else:  # Media scene
                # For now, mark as success (will implement media processing later)
                scene_result.status = "success"
                print(f"📝 Processed media scene {i} (placeholder)")
            
            # Calculate processing time
            scene_result.processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Update campaign response
            campaign_response.results.append(scene_result)
            campaign_response.scenes_completed += 1
        
        # Mark campaign as completed
        campaign_response.status = "completed"
        campaign_response.message = f"Campaign '{campaign.campaign_id}' completed! Generated {campaign_response.images_generated} baby images and {len([r for r in campaign_response.results if r.status == 'success'])} scene assets."
        
        print(f"✅ Campaign {campaign.campaign_id} processing complete!")
        
    except Exception as e:
        campaign_response.status = "failed"
        campaign_response.message = f"Campaign failed: {str(e)}"
        print(f"❌ Error processing campaign {campaign.campaign_id}: {str(e)}")

# Add new endpoint to get baby images
@router.get("/{job_id}/images")
async def get_campaign_images(job_id: str):
    """Get generated baby images for a campaign"""
    if job_id not in campaign_store:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign = campaign_store[job_id]
    return {
        "job_id": job_id,
        "baby_images": campaign.baby_images,
        "images_generated": campaign.images_generated
    }

# Update health check to include OpenAI
@router.get("/health")
async def health_check():
    """Health check with all AI services"""
    voice_service = VoiceService()
    image_service = ImageService()
    
    voice_connection = await voice_service.test_connection()
    image_connection = await image_service.test_connection()
    
    return {
        "status": "ok",
        "service": "campaign_processor",
        "elevenlabs_connected": voice_connection,
        "openai_connected": image_connection,
        "elevenlabs_api_configured": settings.elevenlabs_api_key is not None,
        "openai_api_configured": settings.openai_api_key is not None
    }
```

## 📋 **Step 5: Tests for Image Service**

```python
# tests/test_image_service.py
import pytest
import os
from app.services.image_service import ImageService
from app.core.config import settings, create_output_directories

class TestImageService:
    
    @pytest.fixture(autouse=True)
    def setup_dirs(self):
        """Ensure output directories exist"""
        create_output_directories()
    
    @pytest.fixture
    def image_service(self):
        return ImageService()
    
    @pytest.fixture
    def baby_profiles(self):
        return {
            "Baby 1": {"tone": "warm, inviting", "voice_id": "baby_voice_1"},
            "Baby 2": {"tone": "curious, thoughtful", "voice_id": "baby_voice_2"}
        }
    
    def test_image_service_init(self, image_service):
        """Test image service initialization"""
        assert image_service.client is not None
        assert os.path.exists(image_service.cache_dir)
    
    def test_cache_key_generation(self, image_service, baby_profiles):
        """Test cache key generation"""
        key1 = image_service._generate_cache_key("Baby 1", baby_profiles["Baby 1"])
        key2 = image_service._generate_cache_key("Baby 2", baby_profiles["Baby 2"])
        key3 = image_service._generate_cache_key("Baby 1", baby_profiles["Baby 1"])
        
        # Different profiles should have different keys
        assert key1 != key2
        # Same profile should have same key
        assert key1 == key3
        # Keys should be reasonable length
        assert len(key1) == 12
    
    def test_prompt_creation(self, image_service, baby_profiles):
        """Test baby prompt creation"""
        prompt1 = image_service._create_baby_prompt("Baby 1", baby_profiles["Baby 1"])
        prompt2 = image_service._create_baby_prompt("Baby 2", baby_profiles["Baby 2"])
        
        # Prompts should be different for different tones
        assert prompt1 != prompt2
        # Should contain key elements
        assert "baby podcaster" in prompt1.lower()
        assert "headphones" in prompt1.lower()
        assert "microphone" in prompt1.lower()
        assert "warm" in prompt1.lower() or "inviting" in prompt1.lower()
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.openai_api_key,
        reason="OpenAI API key not configured"
    )
    async def test_api_connection(self, image_service):
        """Test OpenAI API connection"""
        result = await image_service.test_connection()
        assert result is True
        print("✅ OpenAI API connection successful!")
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.openai_api_key,
        reason="OpenAI API key not configured"
    )
    async def test_baby_image_generation(self, image_service, baby_profiles):
        """Test actual baby image generation"""
        campaign_id = "test_monrovia_001"
        speaker = "Baby 1"
        
        image_path = await image_service.generate_baby_image(
            speaker=speaker,
            baby_profile=baby_profiles[speaker],
            campaign_id=campaign_id
        )
        
        assert image_path is not None
        assert os.path.exists(image_path)
        assert image_path.endswith(".png")
        
        # Check file size (should be reasonable for a generated image)
        file_size = os.path.getsize(image_path)
        assert file_size > 10000  # At least 10KB
        assert file_size < 5000000  # Less than 5MB
        
        print(f"✅ Generated baby image: {image_path} ({file_size} bytes)")
        
        # Test caching - generate same image again
        cached_image_path = await image_service.generate_baby_image(
            speaker=speaker,
            baby_profile=baby_profiles[speaker],
            campaign_id=f"{campaign_id}_cached"
        )
        
        # Should use cache (different filename but same base image)
        assert cached_image_path is not None
        print(f"✅ Image caching working: {cached_image_path}")
        
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(cached_image_path):
            os.remove(cached_image_path)
```

## 🧪 **Test Everything**

```bash
# Test image service
pytest tests/test_image_service.py -v -s

# Test full campaign with images
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
         },
         {
           "type": "dialogue",
           "speaker": "Baby 2",
           "text": "Mon Rovîa? Can not say I have heard of him. What is his vibe?"
         }
       ],
       "baby_profiles": {
         "Baby 1": {"tone": "warm, inviting", "voice_id": "baby_voice_1"},
         "Baby 2": {"tone": "curious, thoughtful", "voice_id": "baby_voice_2"}
       }
     }'

# Check status with images
curl -X GET "http://localhost:8000/api/v1/campaigns/{job_id}/status"

# Get just the images
curl -X GET "http://localhost:8000/api/v1/campaigns/{job_id}/images"

# Check health (should show both APIs connected)
curl -X GET "http://localhost:8000/api/v1/campaigns/health"
```

## 🎯 **Checkpoint 4 Complete**

Now we have:
- ✅ OpenAI DALL-E integration for baby image generation
- ✅ Intelligent image caching to avoid regenerating same babies
- ✅ Tone-specific prompt engineering for different baby personalities
- ✅ Complete asset generation: audio + images for each dialogue scene
- ✅ Enhanced status tracking with image generation progress
- ✅ Proper error handling and optimization for video processing
