import fastapi
from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.processing_appeals.models import Category
from src.user_profile.models import Role
from src.add_content.schemas import CategorySchema, RoleSchema

router = fastapi.APIRouter(prefix="/add", tags=["add-content"])


@router.post("/role")
async def add_role(
    role: RoleSchema,
    session: AsyncSession = Depends(get_async_session),
    #  user: User = Depends(current_user),
):
    stmt = insert(Role).values(**role.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/category")
async def add_category(
    category: CategorySchema,
    session: AsyncSession = Depends(get_async_session),
    #  user: User = Depends(current_user),
):
    stmt = insert(Category).values(**category.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
