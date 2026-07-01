from fastapi import Request
from fastapi.responses import JSONResponse

from app.utils.exceptions import (
    EmployeeNotFoundException
)

from app.core.logger import logger


async def employee_not_found_handler(
    request: Request,
    exc: EmployeeNotFoundException
):

    logger.warning(
        str(exc)
    )

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": str(exc)
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.error(
        str(exc)
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )