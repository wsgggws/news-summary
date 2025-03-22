from fastapi import HTTPException, status


class UserBannedException(HTTPException):
    """用户被禁用异常"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user has been banned",
        )


class InsufficientBalanceException(HTTPException):
    """余额不足异常"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient balance",
        )


class RateLimitExceededException(HTTPException):
    """超出限流异常"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
