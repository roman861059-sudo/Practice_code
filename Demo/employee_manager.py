import json
import os

class EmployeeManager:
    def __init__(self, json_file="employees.json"):
        self.json_file = json_file
        self.employees = self.load_employees()

    def load_employees(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_employees(self):
        with open(self.json_file, "w") as f:
            json.dump(self.employees, f, indent=4)

    def add_employee(self, name: str, emp_id: int, tshirt_size: str):
        if any(emp["EmpId"] == emp_id for emp in self.employees):
            return {"error": "Employee ID already exists"}
        new_emp = {"Name": name, "EmpId": emp_id, "Tshirt_Size": tshirt_size}
        self.employees.append(new_emp)
        self.save_employees()
        return {"message": "Employee added successfully", "employee": new_emp}

    def get_all_employees(self):
        return self.employees

    def get_employee(self, emp_id: int):
        for emp in self.employees:
            if emp["EmpId"] == emp_id:
                return emp
        return {"error": "Employee not found"}

    def update_employee(self, emp_id: int, name: str, tshirt_size: str):
        for emp in self.employees:
            if emp["EmpId"] == emp_id:
                emp["Name"] = name
                emp["Tshirt_Size"] = tshirt_size
                self.save_employees()
                return {"message": "Employee updated successfully", "employee": emp}
        return {"error": "Employee not found"}

    def delete_employee(self, emp_id: int):
        for i, emp in enumerate(self.employees):
            if emp["EmpId"] == emp_id:
                removed = self.employees.pop(i)
                self.save_employees()
                return {"message": "Employee deleted successfully", "employee": removed}
        return {"error": "Employee not found"}
