from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class ContentIdea(BaseModel):
    topic: str = Field(..., description="Main topic or title of the content")
    content_type: str = Field(default="blog post", description="Type of content (blog post, social media, video script, etc.)")
    industry: Optional[str] = Field(None, description="Industry or niche")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    competitors: Optional[List[str]] = Field(default=[], description="List of competitor URLs or names")
    publish_date: Optional[str] = Field(None, description="Scheduled publish date")
    campaign_duration: Optional[str] = Field(default="1 week", description="Campaign duration")
    word_count: Optional[str] = Field(default="800-1000", description="Target word count")
    keywords: Optional[List[str]] = Field(default=[], description="Seed keywords to focus on")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "AI Tools for Content Marketing",
                "content_type": "blog post",
                "industry": "marketing",
                "target_audience": "marketing professionals",
                "competitors": ["contentmarketinginstitute.com", "hubspot.com"],
                "publish_date": "2024-03-15",
                "campaign_duration": "2 weeks",
                "word_count": "1200-1500",
                "keywords": ["AI content", "marketing automation", "content strategy"]
            }
        }

class ContentCreationRequest(BaseModel):
    content_ideas: List[ContentIdea] = Field(..., description="List of content ideas to process")
    google_sheet_row: Optional[Dict] = Field(None, description="Original Google Sheet row data")

    class Config:
        json_schema_extra = {
            "example": {
                "content_ideas": [
                    {
                        "topic": "AI Tools for Content Marketing",
                        "content_type": "blog post",
                        "industry": "marketing",
                        "target_audience": "marketing professionals",
                        "competitors": ["contentmarketinginstitute.com"],
                        "keywords": ["AI content", "marketing automation"]
                    }
                ],
                "google_sheet_row": {
                    "row_id": 1,
                    "source": "google_sheets"
                }
            }
        }

class ContentCreationResponse(BaseModel):
    status: str = Field(..., description="Status of the content creation process")
    processed_ideas: List[Dict] = Field(..., description="List of processed content ideas with results")
    processing_time: float = Field(..., description="Time taken to process all ideas in seconds")
    errors: List[str] = Field(default=[], description="List of errors encountered during processing")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "processed_ideas": [
                    {
                        "original_idea": {
                            "topic": "AI Tools for Content Marketing",
                            "content_type": "blog post"
                        },
                        "optimized_content": "Complete optimized content with trend insights...",
                        "timestamp": "2024-03-15T10:30:00",
                        "status": "success"
                    }
                ],
                "processing_time": 45.67,
                "errors": []
            }
        }

class QuickTrendRequest(BaseModel):
    topic: str = Field(..., description="Topic to analyze trends for")
    industry: str = Field(default="general", description="Industry context")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "sustainable fashion",
                "industry": "fashion"
            }
        }

class QuickTrendResponse(BaseModel):
    topic: str = Field(..., description="The analyzed topic")
    industry: str = Field(..., description="Industry context")
    general_trends: str = Field(..., description="General trend insights")
    social_trends: str = Field(..., description="Social media trend insights")
    status: str = Field(..., description="Status of the trend analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "sustainable fashion",
                "industry": "fashion",
                "general_trends": "Sustainable fashion is trending with focus on eco-friendly materials...",
                "social_trends": "High engagement on sustainable fashion content, trending hashtags...",
                "status": "success"
            }
        }

class AsyncTaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique identifier for the async task")
    status: str = Field(..., description="Current status of the task")
    check_status_url: str = Field(..., description="URL to check task status")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "12345-abcde-67890",
                "status": "task_started",
                "check_status_url": "/api/v1/content/status/12345-abcde-67890"
            }
        }

class TaskStatusResponse(BaseModel):
    status: str = Field(..., description="Current status of the task")
    progress: int = Field(..., description="Progress percentage (0-100)")
    result: Optional[Dict] = Field(None, description="Task result when completed")
    errors: List[str] = Field(default=[], description="List of errors encountered")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "progress": 100,
                "result": {
                    "processed_ideas": [],
                    "errors": []
                },
                "errors": []
            }
        }
