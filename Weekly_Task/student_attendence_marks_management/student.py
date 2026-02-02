import streamlit as st
from db import get_connection

def add_student():
    st.header("Add Student")

    with st.form("add_student"):
        roll = st.text_input("Roll No")
        name = st.text_input("Name")
        cls = st.selectbox("Class", ["AI-A","AI-B","AI-C","AI-D","AI-E","AIML-A","AIML-B","AIML-C","AIML-D","AIML-E","AIML-F"])
        submit = st.form_submit_button("Add Student")

    if submit:
        if not roll or not name:
            st.error("All fields required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (roll_no, name, class) VALUES (%s, %s, %s)",
            (roll, name, cls)
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("Student added successfully")
