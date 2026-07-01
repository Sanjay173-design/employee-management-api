from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EmployeeCreate(BaseModel):
    name: str
    age: int
    department: str
    salary: float


class EmployeeResponse(BaseModel):
    id: UUID
    name: str
    age: int
    department: str
    salary: float
    created_at: datetime

class EmployeeUpdate(BaseModel):
    name: str
    age: int
    department: str
    salary: float    