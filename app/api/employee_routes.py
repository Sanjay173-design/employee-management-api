from typing import List

from fastapi import (
    APIRouter,
    status,
    Depends,
    BackgroundTasks,
)

from sqlalchemy.orm import Session

from fastapi import Query

from app.core.dependencies import get_db
from app.core.redis_client import redis_client

from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)

from app.services.employee_service import EmployeeService

from app.core.permissions import (
    require_role
)

from app.core.auth import (
    get_current_user
)

from app.utils.background_tasks import (
    print_message
)

from app.tasks.email_tasks import (
    send_email_task
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return EmployeeService.create_employee(
        db,
        employee,
        current_user["email"]
    )

@router.get("/redis-test")
async def redis_test():

    redis_client.set(
        "test_key",
        "Hello Redis"
    )

    value = redis_client.get(
        "test_key"
    )

    return {
        "value": value
    }

@router.get(
    "/",
    response_model=List[EmployeeResponse]
)
async def get_employees(
    page: int = Query(1),
    limit: int = Query(10),
    db: Session = Depends(get_db),
    current_user = Depends(
        get_current_user
    )
):

    return EmployeeService.get_all_employees(
        db,
        page,
        limit
    )

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
async def get_employee(
    employee_id: str,
    db: Session = Depends(get_db)
):

    return EmployeeService.get_employee_by_id(
        db,
        employee_id
    )


@router.delete(
    "/{employee_id}",
    response_model=EmployeeResponse
)
async def delete_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(["admin"])
    )
):

    return EmployeeService.delete_employee(
        db,
        employee_id,
        current_user["email"]
    )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
async def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):

    return EmployeeService.update_employee(
        db,
        employee_id,
        employee_data,
        current_user["email"]
    )


@router.post("/test-background")
async def test_background(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        print_message
    )

    return {
        "message": "Task started"
    }


@router.post("/test-celery")
async def test_celery():

    task = send_email_task.delay()

    return {
        "message": "Task queued",
        "task_id": task.id
    }