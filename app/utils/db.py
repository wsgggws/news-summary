from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


def handle_integrity_error(e: IntegrityError):
    """统一处理数据库约束错误，隐藏数据库具体错误细节"""
    error_msg = str(e.orig).split("DETAIL: ")[-1]
    if "(username)" in str(e):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username already exists: {error_msg}",
        )
    if "(email)" in str(e):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email already exists: {error_msg}",
        )
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Database constraint violation.",
    )


# 统一处理数据库约束错误
async def commit_db(db: AsyncSession):
    """封装数据库提交逻辑，统一捕获异常"""
    try:
        await db.commit()
    except IntegrityError as e:
        raise handle_integrity_error(e)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
