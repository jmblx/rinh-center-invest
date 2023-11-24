from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
import sentry_sdk

from src.auth.base_config import (
    auth_backend,
    fastapi_users,
    google_oauth_client,
)
from src.add_content.router import router as add_content_router
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.config import SENTRY_URL, SECRET_AUTH
from src.homepage.router import router as homepage_router
from src.user_profile.router import router as user_router

# from src.tasks.router import router as router_tasks

sentry_sdk.init(
    dsn=SENTRY_URL,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


app = FastAPI(title="messages proceed API")

app.include_router(add_content_router)
app.include_router(homepage_router)
app.include_router(user_router)

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
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET_AUTH,
        # redirect_url="http://127.0.0.1:8000/",
        is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_oauth_associate_router(
        google_oauth_client, UserRead, "SECRET"
    ),
    prefix="/auth/associate/google",
    tags=["auth"],
)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


origins = [
    "http://localhost:3000",
]

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

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(
#     "redis://localhost",
#     encoding="utf8",
#     decode_responses=True
#   )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
