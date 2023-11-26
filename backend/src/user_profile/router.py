import fastapi
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.database import get_async_session
from src.user_profile.models import User

# from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK


router = fastapi.APIRouter(prefix="/profile", tags=["user-profile"])

# Эндпоинт для получения основных данных пользователя
@router.get("/")
async def get_user_data(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return {
        "status": "success",
        "first_name": user.first_name,
        "registered_at": user.registered_at,
        "details": None,
    }
