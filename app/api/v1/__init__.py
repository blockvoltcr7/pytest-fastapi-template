# This file makes 'v1' a Python package 
from fastapi import APIRouter
from app.api.v1.endpoints import items, campaigns

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"]) 