import streamlit as st
from db import register, login

st.set_page_config(page_title="Authorize", layout="centered")

menu = st.sidebar.selectbox(
    "Choose Operation",
    ["Register", "Login"]
)

if menu == "Register":
    st.subheader("Register here")

    with st.form("Register"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            if register(username, password):
                st.success("Registration Successful")
            else:
                st.error("Registration Failed")

elif menu == "Login":
    st.subheader("Login here")

    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if login(username, password):
                st.success("Login Successful ✅")
            else:
                st.error("Invalid Username or Password ❌")
