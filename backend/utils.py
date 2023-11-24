from sqlalchemy import insert, select

from src.database import async_session_maker


async def get_data(
    class_,
    filter,
    is_scalar: bool = False,
):
    async with async_session_maker() as session:
        stmt = select(class_).where(filter)
        if is_scalar:
            res_query = await session.execute(stmt)
            res = res_query.scalar()
        else:
            res_query = await session.execute(stmt)
            res = res_query.fetchall()
            res = [result[0] for result in res]
    return res
