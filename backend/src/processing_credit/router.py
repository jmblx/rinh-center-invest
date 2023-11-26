import fastapi
from fastapi import BackgroundTasks, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.database import get_async_session
from src.processing_credit.processing_model import use_model
from src.user_profile.models import User
from src.utils import get_data
from src.processing_credit.models import Request
from src.report.tasks import send_email_report_dashboard

router = fastapi.APIRouter(prefix="/credit", tags=["credit"])


# Эндпоинт выдачи вердикта моделью заявке на кредит
@router.post("/processing_request")
async def processing_request(
    data: dict,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    result = (use_model(data))[0][0]
    data = {key: value[0] for key, value in data.items()}
    data["user_id"] = user.id
    data["is_good_client"] = float(result)
    stmt = (
        insert(Request).values(**data)
    )
    await session.execute(stmt)
    await session.commit()
    background_tasks.add_task(
        send_email_report_dashboard,
        user.first_name,
        user.email,
        int(result)
    )
    return {"result": str(result)}


# Эндпоинт получения всех заявок пользователя
@router.get("/get_requests")
async def get_requests(
    user: User = Depends(current_user)
):
    requests = await get_data(
        class_=Request,
        filter=Request.user_id == user.id,
        is_scalar=False,
        order_by=Request.created_at
    )
    return requests
