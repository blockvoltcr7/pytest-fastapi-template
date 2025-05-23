from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def read_hello():
    return {"message": "Hello World"}