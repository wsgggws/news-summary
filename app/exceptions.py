from fastapi import HTTPException, status


class UserBannedException(HTTPException):
    """用户被禁用异常"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This user has been banned.",
        )


class RateLimitExceededException(HTTPException):
    """超出限流异常"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )


class RSSSubscribeRepeatException(HTTPException):
    """重复订阅"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL has been subscribed for you.",
        )


class RSSInvalidException(HTTPException):
    """订阅链接无效"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RSS is invalid.",
        )


class RSSNotFoundException(HTTPException):
    """订阅不存在"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RSS id does not found.",
        )
