import pytest
import os
import allure
from app.services.voice_service import VoiceService
from app.core.config import settings, create_output_directories

@allure.epic("Voice Generation")
@allure.feature("ElevenLabs SDK")
class TestVoiceServiceSDK:
    
    @pytest.fixture(autouse=True)
    def setup_dirs(self):
        """Ensure output directories exist"""
        create_output_directories()
    
    @pytest.fixture
    def voice_service(self):
        return VoiceService()
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.elevenlabs_api_key,
        reason="ElevenLabs API key not configured"
    )
    @allure.story("Speech Generation")
    @allure.severity(allure.severity_level.CRITICAL)
    async def test_speech_generation_with_sdk(self, voice_service):
        """Test speech generation using ElevenLabs SDK"""
        with allure.step("Generate speech for a test phrase"):
            test_text = "Yo, I just stumbled upon this artist, Mon Rovîa."
            voice_id = "pNInz6obpgDQGcFmaJgB"  # Free voice
            output_filename = "test_monrovia_scene.mp3"
            
            audio_path = await voice_service.generate_speech(
                text=test_text,
                voice_id=voice_id,
                output_filename=output_filename,
                tone_adjustments={"tone": "warm, inviting"}
            )
        
        with allure.step("Verify audio file was created"):
            assert audio_path is not None
            assert os.path.exists(audio_path)
            
            # Check file size
            file_size = os.path.getsize(audio_path)
            assert file_size > 0
            
            # Just note the path since allure doesn't have MP3 type
            allure.attach(
                f"Audio file created at: {audio_path} ({file_size} bytes)",
                name="Generated Audio",
                attachment_type=allure.attachment_type.MP4
            )
            
            print(f"✅ Generated Mon Rovîa scene audio: {audio_path} ({file_size} bytes)")
        
        # Cleanup
        with allure.step("Clean up test files"):
            os.remove(audio_path)
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.elevenlabs_api_key,
        reason="ElevenLabs API key not configured"
    )
    @allure.story("API Connection")
    @allure.severity(allure.severity_level.BLOCKER)
    async def test_api_connection_sdk(self, voice_service):
        """Test API connection using SDK"""
        with allure.step("Test connection to ElevenLabs API"):
            result = await voice_service.test_connection()
            assert result is True
            print("✅ ElevenLabs SDK connection successful!")
    
    @pytest.mark.skipif(
        not settings.elevenlabs_api_key,
        reason="ElevenLabs API key not configured"
    )
    @allure.story("Voice Listing")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_voices(self, voice_service):
        """Test getting available voices"""
        with allure.step("List all available voices"):
            voices = voice_service.get_available_voices()
            assert isinstance(voices, list)
            
            if voices:  # If voices are returned
                assert "voice_id" in voices[0]
                assert "name" in voices[0]
                
                # Attach voice list as JSON
                allure.attach(
                    str(voices),
                    name="Available Voices",
                    attachment_type=allure.attachment_type.JSON
                )
                
                print(f"✅ Found {len(voices)} available voices") 