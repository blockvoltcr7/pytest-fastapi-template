from pydantic_settings import BaseSettings
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
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }

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