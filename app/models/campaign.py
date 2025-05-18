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