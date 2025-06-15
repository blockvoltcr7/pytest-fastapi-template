"""Tests for Gemini TTS podcast generation."""

import os
import pytest
import allure
from tests.utils.gemini.gemini_tts_utils import (
    create_gemini_client,
    generate_podcast_audio,
    verify_audio_files_created,
    cleanup_test_files,
    attach_audio_info_to_allure
)


@pytest.fixture(scope="function")
def gemini_client():
    """Create a Gemini client for testing."""
    try:
        return create_gemini_client()
    except ValueError as e:
        pytest.skip(f"Skipping Gemini TTS test: {e}")


# @pytest.fixture(scope="function", autouse=True)
# def cleanup_files():
#     """Automatically clean up test files after each test."""
#     yield
#     cleanup_test_files("TEST_PODCAST_*")


@allure.feature("Gemini TTS")
@allure.story("Podcast Generation")
@allure.title("Generate Coffee Podcast Audio with Multi-Speaker TTS")
def test_gemini_podcast_generation(gemini_client):
    """
    Test that Gemini TTS can successfully generate multi-speaker podcast audio.

    This test verifies that:
    1. The TTS service can connect to Gemini API
    2. Audio files are generated from the coffee podcast content
    3. Generated files exist and are not empty
    """
    with allure.step("Generate podcast audio using Gemini TTS"):
        generated_files = generate_podcast_audio(gemini_client)

        # Attach file info to Allure report
        attach_audio_info_to_allure(generated_files)

    with allure.step("Verify audio files were created"):
        # Main assertion: verify that audio files were created
        assert verify_audio_files_created(generated_files), "No valid audio files were generated"

        # Additional verification that we have at least one file
        assert len(generated_files) > 0, "Expected at least one audio file to be generated"

        allure.attach(
            f"Successfully generated {len(generated_files)} audio file(s)",
            name="Test Result",
            attachment_type=allure.attachment_type.TEXT,
        )
