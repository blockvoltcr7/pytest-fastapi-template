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