from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.auth import (
    Token,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from app.services.database import get_db
from app.utils.db import commit_db
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/v1/user")


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    用户注册接口
    - 验证用户名和邮箱的唯一性
    - 密码哈希后存储
    """
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(new_user)
    await commit_db(db)
    await db.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    用户登录接口
    - 验证用户名和密码
    - 生成并返回 JWT 令牌
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # 更新用户最后登录时间和激活状态
    user.last_login = datetime.now(tz=timezone.utc)
    db.add(user)
    await db.commit()

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def user_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    - 需要有效的 JWT 令牌
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def UserUpdateser_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新当前用户信息
    - 需要有效的 JWT 令牌
    - 可以更新用户名、邮箱和密码等
    """
    # 仅获取有值的字段
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))  # 处理密码加密
    # 动态更新字段
    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.add(current_user)
    await commit_db(db)
    await db.refresh(current_user)
    return current_user
