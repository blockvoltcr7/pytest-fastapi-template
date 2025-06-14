from fastapi import APIRouter
from app.api.v1.endpoints.hello_world_v1 import router as hello_world_router
from app.api.v1.endpoints.crewai_v1 import router as crewai_router

api_router = APIRouter()
api_router.include_router(hello_world_router, tags=["hello world"])
api_router.include_router(crewai_router, tags=["crewai"])
