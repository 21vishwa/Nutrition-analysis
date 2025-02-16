import streamlit as st
from db_operations import insert_user, verify_user, user_exists

def handle_login_signup():
    """ Handle user login and signup """
    if st.radio("Select an option:", ["Login", "Signup"]) == "Login":
        user_name = st.text_input("User Name:")
        password = st.text_input("Password:", type='password')
        if st.button("Login"):
            if verify_user(user_name, password):
                st.session_state['logged_in'] = True
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    else:
        new_user_name = st.text_input("New User Name:")
        new_password = st.text_input("New Password:", type='password')
        if st.button("Signup"):
            if user_exists(new_user_name):
                st.error("User name already exists.")
            else:
                insert_user(new_user_name, new_password)
                st.success("User created successfully! You can now log in.")
