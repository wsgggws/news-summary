from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


# 用户注册请求模型
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    def validate_username(cls, value):
        if not (4 <= len(value) <= 20):
            raise ValueError("Password length must be between 4 to 20 characters long")
        return value

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
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
