from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

import sentry_sdk

from src.auth.base_config import (
    auth_backend,
    fastapi_users,
)
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.config import SENTRY_URL, SECRET_AUTH
from src.user_profile.router import router as user_router
from src.processing_credit.router import router as processing_credit_router

sentry_sdk.init(
    dsn=SENTRY_URL,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app = FastAPI(title="requests proceed API")

# Подключение роутеров для обработки отчётов
app.include_router(user_router)
app.include_router(processing_credit_router)

# Подключение роутеров для авторизации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Регулировка обращений к API с других адресов
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
