import os
import json

from uuid import uuid4
from datetime import datetime

from app.models.employee_model import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.services.audit_service import AuditService
from app.utils.exceptions import EmployeeNotFoundException
from app.core.redis_client import redis_client
from app.core.logger import logger

class EmployeeService:

    @staticmethod
    def create_employee(
        db,
        employee_data,
        user_email
    ):

        logger.info(
            f"Creating employee: {employee_data.name}"
        )

        employee = Employee(
            id=uuid4(),
            name=employee_data.name,
            age=employee_data.age,
            department=employee_data.department,
            salary=employee_data.salary,
            created_at=datetime.now()
        )

        created_employee = EmployeeRepository.create_employee(
            db,
            employee
        )

        redis_client.delete(
            "employees:1:10"
        )

        AuditService.log_action(
            db,
            user_email,
            "CREATE",
            "Employee",
            created_employee.id
        )

        logger.info(
            f"Employee created successfully: {created_employee.id}"
        )

        return created_employee

    @staticmethod
    def get_all_employees(
        db,
        page,
        limit,
        department=None,
        name=None,
        sort_by=None
    ):

        testing = (
            os.getenv(
                "TESTING",
                "False"
            ) == "True"
        )

        if testing:

            logger.info(
                "Running in test mode - skipping Redis cache"
            )

            return EmployeeRepository.get_all_employees(
                db,
                page,
                limit,
                department,
                name,
                sort_by
            )

        logger.info(
            f"Fetching employees page={page} limit={limit}"
        )

        cache_key = (
           f"employees:"
           f"{page}:"
           f"{limit}:"
           f"{department}:"
           f"{name}:"
           f"{sort_by}"
    )

        cached_data = redis_client.get(
            cache_key
        )

        if cached_data:

            logger.info(
                f"Cache hit for key {cache_key}"
            )

            return json.loads(
                cached_data
            )

        logger.info(
            f"Cache miss for key {cache_key}"
        )

        employees = EmployeeRepository.get_all_employees(
            db,
            page,
            limit
        )

        serialized = []

        for employee in employees:

            serialized.append(
                {
                    "id": str(employee.id),
                    "name": employee.name,
                    "age": employee.age,
                    "department": employee.department,
                    "salary": employee.salary,
                    "created_at": employee.created_at.isoformat()
                }
            )

        redis_client.set(
            cache_key,
            json.dumps(serialized),
            ex=60
        )

        logger.info(
            f"Stored {len(serialized)} employees in cache"
        )

        return serialized

    @staticmethod
    def get_employee_by_id(
        db,
        employee_id
    ):

        logger.info(
            f"Fetching employee {employee_id}"
        )

        employee = EmployeeRepository.get_employee_by_id(
            db,
            employee_id
        )

        if not employee:

            logger.warning(
                f"Employee not found: {employee_id}"
            )

            raise EmployeeNotFoundException(
                employee_id
            )

        return employee

    @staticmethod
    def update_employee(
        db,
        employee_id,
        updated_data,
        user_email
    ):

        logger.info(
            f"Updating employee {employee_id}"
        )

        employee = EmployeeRepository.get_employee_by_id(
            db,
            employee_id
        )

        if not employee:

            logger.warning(
                f"Employee not found: {employee_id}"
            )

            raise EmployeeNotFoundException(
                employee_id
            )

        employee.name = updated_data.name
        employee.age = updated_data.age
        employee.department = updated_data.department
        employee.salary = updated_data.salary

        EmployeeRepository.update_employee(
            db
        )

        redis_client.delete(
            "employees:1:10"
        )

        AuditService.log_action(
            db,
            user_email,
            "UPDATE",
            "Employee",
            employee_id
        )

        logger.info(
            f"Employee updated successfully: {employee_id}"
        )

        return employee

    @staticmethod
    def delete_employee(
        db,
        employee_id,
        user_email
    ):

        logger.warning(
            f"Deleting employee {employee_id}"
        )

        employee = EmployeeRepository.get_employee_by_id(
            db,
            employee_id
        )

        if not employee:

            logger.warning(
                f"Employee not found: {employee_id}"
            )

            raise EmployeeNotFoundException(
                employee_id
            )

        EmployeeRepository.delete_employee(
            db,
            employee
        )

        redis_client.delete(
            "employees:1:10"
        )

        AuditService.log_action(
            db,
            user_email,
            "DELETE",
            "Employee",
            employee_id
        )

        logger.warning(
            f"Employee deleted successfully: {employee_id}"
        )

        return employee