from pydantic import BaseModel, field_validator
from typing import List, Dict, Literal, Optional, Union
from uuid import UUID, uuid4
from datetime import datetime

class DialogueScene(BaseModel):
    type: Literal["dialogue"]
    speaker: Literal["Baby 1", "Baby 2"]
    text: str
    
    @field_validator('text')
    @classmethod
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

# Union type for scenes
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
    
    @field_validator('script')
    @classmethod
    def script_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Script must contain at least one scene')
        return v
    
    @field_validator('baby_profiles')
    @classmethod
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