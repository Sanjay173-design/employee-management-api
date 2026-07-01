from sqlalchemy.orm import Session

from app.models.employee_model import Employee


class EmployeeRepository:

    @staticmethod
    def create_employee(
        db: Session,
        employee: Employee
    ):

        db.add(employee)

        db.commit()

        db.refresh(employee)

        return employee

    @staticmethod
    def get_all_employees(
        db: Session,
        page=1,
        limit=10,
        department=None,
        name=None,
        sort_by=None
    ):

        query = db.query(Employee)

        if department:

            query = query.filter(
                Employee.department == department
            )

        if name:

            query = query.filter(
                Employee.name.ilike(
                    f"%{name}%"
                )
            )

        if sort_by == "salary":

            query = query.order_by(
                Employee.salary.desc()
            )

        elif sort_by == "created_at":

            query = query.order_by(
                Employee.created_at.desc()
            )

        offset = (
            page - 1
        ) * limit

        return (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_employee_by_id(
        db: Session,
        employee_id
    ):

        return db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

    @staticmethod
    def delete_employee(
        db: Session,
        employee
    ):

        db.delete(employee)

        db.commit()

    @staticmethod
    def update_employee(
        db: Session
    ):

        db.commit()