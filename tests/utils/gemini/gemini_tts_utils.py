"""Gemini TTS test utilities and helper functions."""

import os
import glob
import allure
import logging
from pathlib import Path
from typing import List, Optional
from google import genai
from google.genai import types

# Configure logging
logger = logging.getLogger(__name__)


def create_gemini_client() -> genai.Client:
    """
    Create a Gemini client with API key from environment variables.

    DEPRECATED: Use create_gemini_client_with_key() instead for better security.

    Returns:
        genai.Client: A configured Gemini client instance

    Raises:
        ValueError: If API key is not found in environment
    """
    # Check for API key in multiple environment variable names
    google_api_key = os.getenv('GOOGLE_API_KEY')
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    logger.info(f"create_gemini_client: Checking environment variables")
    logger.info(f"create_gemini_client: GOOGLE_API_KEY present: {bool(google_api_key)}")
    logger.info(f"create_gemini_client: GEMINI_API_KEY present: {bool(gemini_api_key)}")

    api_key = google_api_key or gemini_api_key

    if not api_key:
        logger.error("create_gemini_client: No API key found in environment variables")
        raise ValueError("API key not found. Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")

    return create_gemini_client_with_key(api_key)


def create_gemini_client_with_key(api_key: str) -> genai.Client:
    """
    Create a Gemini client with the provided API key.

    Args:
        api_key: Google/Gemini API key

    Returns:
        genai.Client: A configured Gemini client instance

    Raises:
        ValueError: If API key is invalid or client creation fails
    """
    if not api_key or not api_key.strip():
        logger.error("create_gemini_client_with_key: No API key provided")
        raise ValueError("API key is required")

    api_key = api_key.strip()
    logger.info(f"create_gemini_client_with_key: Using API key with length {len(api_key)}")

    try:
        logger.info("create_gemini_client_with_key: About to create genai.Client...")
        client = genai.Client(api_key=api_key)
        logger.info("create_gemini_client_with_key: Gemini client created successfully")
        return client
    except Exception as e:
        logger.error(f"create_gemini_client_with_key: Failed to create client: {str(e)}")
        logger.error(f"create_gemini_client_with_key: Exception type: {type(e).__name__}")
        raise ValueError(f"Failed to create Gemini client: {str(e)}")


def get_coffee_podcast_content() -> str:
    """
    Return the coffee podcast dialogue content for TTS generation.

    Returns:
        str: The complete podcast dialogue content
    """
    return """System instructions: Read aloud in a warm, welcoming tone; vibe is optimistic and forward-looking as we discuss how AI and sustainability are reshaping the organic coffee experience. Keep the pacing conversational and engaging.
Speaker 1: Hey there, Veronica here—welcome to "Brewing Tomorrow," where we sip on stories of organic coffee, tech, and the planet.
Speaker 2: And I'm Kevin, delighted to join you. Let's dive into the conscious coffee revolution that's perking up cups worldwide.
Speaker 1: Today's consumers want more than caffeine; they want confidence their beans are grown with earth-friendly practices.
Speaker 2: Exactly—transparent sourcing, shade-grown farms, and sustainable roasting build trust and loyalty in every mug.
Speaker 1: Now add AI magic: personalized quizzes can match you with the perfect blend based on taste and health goals.
Speaker 2: Plus evolving subscription boxes that learn your preferences over time—goodbye guesswork, hello ritual.
Speaker 1: Speaking of health, organic coffee boasts antioxidants and lower acidity, making each sip a wellness win.
Speaker 2: And by sharing farmer stories and #CoffeeCommunity moments, brands foster deeper connections and real impact.
Speaker 1: Ready to brew better? Hit that newsletter signup for behind-the-scenes insights and exclusive sustainable tips.
Speaker 2: Then take our "Find Your Perfect Brew" quiz—together, we'll craft a cup that's good for you and the planet."""


def create_tts_config() -> types.GenerateContentConfig:
    """
    Create the TTS generation configuration with multi-speaker setup.

    Returns:
        types.GenerateContentConfig: Configuration for Gemini TTS generation
    """
    return types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 1",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Zephyr"
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Speaker 2",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Puck"
                            )
                        ),
                    ),
                ]
            ),
        ),
    )


def generate_podcast_audio(client: genai.Client, output_dir: str = "output") -> List[str]:
    """
    Generate podcast audio using Gemini TTS API.

    Args:
        client: Configured Gemini client
        output_dir: Directory to save audio files (defaults to 'output' in the project root)

    Returns:
        List[str]: List of generated audio file paths
    """
    import mimetypes
    import struct

    def save_binary_file(file_name, data):
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")

    # Ensure output directory exists, relative to project root
    os.makedirs(output_dir, exist_ok=True)

    def parse_audio_mime_type(mime_type: str) -> dict:
        bits_per_sample = 16
        rate = 24000

        parts = mime_type.split(";")
        for param in parts:
            param = param.strip()
            if param.lower().startswith("rate="):
                try:
                    rate_str = param.split("=", 1)[1]
                    rate = int(rate_str)
                except (ValueError, IndexError):
                    pass
            elif param.startswith("audio/L"):
                try:
                    bits_per_sample = int(param.split("L", 1)[1])
                except (ValueError, IndexError):
                    pass

        return {"bits_per_sample": bits_per_sample, "rate": rate}

    def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
        parameters = parse_audio_mime_type(mime_type)
        bits_per_sample = parameters["bits_per_sample"]
        sample_rate = parameters["rate"]
        num_channels = 1
        data_size = len(audio_data)
        bytes_per_sample = bits_per_sample // 8
        block_align = num_channels * bytes_per_sample
        byte_rate = sample_rate * block_align
        chunk_size = 36 + data_size

        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1,
            num_channels, sample_rate, byte_rate, block_align,
            bits_per_sample, b"data", data_size
        )
        return header + audio_data

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=get_coffee_podcast_content()),
            ],
        ),
    ]

    config = create_tts_config()
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []
    file_index = 0

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"TEST_PODCAST_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)

            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)

            file_path = os.path.join(output_dir, f"{file_name}{file_extension}")
            save_binary_file(file_path, data_buffer)
            generated_files.append(file_path)
        else:
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text)

    return generated_files


