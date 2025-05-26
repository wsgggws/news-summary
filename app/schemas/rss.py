from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field


class RSSSubscribeRequest(BaseModel):
    url: HttpUrl = Field(description="要订阅的RSS源的URL")
    title: Optional[str] = Field(None, description="RSS源的标题 (可选, 如果未提供将尝试自动获取)")
    notify_enabled: bool = Field(True, description="是否为此订阅开启通知 (默认为True)")


class RSSSubscribeResponse(BaseModel):
    id: UUID = Field(description="成功订阅后RSS源在数据库中的唯一标识符")
    url: HttpUrl = Field(description="已订阅的RSS源的URL")
    title: Optional[str] = Field(None, description="已订阅的RSS源的标题")
    message: str = Field("success", description="操作结果消息 (例如 'success')")

    class Config:
        from_attributes = True  # 允许 Pydantic 直接从 ORM 模型转换
