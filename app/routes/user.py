from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import (
    Token,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from app.services.database import get_db
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/v1/user")


@router.post("/register")
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
    try:
        db.add(new_user)
        await db.commit()
    except IntegrityError as e:
        # 捕获唯一性约束错误
        if "(username)" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{str(e.orig).split('DETAIL: ')[-1]}",
            )
        if "(email)" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{str(e.orig).split('DETAIL: ')[-1]}",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
    await db.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    用户登录接口
    - 验证用户名和密码
    - 生成并返回 JWT 令牌
    """
    if not (form_data.username and form_data.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and password is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
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


@router.get("/me")
async def user_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    - 需要有效的 JWT 令牌
    """
    return current_user


@router.put("/me")
async def update_user_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新当前用户信息
    - 需要有效的 JWT 令牌
    - 可以更新用户名、邮箱和密码
    """
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    if user_update.password:
        current_user.password_hash = get_password_hash(user_update.password)

    try:
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
    except IntegrityError as e:
        # 捕获唯一性约束错误
        if "(username)" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{str(e.orig).split('DETAIL: ')[-1]}",
            )
        if "(email)" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{str(e.orig).split('DETAIL: ')[-1]}",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
    return current_user
