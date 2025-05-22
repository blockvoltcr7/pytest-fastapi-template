import pytest
import os
import asyncio
from app.services.voice_service import VoiceService
from app.services.image_service import ImageService
from app.services.video_service import VideoService
from app.core.config import settings, create_output_directories

@pytest.mark.asyncio
@pytest.mark.skipif(
    not all([settings.hedra_api_key, settings.elevenlabs_api_key, settings.openai_api_key]),
    reason="All API keys required for integration test"
)
async def test_simplified_pipeline():
    """
    Test the complete pipeline without Allure reporting:
    1. Generate audio with ElevenLabs
    2. Generate image with OpenAI
    3. Create lip-sync video with Hedra
    """
    # Setup
    create_output_directories()
    voice_service = VoiceService()
    image_service = ImageService()
    video_service = VideoService()
    
    # Test data
    test_text = "Hello, this is a test of the baby podcast video generation pipeline!"
    test_speaker = "Baby 1"
    test_campaign_id = f"simple_test_{int(asyncio.get_event_loop().time())}"
    
    # Step 1: Test connections
    print("\n==== Testing API Connections ====")
    
    print("Testing ElevenLabs connection...")
    voice_connection = await voice_service.test_connection()
    assert voice_connection, "ElevenLabs connection failed"
    print("✅ ElevenLabs connection successful")
    
    print("Testing OpenAI connection...")
    image_connection = await image_service.test_connection()
    assert image_connection, "OpenAI connection failed"
    print("✅ OpenAI connection successful")
    
    print("Testing Hedra connection...")
    video_connection = await video_service.test_connection()
    assert video_connection, "Hedra connection failed"
    print("✅ Hedra connection successful")
    
    # Step 2: Generate audio
    print("\n==== Generating Audio ====")
    audio_path = await voice_service.generate_speech(
        text=test_text,
        voice_id=settings.default_baby_voices["baby_voice_1"],
        output_filename=f"{test_campaign_id}_audio.mp3",
        tone_adjustments={"tone": "warm, inviting"}
    )
    assert audio_path is not None, "Audio generation failed"
    assert os.path.exists(audio_path), f"Audio file not found at {audio_path}"
    print(f"✅ Audio generated: {audio_path}")
    
    # Step 3: Generate image
    print("\n==== Generating Image ====")
    baby_profile = {"tone": "warm, inviting", "voice_id": settings.default_baby_voices["baby_voice_1"]}
    image_path = await image_service.generate_baby_image(
        speaker=test_speaker,
        baby_profile=baby_profile,
        campaign_id=test_campaign_id
    )
    assert image_path is not None, "Image generation failed"
    assert os.path.exists(image_path), f"Image file not found at {image_path}"
    print(f"✅ Image generated: {image_path}")
    
    # Step 4: Generate video
    print("\n==== Generating Video ====")
    video_path = await video_service.create_lipsync_video(
        audio_path=audio_path,
        image_path=image_path,
        scene_index=1,
        speaker=test_speaker,
        campaign_id=test_campaign_id
    )
    
    # Verify video was created
    assert video_path is not None, "Video generation failed"
    assert os.path.exists(video_path), f"Video file not found at {video_path}"
    video_size = os.path.getsize(video_path)
    assert video_size > 10000, f"Video file too small ({video_size} bytes)"
    print(f"✅ Video generated: {video_path} ({video_size:,} bytes)")
    
    # Final success message
    print("\n🎉 Complete pipeline test successful!")
    print(f"Final outputs:\nAudio: {audio_path}\nImage: {image_path}\nVideo: {video_path}") 