
import streamlit as st

def check_password(username, password):
    """
    Simple hardcoded authentication.
    In a real app, you would verify against a database or secure storage.
    """
    return username == "admin" and password == "admin123"

def login_form():
    """renders the login form and handles authentication state"""
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 50px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            background-color: #f9f9f9;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔒 Login")
        st.write("Please sign in to access the system.")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if check_password(username, password):
                    st.session_state["logged_in"] = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
