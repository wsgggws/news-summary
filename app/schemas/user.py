from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """用户基类模型，提供复用的字段校验"""

    username: Optional[str] = Field(
        None,
        min_length=4,
        max_length=20,
        description="用户名, 长度必须为4-20个字符 (Username must be 4-20 characters long)",
    )
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    password: Optional[str] = Field(None, description="用户密码 (注册和更新时使用)")
    bio: Optional[str] = Field(None, description="用户个人简介")
    avatar: Optional[str] = Field(None, description="用户头像链接")
    favorite_sites: Optional[dict] = Field(None, description="用户收藏的站点列表")


# 用户注册请求模型
class UserCreate(UserBase):
    @field_validator("password")
    def validate_password(cls, value):
        """
        密码验证器：检查密码长度和复杂性
        - 长度必须在 8 到 20 个字符之间
        - 必须包含至少一个大写字母、一个小写字母、一个数字和一个特殊字符
        """
        if not (8 <= len(value) <= 20):
            raise ValueError("Password length must be between 8 to 20 characters long")
        # 检查密码复杂性
        upper = lower = digit = special = False
        special_chars = '!@#$%^&*(),.?":;{}|<>'
        for char in value:
            if upper or char.isupper():
                upper = True
            # 上面 upper or 的这种写法，下面就不能用 elif 了!
            if lower or char.islower():
                lower = True
            if digit or char.isdigit():
                digit = True
            if special or (char in special_chars):
                special = True
        # 如果缺少任何一种字符类型，抛出错误
        if not all([upper, lower, digit, special]):
            raise ValueError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character"
            )
        return value


# 用户更新请求模型
class UserUpdate(UserBase):
    pass


class UserResponse(BaseModel):
    id: UUID = Field(description="用户唯一标识符")
    username: str = Field(description="用户名")
    email: str = Field(description="用户邮箱")
    last_login: Optional[datetime] = Field(None, description="上次登录时间")
    avatar: Optional[str] = Field(None, description="用户头像链接")
    bio: Optional[str] = Field(None, description="用户个人简介")
    favorite_sites: Optional[dict] = Field(None, description="用户收藏的站点列表")
    created_at: datetime = Field(description="用户创建时间")
    updated_at: datetime = Field(description="用户更新时间")

    class Config:
        from_attributes = True  # 允许 Pydantic 直接从 ORM 模型转换
