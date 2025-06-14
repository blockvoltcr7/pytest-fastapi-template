from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.v1.schemas.content.content_schemas import (
    ContentCreationRequest,
    ContentCreationResponse,
    ContentIdea,
    QuickTrendRequest,
    QuickTrendResponse,
    AsyncTaskResponse,
    TaskStatusResponse
)
from app.agents.content_crew.content_creation_crew import ContentCreationCrew
from app.tools.content_tools.trend_tools import ContentTrendTools
from typing import Dict, List
import time
import asyncio
import uuid

router = APIRouter()

# In-memory task storage (in production, use a proper database)
task_status = {}

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

@router.post(
    "/content/create-async",
    summary="Create content asynchronously",
    description="Start async content creation task (for long-running processes)",
    response_model=AsyncTaskResponse,
)
async def create_content_async(
    request: ContentCreationRequest,
    background_tasks: BackgroundTasks
) -> AsyncTaskResponse:
    """
    Start asynchronous content creation for N8N webhook integration

    Args:
        request: Content creation request
        background_tasks: FastAPI background tasks

    Returns:
        AsyncTaskResponse: Task ID and status check URL
    """
    task_id = str(uuid.uuid4())
    task_status[task_id] = {
        "status": "pending",
        "progress": 0,
        "result": None,
        "errors": []
    }

    # Add background task
    background_tasks.add_task(
        process_content_background,
        task_id,
        request
    )

    return AsyncTaskResponse(
        task_id=task_id,
        status="task_started",
        check_status_url=f"/api/v1/content/status/{task_id}"
    )

@router.get(
    "/content/status/{task_id}",
    summary="Check content creation status",
    description="Check the status of an async content creation task",
    response_model=TaskStatusResponse,
)
async def check_content_status(task_id: str) -> TaskStatusResponse:
    """
    Check status of async content creation task

    Args:
        task_id: Unique task identifier

    Returns:
        TaskStatusResponse: Current task status and progress
    """
    if task_id not in task_status:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_data = task_status[task_id]
    return TaskStatusResponse(
        status=task_data["status"],
        progress=task_data["progress"],
        result=task_data.get("result"),
        errors=task_data.get("errors", [])
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

@router.post(
    "/content/quick-trends",
    summary="Get quick trend analysis",
    description="Get quick trend insights without full content creation",
    response_model=QuickTrendResponse,
)
async def get_quick_trends(request: QuickTrendRequest) -> QuickTrendResponse:
    """
    Quick endpoint for trend analysis only

    Args:
        request: Quick trend analysis request

    Returns:
        QuickTrendResponse: Trend insights for the topic
    """
    try:
        tools = ContentTrendTools()

        # Get trends
        trends = tools.search_trending_topics(request.industry, [request.topic])
        social_trends = tools.search_social_trends(request.topic)

        return QuickTrendResponse(
            topic=request.topic,
            industry=request.industry,
            general_trends=trends[:500] if len(trends) > 500 else trends,  # First 500 chars
            social_trends=social_trends[:500] if len(social_trends) > 500 else social_trends,
            status="success"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Trend analysis failed: {str(e)}"
        )

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

@router.delete(
    "/content/tasks/{task_id}",
    summary="Clean up completed task",
    description="Remove a completed task from memory",
)
async def cleanup_task(task_id: str) -> Dict:
    """
    Clean up a completed task from memory

    Args:
        task_id: Task identifier to clean up

    Returns:
        Dict: Cleanup status
    """
    if task_id in task_status:
        del task_status[task_id]
        return {"status": "cleaned", "task_id": task_id}
    else:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
