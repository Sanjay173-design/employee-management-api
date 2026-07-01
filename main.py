import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.employee_routes import router as employee_router
from app.api.auth_routes import router as auth_router
from app.core.database import engine, Base

from app.core.exception_handlers import (
    employee_not_found_handler,
    generic_exception_handler
)

from app.utils.exceptions import (
    EmployeeNotFoundException
)

from app.middleware.rate_limiter import (
    RateLimiterMiddleware
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    testing = os.getenv(
        "TESTING",
        "False"
    ) == "True"

    if not testing:

        print(
            "Creating database tables..."
        )

        Base.metadata.create_all(
            bind=engine
        )

    yield

    print(
        "Application shutdown"
    )

app = FastAPI(
    title="Employee Management API",
    lifespan=lifespan
)

app.add_exception_handler(
    EmployeeNotFoundException,
    employee_not_found_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.add_middleware(
    RateLimiterMiddleware
)

app.include_router(
    employee_router
)

app.include_router(
    auth_router
)

@app.get("/")
async def home():

    return {
        "message": "API Running"
    }