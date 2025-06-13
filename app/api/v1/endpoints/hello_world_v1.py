from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/hello",
    summary="Say hello to the world",
    description="A simple endpoint that returns a hello world message",
    response_description="The hello world message",
)
async def read_hello() -> dict[str, str]:
    """Return a hello world message

    Returns:
        dict[str, str]: A dictionary containing the message
    """
    return {"message": "Hello World"}
