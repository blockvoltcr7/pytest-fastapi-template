from fastapi import APIRouter
from app.api.v1.endpoints.hello_world_v1 import router as hello_world_router
from app.api.v1.endpoints.crewai_v1 import router as crewai_router
from app.api.v1.endpoints.crewai_v1_content_crew import router as content_crew_router

api_router = APIRouter()
api_router.include_router(hello_world_router, tags=["hello world"])
api_router.include_router(crewai_router, tags=["crewai"])
api_router.include_router(content_crew_router, tags=["content crew"])
