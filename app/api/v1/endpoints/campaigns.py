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
            
            if hasattr(scene, 'type') and scene.type == "dialogue":
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