def verify_audio_files_created(file_paths: List[str]) -> bool:
    """
    Verify that audio files were created and are not empty.

    Args:
        file_paths: List of file paths to verify

    Returns:
        bool: True if all files exist and are not empty
    """
    if not file_paths:
        return False

    for file_path in file_paths:
        if not os.path.exists(file_path):
            return False
        if os.path.getsize(file_path) == 0:
            return False

    return True


def cleanup_test_files(pattern: str = "TEST_PODCAST_*") -> None:
    """
    Clean up generated test files.

    Args:
        pattern: Glob pattern for files to delete
    """
    files_to_delete = glob.glob(pattern)
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Cleaned up: {file_path}")
        except OSError as e:
            print(f"Error cleaning up {file_path}: {e}")


def generate_podcast_audio_binary(client: genai.Client, text_content: str) -> bytes:
    """
    Generate podcast audio and return as binary data instead of saving files.

    Args:
        client: Configured Gemini client
        text_content: The podcast dialogue text content

    Returns:
        bytes: Combined WAV audio data as binary

    Raises:
        ValueError: If no audio data is generated
    """
    logger.info(f"generate_podcast_audio_binary: Starting audio generation for text length: {len(text_content)}")
    import mimetypes
    import struct
    from io import BytesIO

    def parse_audio_mime_type(mime_type: str) -> dict:
        bits_per_sample = 16
        rate = 24000

        parts = mime_type.split(";")
        for param in parts:
            param = param.strip()
            if param.lower().startswith("rate="):
                try:
                    rate_str = param.split("=", 1)[1]
                    rate = int(rate_str)
                except (ValueError, IndexError):
                    pass
            elif param.startswith("audio/L"):
                try:
                    bits_per_sample = int(param.split("L", 1)[1])
                except (ValueError, IndexError):
                    pass

        return {"bits_per_sample": bits_per_sample, "rate": rate}

    def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
        parameters = parse_audio_mime_type(mime_type)
        bits_per_sample = parameters["bits_per_sample"]
        sample_rate = parameters["rate"]
        num_channels = 1
        data_size = len(audio_data)
        bytes_per_sample = bits_per_sample // 8
        block_align = num_channels * bytes_per_sample
        byte_rate = sample_rate * block_align
        chunk_size = 36 + data_size

        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1,
            num_channels, sample_rate, byte_rate, block_align,
            bits_per_sample, b"data", data_size
        )
        return header + audio_data

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text_content),
            ],
        ),
    ]

    config = create_tts_config()
    audio_chunks = []

    logger.info(f"generate_podcast_audio_binary: Starting streaming request to Gemini API with model: {model}")

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue

            if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                data_buffer = inline_data.data
                file_extension = mimetypes.guess_extension(inline_data.mime_type)

                if file_extension is None:
                    data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)

                audio_chunks.append(data_buffer)
                logger.info(f"generate_podcast_audio_binary: Received audio chunk {len(audio_chunks)}, size: {len(data_buffer)} bytes")

    except Exception as e:
        logger.error(f"generate_podcast_audio_binary: Error during streaming: {str(e)}")
        raise

    logger.info(f"generate_podcast_audio_binary: Completed streaming, received {len(audio_chunks)} audio chunks")

    if not audio_chunks:
        logger.error("generate_podcast_audio_binary: No audio data was generated from the provided text")
        raise ValueError("No audio data was generated from the provided text")

    # Combine all audio chunks into a single WAV file
    if len(audio_chunks) == 1:
        logger.info(f"generate_podcast_audio_binary: Returning single audio chunk of size: {len(audio_chunks[0])} bytes")
        return audio_chunks[0]
    else:
        # For multiple chunks, we need to combine them properly
        # This is a simplified approach - for production, you might want more sophisticated audio concatenation
        combined_audio = b"".join(audio_chunks)
        logger.info(f"generate_podcast_audio_binary: Combined {len(audio_chunks)} chunks into {len(combined_audio)} bytes")
        return combined_audio


def attach_audio_info_to_allure(file_paths: List[str]) -> None:
    """
    Attach audio file information to Allure report.

    Args:
        file_paths: List of generated audio file paths
    """
    if not file_paths:
        allure.attach(
            "No audio files were generated",
            name="Audio Generation Status",
            attachment_type=allure.attachment_type.TEXT,
        )
        return

    file_info = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            file_info.append(f"{os.path.basename(file_path)}: {size} bytes")
        else:
            file_info.append(f"{os.path.basename(file_path)}: NOT FOUND")

    allure.attach(
        "\n".join(file_info),
        name="Generated Audio Files",
        attachment_type=allure.attachment_type.TEXT,
    )
