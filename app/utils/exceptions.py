class EmployeeNotFoundException(Exception):

    def __init__(self, employee_id):

        self.message = f"Employee with ID {employee_id} not found"

        super().__init__(self.message)