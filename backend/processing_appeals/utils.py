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
