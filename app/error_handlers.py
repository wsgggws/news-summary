from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse


def setup_exception_handlers(app: FastAPI):
    """统一异常处理"""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )

    # @app.exception_handler(RequestValidationError)
    # async def validation_exception_handler(request, exc):
    #     return JSONResponse(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         content={"detail": exc.errors},
    #     )
