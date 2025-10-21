import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("👔 Employee Management System")

menu = ["View Employees", "Add Employee", "Update Employee", "Delete Employee"]
choice = st.sidebar.selectbox("Menu", menu)

# --- READ ---
if choice == "View Employees":
    st.subheader("Employee List")
    res = requests.get(f"{API_URL}/employees")
    if res.status_code == 200:
        employees = res.json()
        st.table(employees)
    else:
        st.error("Failed to fetch employees")

# --- CREATE ---
elif choice == "Add Employee":
    st.subheader("Add New Employee")
    name = st.text_input("Name")
    emp_id = st.number_input("Employee ID", min_value=1)
    tshirt = st.selectbox("T-Shirt Size", ["S", "M", "L", "XL", "XXL"])

    if st.button("Add Employee"):
        data = {"Name": name, "EmpId": emp_id, "Tshirt_Size": tshirt}
        res = requests.post(f"{API_URL}/employees", json=data)
        if res.status_code == 200:
            st.success("✅ Employee added successfully!")
        else:
            st.error(res.json()["detail"])

# --- UPDATE ---
elif choice == "Update Employee":
    st.subheader("Update Employee Details")
    emp_id = st.number_input("Enter Employee ID to update", min_value=1)
    name = st.text_input("New Name")
    tshirt = st.selectbox("New T-Shirt Size", ["S", "M", "L", "XL", "XXL"])

    if st.button("Update Employee"):
        data = {"Name": name, "EmpId": emp_id, "Tshirt_Size": tshirt}
        res = requests.put(f"{API_URL}/employees/{emp_id}", json=data)
        if res.status_code == 200:
            st.success("✅ Employee updated successfully!")
        else:
            st.error(res.json()["detail"])

# --- DELETE ---
elif choice == "Delete Employee":
    st.subheader("Delete Employee")
    emp_id = st.number_input("Enter Employee ID to delete", min_value=1)

    if st.button("Delete"):
        res = requests.delete(f"{API_URL}/employees/{emp_id}")
        if res.status_code == 200:
            st.success("🗑️ Employee deleted successfully!")
        else:
            st.error(res.json()["detail"])
