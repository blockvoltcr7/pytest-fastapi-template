from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.content.content_schemas import (
    ContentCreationRequest,
    ContentCreationResponse,
    ContentIdea
)
from app.agents.content_crew.content_creation_crew import ContentCreationCrew
from app.tools.content_tools.trend_tools import ContentTrendTools
from typing import Dict, List
import time

router = APIRouter()

@router.post(
    "/content/create",
    summary="Create optimized content based on trends",
    description="Process content ideas through AI crew for trend analysis and optimization",
    response_model=ContentCreationResponse,
    response_description="Optimized content with trend insights",
)
async def create_content(request: ContentCreationRequest) -> ContentCreationResponse:
    """
    Process content ideas through the content creation crew

    This endpoint is designed for N8N integration to:
    1. Receive content ideas from Google Sheets
    2. Analyze trends and competitors
    3. Create optimized content

    Args:
        request: Content creation request with ideas and optional Google Sheet data

    Returns:
        ContentCreationResponse: Results of content processing with optimization insights
    """
    start_time = time.time()
    errors = []
    processed_ideas = []

    try:
        # Initialize the content crew
        crew = ContentCreationCrew()

        # Process each content idea
        for idea in request.content_ideas:
            try:
                # Convert Pydantic model to dict
                idea_dict = idea.model_dump()

                # Add Google Sheet context if available
                if request.google_sheet_row:
                    idea_dict['sheet_context'] = request.google_sheet_row

                # Process through crew
                result = crew.process_content_idea(idea_dict)
                processed_ideas.append(result)

            except Exception as e:
                error_msg = f"Error processing idea '{idea.topic}': {str(e)}"
                errors.append(error_msg)
                print(f"Error: {error_msg}")

        processing_time = time.time() - start_time

        return ContentCreationResponse(
            status="success" if not errors else "partial_success",
            processed_ideas=processed_ideas,
            processing_time=processing_time,
            errors=errors
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Content creation failed: {str(e)}"
        )



async def process_content_background(task_id: str, request: ContentCreationRequest):
    """
    Background task for content processing

    Args:
        task_id: Unique task identifier
        request: Content creation request
    """
    try:
        task_status[task_id]["status"] = "processing"

        # Initialize crew
        crew = ContentCreationCrew()
        processed_ideas = []
        errors = []

        total_ideas = len(request.content_ideas)

        for idx, idea in enumerate(request.content_ideas):
            try:
                # Update progress
                progress = int((idx / total_ideas) * 100)
                task_status[task_id]["progress"] = progress

                # Process idea
                idea_dict = idea.model_dump()
                if request.google_sheet_row:
                    idea_dict['sheet_context'] = request.google_sheet_row

                result = crew.process_content_idea(idea_dict)
                processed_ideas.append(result)

            except Exception as e:
                errors.append(f"Error processing '{idea.topic}': {str(e)}")

        # Update final status
        task_status[task_id].update({
            "status": "completed",
            "progress": 100,
            "result": {
                "processed_ideas": processed_ideas,
                "errors": errors
            }
        })

    except Exception as e:
        task_status[task_id].update({
            "status": "failed",
            "errors": [str(e)]
        })


@router.get(
    "/content/health",
    summary="Health check for content creation service",
    description="Check if the content creation service is running properly",
)
async def content_service_health() -> Dict:
    """
    Health check endpoint for the content creation service

    Returns:
        Dict: Service health status
    """
    try:
        # Test basic functionality
        tools = ContentTrendTools()
        crew = ContentCreationCrew()

        return {
            "status": "healthy",
            "service": "content_creation_crew",
            "tools_available": {
                "search_tool": tools.search_tool is not None,
                "website_search_tool": tools.website_search_tool is not None,
                "scrape_tool": tools.scrape_tool is not None
            },
            "agents_count": 4,
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }
