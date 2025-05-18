from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(title="Baby Podcast GenAI", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Baby Podcast GenAI API"}

# To run this application:
# Ensure you are in the root directory of the project (baby-podcast-genai)
# Activate your virtual environment: source .venv/bin/activate
# Run: uvicorn app.main:app --reload 