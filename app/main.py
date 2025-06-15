"""
GenAI API

FastAPI application providing a simple API for GenAI.

The API is available under `/api/v1` and provides endpoints for:

* `/health`: A health check endpoint that returns a success message if the API is running.
* `/hello`: An example endpoint that returns a greeting message.

This application now includes OAuth2 security with JWT.

To run this application:

1. Ensure you are in the root directory of the project.
2. Activate your virtual environment: `source .venv/bin/activate`.
3. Run: `uvicorn app.main:app --reload`.

"""
from fastapi import FastAPI
from app.api.v1.api import api_router
import uvicorn

app = FastAPI(
    title="GenAI API",
    version="1.0.0",
    description="A simple API for GenAI with OAuth2 Bearer Token security",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint that returns a message.

    Returns:
        dict: A dictionary containing a message.
    """
    return {"message": "GenAI API"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint that returns a success message if the API is running.

    Returns:
        dict: A dictionary containing a status and a message.
    """
    return {"status": "healthy", "message": "API is running successfully"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
