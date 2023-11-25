import json

import fastapi
from fastapi import Depends, Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.database import get_async_session
from src.processing_credit.processing_model import use_model
from src.user_profile.models import User
from src.utils import get_data
from src.processing_credit.models import Request

router = fastapi.APIRouter(prefix="/credit", tags=["credit"])


@router.post("/processing_request")
async def appeal_neuro(
    data: dict,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    result_for_front = use_model(data)
    data = {key: value[0] for key, value in data.items()}
    data["user_id"] = user.id
    stmt = (
        insert(Request).values(**data)
    )
    await session.execute(stmt)
    await session.commit()

    return {"result": str(result_for_front[0][0])}
