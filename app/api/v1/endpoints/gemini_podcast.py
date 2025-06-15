"""Gemini TTS Podcast API endpoint."""

import logging
from fastapi import APIRouter, HTTPException, Response, Header
from pydantic import BaseModel, Field
from typing import Annotated
from tests.utils.gemini.gemini_tts_utils import create_gemini_client_with_key, generate_podcast_audio_binary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class PodcastRequest(BaseModel):
    """Request model for podcast generation."""
    text: str = Field(
        ...,
        description="The podcast dialogue text content with Speaker 1: and Speaker 2: format",
        min_length=10,
        max_length=50000,
        example="""System instructions: Read aloud in a warm, welcoming tone; vibe is optimistic and forward-looking as we discuss how AI and sustainability are reshaping the organic coffee experience. Keep the pacing conversational and engaging.
Speaker 1: Hey there, Veronica here—welcome to "Brewing Tomorrow," where we sip on stories of organic coffee, tech, and the planet.
Speaker 2: And I'm Kevin, delighted to join you. Let's dive into the conscious coffee revolution that's perking up cups worldwide."""
    )


@router.post(
    "/podcast",
    summary="Generate TTS Podcast Audio",
    description="Generate multi-speaker podcast audio using Google Gemini TTS API. Returns WAV audio data as binary response. Requires a valid Google/Gemini API key in the X-API-Key header.",
    response_description="WAV audio file as binary data",
    responses={
        200: {
            "content": {"audio/wav": {}},
            "description": "Generated podcast audio as WAV file"
        },
        400: {"description": "Invalid input text format"},
        401: {"description": "Missing or invalid API key in X-API-Key header"},
        500: {"description": "Internal server error"},
        502: {"description": "Gemini API error"}
    }
)
async def generate_podcast(
    request: PodcastRequest,
    x_api_key: Annotated[str, Header(alias="X-API-Key", description="Your Google/Gemini API key")]
):
    """
    Generate multi-speaker podcast audio from text dialogue.

    This endpoint accepts text containing dialogue in Speaker 1: / Speaker 2: format
    and returns a WAV audio file using Google's Gemini TTS API.

    Args:
        request: PodcastRequest containing the dialogue text
        x_api_key: Google/Gemini API key provided in X-API-Key header

    Returns:
        Response: Binary WAV audio data with appropriate headers

    Raises:
        HTTPException: For various error conditions (400, 401, 500, 502)
    """
    # Validate API key
    if not x_api_key or not x_api_key.strip():
        logger.error("No API key provided in X-API-Key header")
        raise HTTPException(
            status_code=401,
            detail="API key required. Please provide your Google/Gemini API key in the X-API-Key header."
        )

    api_key = x_api_key.strip()
    logger.info(f"API key provided via header (length: {len(api_key)})")

    # Validate text contains speakers
    if "Speaker 1:" not in request.text or "Speaker 2:" not in request.text:
        raise HTTPException(
            status_code=400,
            detail="Text must contain 'Speaker 1:' and 'Speaker 2:' dialogue format"
        )

    try:
        # Create Gemini client with user's API key
        logger.info("Creating Gemini client with user-provided API key...")
        client = create_gemini_client_with_key(api_key)
        logger.info("Gemini client created successfully")

        # Generate audio as binary data
        logger.info(f"Generating audio for text of length: {len(request.text)}")
        audio_data = generate_podcast_audio_binary(client, request.text)
        logger.info(f"Audio generation successful, size: {len(audio_data)} bytes")

        # Return binary response with appropriate headers
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=podcast.wav",
                "Content-Length": str(len(audio_data))
            }
        )

    except ValueError as e:
        # Handle specific ValueError from our utility function
        logger.error(f"ValueError occurred: {str(e)}")
        if "API key not valid" in str(e) or "INVALID_ARGUMENT" in str(e):
            raise HTTPException(status_code=401, detail="Invalid API key. Please check your Google/Gemini API key.")
        elif "No audio data was generated" in str(e):
            raise HTTPException(status_code=502, detail="Failed to generate audio from Gemini API")
        else:
            raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors from Gemini API or other issues
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")

        # Check if it's an API key related error
        error_str = str(e).lower()
        if "api key" in error_str or "invalid_argument" in error_str or "authentication" in error_str:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key. Please check your Google/Gemini API key."
            )
        else:
            raise HTTPException(
                status_code=502,
                detail=f"Gemini API error: {str(e)}"
            )
