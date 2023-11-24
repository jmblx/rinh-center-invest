from pydantic import BaseModel
from typing_extensions import Any, Dict


class CompetenceSchema(BaseModel):
    competencies: Dict[str, Any]
