from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from .exceptions import CustomException, AccessDenied, NotFound


async def http_exception_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    response = JSONResponse(
        content={"successful": False, "detail": exc.detail},
        status_code=exc.status_code,
    )
    if exc.headers is not None:
        response.init_headers(exc.headers)

    return response


async def custom_exception_handler(
    _: Request,
    exc: CustomException,
) -> JSONResponse:
    status_code_map = {
        AccessDenied: status.HTTP_403_FORBIDDEN,
        NotFound: status.HTTP_404_NOT_FOUND,
    }

    response = JSONResponse(
        content={"successful": False, "code": exc.__class__.__name__, "detail": str(exc)},
        status_code=status_code_map.get(exc, status.HTTP_400_BAD_REQUEST),
    )

    return response
