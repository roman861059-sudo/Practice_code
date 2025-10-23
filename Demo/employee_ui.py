import streamlit as st
import pandas as pd
import os
import re
import json
from io import BytesIO

# =========================================
# File paths
# =========================================
EMP_FILE = "emp_details.csv"
PERF_FILE = "performance.csv"
EMP_JSON = "emp_details.json"
PERF_JSON = "performance.json"

# =========================================
# Ensure CSV files exist
# =========================================
def ensure_csv(file_path, columns):
    """Ensure CSV exists with proper columns."""
    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

ensure_csv(EMP_FILE, ["name", "empid", "doj", "avg_performance", "comments", "verdict"])
ensure_csv(PERF_FILE, ["empid", "name", "performance_year", "band", "overall_feedback", "verdict"])

# =========================================
# Sentiment-based verdict logic
# =========================================
POSITIVE = {"good", "great", "excellent", "awesome", "well", "positive", "productive", "hardworking", "improved", "strong", "outstanding"}
NEGATIVE = {"bad", "poor", "late", "unreliable", "issues", "problem", "negative", "slow", "underperform", "weak", "inconsistent"}

def basic_sentiment(comment):
    """Simple keyword-based verdict."""
    if not comment or not str(comment).strip():
        return "Neutral"
    tokens = re.findall(r"\w+", comment.lower())
    pos = sum(1 for w in tokens if w in POSITIVE)
    neg = sum(1 for w in tokens if w in NEGATIVE)
    if pos > neg:
        return "Good"
    elif neg > pos:
        return "Bad"
    else:
        return "Neutral"

# =========================================
# CSV and JSON Helpers
# =========================================
def load_csv(file_path):
    return pd.read_csv(file_path)

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

def save_json(df, json_path):
    df.to_json(json_path, orient="records", indent=4)

def download_link(df, filename):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        label=f"📥 Download {filename}",
        data=buffer,
        file_name=filename,
        mime="text/csv"
    )

# =========================================
# Ensure verdict column logic
# =========================================
def ensure_verdict_columns():
    """Ensure both CSVs have 'verdict' and fill missing."""
    for file_path, text_col, json_path in [
        (EMP_FILE, "comments", EMP_JSON),
        (PERF_FILE, "overall_feedback", PERF_JSON)
    ]:
        df = load_csv(file_path)
        if "verdict" not in df.columns:
            df["verdict"] = None
        for i, row in df.iterrows():
            if pd.isna(row.get("verdict")) or not row.get("verdict"):
                df.at[i, "verdict"] = basic_sentiment(row.get(text_col, ""))
        save_csv(df, file_path)
        save_json(df, json_path)

# Run check on startup
ensure_verdict_columns()

# =========================================
# Streamlit UI
# =========================================
st.set_page_config(page_title="Employee Management System", layout="wide")
st.title("📊 Employee Management System (CSV + JSON + Auto Verdict)")

menu = [
    "View Employees", "Add Employee", "Update Employee", "Delete Employee",
    "View Performance", "Add Performance", "Update Performance", "Delete Performance",
    "📤 Upload / 📥 Download CSVs"
]
choice = st.sidebar.selectbox("Menu", menu)

# =========================================
# Employee CRUD
# =========================================
if choice == "View Employees":
    st.subheader("Employee List")
    df = load_csv(EMP_FILE)
    if not df.empty:
        st.dataframe(df)
        download_link(df, "emp_details.csv")
        st.success(f"Employee data also saved to {EMP_JSON}")
    else:
        st.warning("No employee data found.")

elif choice == "Add Employee":
    st.subheader("Add New Employee")
    name = st.text_input("Name")
    empid = st.text_input("Employee ID")
    doj = st.date_input("Date of Joining")
    avg_perf = st.number_input("Average Performance", min_value=0.0, max_value=5.0, step=0.1)
    comments = st.text_area("Comments / Feedback about Employee")

    if st.button("Add Employee"):
        df = load_csv(EMP_FILE)
        if empid in df["empid"].astype(str).values:
            st.error("Employee ID already exists.")
        else:
            verdict = basic_sentiment(comments)
            new_row = {"name": name, "empid": empid, "doj": doj, "avg_performance": avg_perf, "comments": comments, "verdict": verdict}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(df, EMP_FILE)
            save_json(df, EMP_JSON)
            st.success(f"✅ Added {name} (ID: {empid}) — Verdict: {verdict}")

elif choice == "Update Employee":
    st.subheader("Update Employee")
    df = load_csv(EMP_FILE)
    if df.empty:
        st.warning("No employees found.")
    else:
        empids = df["empid"].astype(str).tolist()
        empid = st.selectbox("Select Employee ID", empids)
        emp = df[df["empid"].astype(str) == empid].iloc[0]

        new_name = st.text_input("Name", emp["name"])
        new_doj = st.date_input("Date of Joining", pd.to_datetime(emp["doj"]))
        new_avg = st.number_input("Average Performance", min_value=0.0, max_value=5.0, value=float(emp["avg_performance"]), step=0.1)
        new_comments = st.text_area("Comments", emp.get("comments", ""))
        new_verdict = basic_sentiment(new_comments)
        st.info(f"Updated Verdict: {new_verdict}")

        if st.button("Update"):
            df.loc[df["empid"].astype(str) == empid, ["name", "doj", "avg_performance", "comments", "verdict"]] = [
                new_name, new_doj, new_avg, new_comments, new_verdict
            ]
            save_csv(df, EMP_FILE)
            save_json(df, EMP_JSON)
            st.success(f"✅ Updated employee ID {empid}")

elif choice == "Delete Employee":
    st.subheader("Delete Employee")
    df = load_csv(EMP_FILE)
    if df.empty:
        st.warning("No employees found.")
    else:
        empids = df["empid"].astype(str).tolist()
        empid = st.selectbox("Select Employee ID to Delete", empids)
        if st.button("Delete"):
            df = df[df["empid"].astype(str) != empid]
            save_csv(df, EMP_FILE)
            save_json(df, EMP_JSON)
            st.success(f"🗑️ Deleted employee ID {empid}")

# =========================================
# Performance CRUD
# =========================================
elif choice == "View Performance":
    st.subheader("Performance Records")
    df = load_csv(PERF_FILE)
    if not df.empty:
        st.dataframe(df)
        download_link(df, "performance.csv")
        st.success(f"Performance data also saved to {PERF_JSON}")
    else:
        st.warning("No performance data found.")

elif choice == "Add Performance":
    st.subheader("Add New Performance")
    empid = st.text_input("Employee ID")
    name = st.text_input("Employee Name")
    year = st.number_input("Performance Year", min_value=2000, max_value=2100, step=1)
    band = st.selectbox("Performance Band", ["A+", "A", "B", "C", "D"])
    feedback = st.text_area("Overall Feedback")

    if st.button("Add Performance"):
        df = load_csv(PERF_FILE)
        exists = df[(df["empid"].astype(str) == empid) & (df["performance_year"].astype(int) == year)]
        if not exists.empty:
            st.error("A record for this employee and year already exists.")
        else:
            verdict = basic_sentiment(feedback)
            new_row = {"empid": empid, "name": name, "performance_year": year, "band": band, "overall_feedback": feedback, "verdict": verdict}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(df, PERF_FILE)
            save_json(df, PERF_JSON)
            st.success(f"✅ Added performance for {name} ({year}) — Verdict: {verdict}")

elif choice == "Update Performance":
    st.subheader("Update Performance Record")
    df = load_csv(PERF_FILE)
    if df.empty:
        st.warning("No performance data found.")
    else:
        keys = df.apply(lambda x: f"{x['empid']} - {x['performance_year']}", axis=1).tolist()
        record_key = st.selectbox("Select Record", keys)
        empid, year = record_key.split(" - ")

        record = df[(df["empid"].astype(str) == empid) & (df["performance_year"].astype(str) == year)].iloc[0]
        new_band = st.selectbox("Band", ["A+", "A", "B", "C", "D"], index=["A+", "A", "B", "C", "D"].index(record["band"]))
        new_feedback = st.text_area("Feedback", record["overall_feedback"])
        new_verdict = basic_sentiment(new_feedback)
        st.info(f"Updated Verdict: {new_verdict}")

        if st.button("Update"):
            df.loc[(df["empid"].astype(str) == empid) & (df["performance_year"].astype(str) == year),
                   ["band", "overall_feedback", "verdict"]] = [new_band, new_feedback, new_verdict]
            save_csv(df, PERF_FILE)
            save_json(df, PERF_JSON)
            st.success(f"✅ Updated performance for {record['name']} ({year})")

elif choice == "Delete Performance":
    st.subheader("Delete Performance Record")
    df = load_csv(PERF_FILE)
    if df.empty:
        st.warning("No performance data found.")
    else:
        keys = df.apply(lambda x: f"{x['empid']} - {x['performance_year']}", axis=1).tolist()
        record_key = st.selectbox("Select Record to Delete", keys)
        if st.button("Delete"):
            empid, year = record_key.split(" - ")
            df = df[~((df["empid"].astype(str) == empid) & (df["performance_year"].astype(str) == year))]
            save_csv(df, PERF_FILE)
            save_json(df, PERF_JSON)
            st.success(f"🗑️ Deleted performance record for {empid} ({year})")

# =========================================
# Upload / Download CSV
# =========================================
elif choice == "📤 Upload / 📥 Download CSVs":
    st.subheader("📤 Upload / 📥 Download CSV Files")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Upload CSV Files")
        uploaded_emp = st.file_uploader("Upload Employee CSV", type=["csv"])
        uploaded_perf = st.file_uploader("Upload Performance CSV", type=["csv"])

        if uploaded_emp is not None:
            df = pd.read_csv(uploaded_emp)
            save_csv(df, EMP_FILE)
            save_json(df, EMP_JSON)
            st.success("✅ Employee CSV uploaded!")

        if uploaded_perf is not None:
            df = pd.read_csv(uploaded_perf)
            save_csv(df, PERF_FILE)
            save_json(df, PERF_JSON)
            st.success("✅ Performance CSV uploaded!")

    with col2:
        st.markdown("### Download Existing CSV Files")
        download_link(load_csv(EMP_FILE), "emp_details.csv")
        download_link(load_csv(PERF_FILE), "performance.csv")
