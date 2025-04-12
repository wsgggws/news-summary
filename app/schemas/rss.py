from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class RSSSubscribeRequest(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    notify_enabled: bool = True


class RSSSubscribeResponse(BaseModel):
    id: UUID
    url: HttpUrl
    title: Optional[str]
    message: str = "success"

    class Config:
        from_attributes = True  # 允许 Pydantic 直接从 ORM 模型转换
