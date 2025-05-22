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
        """Optimize an image for video processing if needed"""
        try:
            # This method could resize, compress, or format the image for video processing
            # For now, just return the original path
            return image_path
        except Exception as e:
            print(f"❌ Error optimizing image: {str(e)}")
            return image_path 