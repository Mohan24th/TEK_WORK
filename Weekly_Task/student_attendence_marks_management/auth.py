import streamlit as st

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.success("Login successful")
            else:
                st.error("Invalid credentials")

        return False

    return True
