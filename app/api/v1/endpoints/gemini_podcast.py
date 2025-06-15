"""Gemini TTS Podcast API endpoint."""

import os
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
from tests.utils.gemini.gemini_tts_utils import create_gemini_client, generate_podcast_audio_binary

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
    description="Generate multi-speaker podcast audio using Google Gemini TTS API. Returns WAV audio data as binary response.",
    response_description="WAV audio file as binary data",
    responses={
        200: {
            "content": {"audio/wav": {}},
            "description": "Generated podcast audio as WAV file"
        },
        400: {"description": "Invalid input text format"},
        500: {"description": "Internal server error - check GEMINI_API_KEY configuration"},
        502: {"description": "Gemini API error"}
    }
)
async def generate_podcast(request: PodcastRequest):
    """
    Generate multi-speaker podcast audio from text dialogue.

    This endpoint accepts text containing dialogue in Speaker 1: / Speaker 2: format
    and returns a WAV audio file using Google's Gemini TTS API.

    Args:
        request: PodcastRequest containing the dialogue text

    Returns:
        Response: Binary WAV audio data with appropriate headers

    Raises:
        HTTPException: For various error conditions (400, 500, 502)
    """
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="API key not configured. Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable."
        )

    # Validate text contains speakers
    if "Speaker 1:" not in request.text or "Speaker 2:" not in request.text:
        raise HTTPException(
            status_code=400,
            detail="Text must contain 'Speaker 1:' and 'Speaker 2:' dialogue format"
        )

    try:
        # Create Gemini client
        client = create_gemini_client()

        # Generate audio as binary data
        audio_data = generate_podcast_audio_binary(client, request.text)

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
        if "API key not found" in str(e):
            raise HTTPException(status_code=500, detail=str(e))
        elif "No audio data was generated" in str(e):
            raise HTTPException(status_code=502, detail="Failed to generate audio from Gemini API")
        else:
            raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors from Gemini API or other issues
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API error: {str(e)}"
        )
