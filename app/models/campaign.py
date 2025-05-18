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
    
    @field_validator('script')
    @classmethod
    def script_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Script must contain at least one scene')
        return v

class CampaignResponse(BaseModel):
    job_id: UUID
    status: Literal["queued", "processing", "completed", "failed"]
    scenes_total: int
    message: str 