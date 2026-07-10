import streamlit as st 
from core import session_manager

def show():
    st.title("Syntax Trainer")
    st.caption("Login or create an account to start")

    with st.form("auth_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        name = st.text_input("Name (sign up only)")

        col1, col2 = st.columns(2)
        with col1:
            sign_in_btn = st.form_submit_button("Sign In")
        with col2:
            sign_up_btn = st.form_submit_button("Sign Up")
    
    if sign_in_btn:
        result = session_manager.sign_in(email, password)
        if "successful" in result:
            st.rerun()
        else:
            st.error(result)
    if sign_up_btn:
        result = session_manager.sign_up(email, password, name)
        if "successful" in result:
            st.rerun()
        else:
            st.error(result)
    
    