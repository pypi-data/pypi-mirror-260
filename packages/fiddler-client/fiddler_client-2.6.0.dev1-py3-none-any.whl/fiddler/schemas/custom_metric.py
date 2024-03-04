from datetime import datetime
from typing import Optional
from uuid import UUID

from fiddler.schemas.base import BaseModel


class CustomExpressionResp(BaseModel):
    id: UUID
    name: str
    model_name: str
    project_name: str
    definition: str
    description: Optional[str]
    created_at: datetime


class CustomMetricResp(CustomExpressionResp):
    """Custom metric response object"""


class SegmentResp(CustomExpressionResp):
    """Segment response object"""
