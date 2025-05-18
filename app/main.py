from fastapi import FastAPI
from app.api.v1.endpoints import items as items_router

app = FastAPI(title="Baby Podcast GenAI")

app.include_router(items_router.router, prefix="/api/v1/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to Baby Podcast GenAI API"}

# To run this application:
# Ensure you are in the root directory of the project (baby-podcast-genai)
# Activate your virtual environment: source .venv/bin/activate
# Run: uvicorn app.main:app --reload 