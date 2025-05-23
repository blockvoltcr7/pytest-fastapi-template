from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings using Pydantic."""
    
    # API Keys
    openai_api_key: str = ""
    elevenlabs_api_key: str = ""
    
    # Directory paths
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    images_dir: Path = base_dir / "output" / "images"
    audio_dir: Path = base_dir / "output" / "audio"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Ensure output directories exist
os.makedirs(settings.images_dir, exist_ok=True)
os.makedirs(settings.audio_dir, exist_ok=True) 