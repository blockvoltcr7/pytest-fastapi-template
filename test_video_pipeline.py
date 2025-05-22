#!/usr/bin/env python
"""
Simple standalone script to test the video generation pipeline
"""
import asyncio
import os
import time
from app.core.config import settings, create_output_directories
from app.services.voice_service import VoiceService
from app.services.image_service import ImageService
from app.services.video_service import VideoService

async def test_pipeline():
    """Test the complete video generation pipeline"""
    
    print("Setting up...")
    create_output_directories()
    voice_service = VoiceService()
    image_service = ImageService()
    video_service = VideoService()
    
    # Print API key status
    print("\n==== API Configuration ====")
    print(f"ElevenLabs API Key configured: {'*****' + settings.elevenlabs_api_key[-4:] if settings.elevenlabs_api_key else 'Not set'}")
    print(f"OpenAI API Key configured: {'*****' + settings.openai_api_key[-4:] if settings.openai_api_key else 'Not set'}")
    print(f"Hedra API Key configured: {'*****' + settings.hedra_api_key[-4:] if settings.hedra_api_key else 'Not set'}")
    
    # Test data
    test_text = "Hello, this is a test of the baby podcast video generation pipeline!"
    test_speaker = "Baby 1"
    timestamp = int(time.time())
    test_campaign_id = f"pipeline_test_{timestamp}"
    
    # Step 1: Test connections
    print("\n==== Testing API Connections ====")
    
    print("Testing ElevenLabs connection...")
    voice_connection = await voice_service.test_connection()
    if not voice_connection:
        print("❌ ElevenLabs connection failed!")
        return False
    print("✅ ElevenLabs connection successful")
    
    print("Testing OpenAI connection...")
    image_connection = await image_service.test_connection()
    if not image_connection:
        print("❌ OpenAI connection failed!")
        return False
    print("✅ OpenAI connection successful")
    
    print("Testing Hedra connection...")
    try:
        video_connection = await video_service.test_connection()
        if not video_connection:
            print("❌ Hedra connection failed!")
            return False
        print("✅ Hedra connection successful")
    except Exception as e:
        print(f"❌ Hedra connection error: {str(e)}")
        return False
    
    # Step 2: Generate audio
    print("\n==== Generating Audio ====")
    try:
        audio_path = await voice_service.generate_speech(
            text=test_text,
            voice_id=settings.default_baby_voices["baby_voice_1"],
            output_filename=f"{test_campaign_id}_audio.mp3",
            tone_adjustments={"tone": "warm, inviting"}
        )
        if not audio_path or not os.path.exists(audio_path):
            print(f"❌ Audio generation failed!")
            return False
        print(f"✅ Audio generated: {audio_path}")
    except Exception as e:
        print(f"❌ Audio generation error: {str(e)}")
        return False
    
    # Step 3: Generate image
    print("\n==== Generating Image ====")
    try:
        baby_profile = {"tone": "warm, inviting", "voice_id": settings.default_baby_voices["baby_voice_1"]}
        image_path = await image_service.generate_baby_image(
            speaker=test_speaker,
            baby_profile=baby_profile,
            campaign_id=test_campaign_id
        )
        if not image_path or not os.path.exists(image_path):
            print(f"❌ Image generation failed!")
            return False
        print(f"✅ Image generated: {image_path}")
    except Exception as e:
        print(f"❌ Image generation error: {str(e)}")
        return False
    
    # Step 4: Generate video
    print("\n==== Generating Video ====")
    try:
        print(f"Starting video generation with:")
        print(f"  Audio: {audio_path}")
        print(f"  Image: {image_path}")
        print(f"  Speaker: {test_speaker}")
        print(f"  Campaign ID: {test_campaign_id}")
        
        video_path = await video_service.create_lipsync_video(
            audio_path=audio_path,
            image_path=image_path,
            scene_index=1,
            speaker=test_speaker,
            campaign_id=test_campaign_id
        )
        
        if not video_path or not os.path.exists(video_path):
            print(f"❌ Video generation failed!")
            return False
        
        video_size = os.path.getsize(video_path)
        if video_size < 10000:
            print(f"❌ Video file too small: {video_size} bytes")
            return False
            
        print(f"✅ Video generated: {video_path} ({video_size:,} bytes)")
        
        # Final success message
        print("\n🎉 Complete pipeline test successful!")
        print(f"Final outputs:\nAudio: {audio_path}\nImage: {image_path}\nVideo: {video_path}")
        return True
        
    except Exception as e:
        print(f"❌ Video generation error: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_pipeline())
    exit(0 if success else 1) 