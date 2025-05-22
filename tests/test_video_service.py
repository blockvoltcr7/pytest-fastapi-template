import pytest
import os
import asyncio
import allure
from app.services.video_service import VideoService
from app.core.config import settings, create_output_directories

@allure.epic("Core Functionality")
@allure.feature("Video Generation")
class TestVideoService:
    
    @allure.story("Basic Functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.hedra_api_key,
        reason="Hedra API key required for this test"
    )
    async def test_connection(self):
        """Test that the Hedra API connection works"""
        with allure.step("Initialize video service"):
            video_service = VideoService()
        
        with allure.step("Test connection to Hedra API"):
            result = await video_service.test_connection()
            assert result is True, "Connection to Hedra API failed"

    @allure.story("Complete Video Generation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not all([settings.hedra_api_key, settings.elevenlabs_api_key, settings.openai_api_key]),
        reason="All API keys required for integration test"
    )
    async def test_complete_video_generation(self):
        """
        Complete integration test - requires actual API keys
        This test will:
        1. Generate a baby image (OpenAI)
        2. Generate voice audio (ElevenLabs)  
        3. Create lip-sync video (Hedra - all steps)
        """
        from app.services.voice_service import VoiceService
        from app.services.image_service import ImageService
        
        with allure.step("Setup test environment"):
            create_output_directories()
            voice_service = VoiceService()
            image_service = ImageService()
            video_service = VideoService()
            
            # Test data
            test_text = "Hello, I'm testing the baby podcast video generation!"
            test_speaker = "Baby 1"
            test_campaign_id = "test_integration_001"
        
        try:
            # Step 1: Generate audio
            with allure.step("Generating test audio"):
                audio_path = await voice_service.generate_speech(
                    text=test_text,
                    voice_id="pNInz6obpgDQGcFmaJgB",  # Free ElevenLabs voice
                    output_filename="test_integration_audio.mp3",
                    tone_adjustments={"tone": "warm, inviting"}
                )
                # Just attach the file without specifying a type - Allure will detect it
                allure.attach.file(audio_path, "Generated Audio")
                assert audio_path is not None
                assert os.path.exists(audio_path)
            
            # Step 2: Generate image
            with allure.step("Generating test image"):
                baby_profile = {"tone": "warm, inviting", "voice_id": "test"}
                image_path = await image_service.generate_baby_image(
                    speaker=test_speaker,
                    baby_profile=baby_profile,
                    campaign_id=test_campaign_id
                )
                if image_path:
                    allure.attach.file(image_path, "Generated Image", allure.attachment_type.PNG)
                assert image_path is not None
                assert os.path.exists(image_path)
            
            # Step 3: Generate video (complete N8N workflow)
            with allure.step("Generating lip-sync video"):
                video_path = await video_service.create_lipsync_video(
                    audio_path=audio_path,
                    image_path=image_path,
                    scene_index=0,
                    speaker=test_speaker,
                    campaign_id=test_campaign_id
                )
                
                # Verify results
                assert video_path is not None
                assert os.path.exists(video_path)
                assert video_path.endswith(".mp4")
                
                # Check file size
                video_size = os.path.getsize(video_path)
                assert video_size > 1000  # At least 1KB
                
                # Attach video to report
                allure.attach.file(video_path, "Generated Video", allure.attachment_type.MP4)
                
        finally:
            # No cleanup - keep files for inspection
            pass 