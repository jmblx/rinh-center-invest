import random

import fastapi
from fastapi import Depends, Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.database import get_async_session
from src.processing_appeals.models import Message, Category
from src.processing_appeals.utils import task_assignment
from src.user_profile.models import User
from src.utils import get_data

router = fastapi.APIRouter(prefix="/chat", tags=["chat"])


# @router.post("/appeal/neuro")
# async def appeal_neuro(
#     message_text: str,
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(current_user),
# ):
#
#     category: Category = await get_data(
#         Category, Category.name == category_name, True
#     )
#     stmt = insert(Message).values(
#         {
#             "text": message_text,
#             "category_id": category.id,
#             "author_id": user.id,
#             #  "priority_exact": priority_exact,
#             #  "priority_conditional": priority_conditional,
#         }
#     )
#     result = await task_assignment(
#         category_name=category_name,
#         author_id=user.id,
#     )
#     await session.execute(stmt)
#     await session.commit()
#     return result


@router.post("/appeal/respondent")
async def appeal_respondent(
    message_text: str,
    category_name: str = None,
    user: User = Depends(current_user),
):
    result = await task_assignment(
        category_name=category_name, author_id=user.id
    )
