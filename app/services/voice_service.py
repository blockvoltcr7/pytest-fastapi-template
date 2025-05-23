import os
from typing import Optional
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from app.core.config import settings


class VoiceService:
    def __init__(self):
        self.client = ElevenLabs(api_key=settings.elevenlabs_api_key)

    async def generate_speech(
        self,
        text: str,
        voice_id: str,
        output_filename: str,
        custom_voice_settings: Optional[dict] = None,
    ) -> Optional[str]:
        """
        Generate speech audio using ElevenLabs SDK

        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
            output_filename: Name for the output file (e.g., "audio_output.mp3")
            custom_voice_settings: Optional voice settings adjustments

        Returns:
            Path to the generated audio file, or None if failed
        """
        if not settings.elevenlabs_api_key:
            raise ValueError("ElevenLabs API key not configured")

        try:
            # Create voice settings
            voice_settings = self._create_generic_voice_settings(custom_voice_settings)

            # Generate audio using SDK
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
                voice_settings=voice_settings,
            )

            # Save audio file
            output_path = os.path.join(settings.audio_dir, output_filename)

            # Write audio bytes to file
            with open(output_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)

            return output_path

        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None

    def _create_generic_voice_settings(
        self, custom_settings: Optional[dict] = None
    ) -> VoiceSettings:
        """
        Create voice settings, applying custom adjustments if provided.
        """
        # Default settings
        default_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,  # Default style, can be overridden
            "use_speaker_boost": True,
        }

        # Apply custom adjustments
        if custom_settings:
            default_settings.update(custom_settings)  # More generic way to update

        return VoiceSettings(**default_settings)

    async def check_api_connection(self) -> bool:
        """Test if ElevenLabs API connection works"""
        if not settings.elevenlabs_api_key:
            return False

        try:
            # Try to get user info to test connection
            user = self.client.user.get()
            return user is not None
        except:
            return False

    def list_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            voices = self.client.voices.get_all()
            return [{"voice_id": v.voice_id, "name": v.name} for v in voices.voices]
        except Exception as e:
            print(f"Error fetching voices: {str(e)}")
            return []
