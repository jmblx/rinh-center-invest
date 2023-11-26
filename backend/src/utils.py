from sqlalchemy import select

from src.database import async_session_maker


# Базовая функция для сбора данных с БД
async def get_data(
    class_,
    filter,
    is_scalar: bool = False,
    order_by=None
):
    async with async_session_maker() as session:
        stmt = select(class_).where(filter)
        if is_scalar:
            res_query = await session.execute(stmt)
            res = res_query.scalar()
        else:
            if order_by:
                stmt = select(class_).where(filter).order_by(order_by)
            res_query = await session.execute(stmt)
            res = res_query.fetchall()
            res = [result[0] for result in res]
    return res


# Рендер шаблона. Мы в курсе про Jinja2, но с ней были проблемы :(
def render_email(
    user_first_name,
    encoded_image,
    verdict
):
    if verdict == "Одобрено":
        verbose_verdict = f"Здравствуйте, {user_first_name}," \
                          f" мы поздравляем вас! Вам одобрили вашу заявку на получение кредита."
    else:
        verbose_verdict = f"Здравствуйте, {user_first_name}," \
                          f" мы сожалеем! Вам не одобрили вашу заявку на получение кредита."
    return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Вердикт по заявке</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                }}

                .card {{
                    background-color: #f8f8f8;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    margin: 20px auto;
                    max-width: 600px;
                    padding: 20px;
                    text-align: center;
                }}

                .decline-header {{
                    color: #ff0000;
                    font-size: 50px
                }}

                .status-image {{
                    max-width: 100%;
                    height: auto;
                    margin: 20px 0;
                }}

                .user-message {{
                    color: #333333;
                    font-size: 16px;
                    line-height: 1.5;
                }}

                .visit-less {{
                    color: #666666;
                    font-size: 14px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1 class="decline-header">{verdict}</h1>
                <img src="data:image/png;base64,{encoded_image}" alt={verdict} class="status-image">
                <p class="user-message">
                    {verbose_verdict}
                </p>
                <div class="visit-less">Заходите к нам меньше!!!</div>
            </div>
        </body>
        </html>
        """
