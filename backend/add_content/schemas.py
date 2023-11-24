from pydantic import BaseModel
from typing_extensions import Any, Dict


class RoleSchema(BaseModel):
    name: str
    permissions: Dict[str, Any]


class CategorySchema(BaseModel):
    name: str
