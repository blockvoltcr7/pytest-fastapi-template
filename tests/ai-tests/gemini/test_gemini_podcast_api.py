"""Integration tests for Gemini TTS Podcast API."""

import os
import pytest
import allure
from fastapi.testclient import TestClient
from app.main import app
from tests.utils.gemini.gemini_tts_utils import get_coffee_podcast_content

client = TestClient(app)


@pytest.fixture(scope="function")
def skip_if_no_api_key():
    """Skip test if GEMINI_API_KEY is not available."""
    if not os.getenv('GEMINI_API_KEY'):
        pytest.skip("GEMINI_API_KEY not found in environment variables")


@allure.feature("Gemini TTS API")
@allure.story("Podcast Generation API")
@allure.title("Test Podcast Generation API Endpoint")
def test_gemini_podcast_api_success(skip_if_no_api_key):
    """
    Test successful podcast generation via API endpoint.

    This test verifies that:
    1. The API accepts valid podcast text input
    2. Returns binary WAV audio data
    3. Sets appropriate response headers
    """
    # Use the existing coffee podcast content
    test_text = get_coffee_podcast_content()

    with allure.step("Send POST request to podcast generation API"):
        response = client.post(
            "/api/v1/gemini/podcast",
            json={"text": test_text}
        )

    with allure.step("Verify successful response"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

        # Verify content type
        assert response.headers["content-type"] == "audio/wav"

        # Verify content disposition header
        assert "attachment" in response.headers.get("content-disposition", "")

        # Verify we got binary audio data
        audio_data = response.content
        assert len(audio_data) > 0, "No audio data received"

        # Basic WAV file header validation
        assert audio_data.startswith(b"RIFF"), "Response does not appear to be a valid WAV file"
        assert b"WAVE" in audio_data[:12], "Response does not contain WAVE header"

        allure.attach(
            f"Generated audio file size: {len(audio_data)} bytes",
            name="Audio Generation Result",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Gemini TTS API")
@allure.story("Podcast Generation API")
@allure.title("Test API with Invalid Text Format")
def test_gemini_podcast_api_invalid_text():
    """Test API with invalid text format (missing speakers)."""

    invalid_text = "This is just plain text without any speaker format."

    with allure.step("Send POST request with invalid text"):
        response = client.post(
            "/api/v1/gemini/podcast",
            json={"text": invalid_text}
        )

    with allure.step("Verify error response"):
        assert response.status_code == 400
        assert "Speaker 1:" in response.json()["detail"]
        assert "Speaker 2:" in response.json()["detail"]


@allure.feature("Gemini TTS API")
@allure.story("Podcast Generation API")
@allure.title("Test API with Empty Text")
def test_gemini_podcast_api_empty_text():
    """Test API with empty or too short text."""

    with allure.step("Send POST request with empty text"):
        response = client.post(
            "/api/v1/gemini/podcast",
            json={"text": ""}
        )

    with allure.step("Verify validation error"):
        assert response.status_code == 422  # Pydantic validation error
        assert "at least 10 characters" in str(response.json()) or "ensure this value has at least 10 characters" in str(response.json())


@allure.feature("Gemini TTS API")
@allure.story("Podcast Generation API")
@allure.title("Test API with Missing Text Field")
def test_gemini_podcast_api_missing_text():
    """Test API with missing text field."""

    with allure.step("Send POST request without text field"):
        response = client.post(
            "/api/v1/gemini/podcast",
            json={}
        )

    with allure.step("Verify validation error"):
        assert response.status_code == 422  # Pydantic validation error
        assert "field required" in str(response.json()) or "Field required" in str(response.json())


@allure.feature("Gemini TTS API")
@allure.story("Podcast Generation API")
@allure.title("Test API with Custom Podcast Content")
def test_gemini_podcast_api_custom_content(skip_if_no_api_key):
    """Test API with custom podcast content."""

    custom_text = """System instructions: Read in a friendly tone.
Speaker 1: Welcome to our test podcast about technology.
Speaker 2: Thanks for having me. Let's discuss the latest in AI development.
Speaker 1: Artificial Intelligence is transforming many industries today.
Speaker 2: Absolutely, and the pace of innovation is accelerating rapidly."""

    with allure.step("Send POST request with custom content"):
        response = client.post(
            "/api/v1/gemini/podcast",
            json={"text": custom_text}
        )

    with allure.step("Verify successful response with custom content"):
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/wav"

        audio_data = response.content
        assert len(audio_data) > 0, "No audio data received"
        assert audio_data.startswith(b"RIFF"), "Response does not appear to be a valid WAV file"

        allure.attach(
            f"Custom content audio size: {len(audio_data)} bytes",
            name="Custom Content Result",
            attachment_type=allure.attachment_type.TEXT,
        )
