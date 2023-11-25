import fastapi
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.database import get_async_session
from src.user_profile.models import User

# from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK


router = fastapi.APIRouter(prefix="/profile", tags=["user-profile"])


@router.get("/")
async def get_user_data(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    user_attrs = user.__dict__
    username = user_attrs.get("username")
    registered_at = user_attrs.get("registered_at")
    # img =
    return {
        "status": "success",
        "username": username,
        "registered_at": registered_at,
        "details": None,
    }
