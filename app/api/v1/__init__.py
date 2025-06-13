"""
Main entrypoint for the v1 API.

This module creates a FastAPI router that includes all v1 endpoints.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import hello_world_v1


# Create the main v1 router
api_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)


# Include routes from endpoints
api_router.include_router(hello_world_v1.router, tags=["hello"])
