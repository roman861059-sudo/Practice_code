# employee_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from employee_manager import EmployeeManager   # ✅ Make sure employee_manager.py is in the same folder

# Initialize FastAPI app
app = FastAPI(title="Employee Info API", version="3.0")

# Initialize Employee Manager (handles JSON file operations)
manager = EmployeeManager("employees.json")

# Define the data model for requests
class Employee(BaseModel):
    Name: str
    EmpId: int
    Tshirt_Size: str

# --- API ROUTES ---

@app.get("/")
def home():
    return {"message": "Welcome to the Employee Info API"}

# READ all employees
@app.get("/employees")
def get_all_employees():
    return manager.get_all_employees()

# READ one employee by ID
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    result = manager.get_employee(emp_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# CREATE new employee
@app.post("/employees")
def add_employee(emp: Employee):
    result = manager.add_employee(emp.Name, emp.EmpId, emp.Tshirt_Size)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# UPDATE existing employee
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Employee):
    result = manager.update_employee(emp_id, emp.Name, emp.Tshirt_Size)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# DELETE employee
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    result = manager.delete_employee(emp_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
