import random

from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST

from src.database import get_async_session
from src.processing_appeals.models import Category, Task
from src.user_profile.models import User
from src.utils import get_data


async def task_assignment(
    category_name: str,
    author_id,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    competent_workers = await get_data(
        class_=User,
        filter=User.competencies.get(category_name) == 1,
        is_scalar=False,
    )

    if len(competent_workers) > 1:
        min_tasks = min(worker.tasks_count for worker in competent_workers)
        best_workers = [
            worker
            for worker in competent_workers
            if worker.tasks_count == min_tasks
        ]

        if len(best_workers) > 1:
            min_competencies = min(
                worker.competencies_count for worker in best_workers
            )
            final_worker = min(
                best_workers, key=lambda worker: worker.competencies_count
            )
        else:
            final_worker = best_workers[0]

    else:
        final_worker = competent_workers[0]

    if final_worker.role_id == 1:
        worker = final_worker
    else:
        response.status_code = HTTP_400_BAD_REQUEST
        return {"details": "error"}
    chat_id = random.randint(1, 99999999)
    stmt = insert(Task).values(
        {
            "author_id": author_id,
            "responding_id": worker.id,
            "chat_id": chat_id,
        }
    )
    await session.execute(stmt)
    worker.tasks_count += 1
    await session.commit()
    return {"status": "success", "chat_id": chat_id}
