from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Fetch the current logged in user.
    """
    return current_user
