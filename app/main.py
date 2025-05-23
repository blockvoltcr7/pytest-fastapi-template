from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(title="GenAI API", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "GenAI API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

# To run this application:
# Ensure you are in the root directory of the project
# Activate your virtual environment: source .venv/bin/activate
# Run: uvicorn app.main:app --reload