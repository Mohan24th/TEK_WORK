import streamlit as st
import pandas as pd
from db import get_connection

def add_marks():
    st.header("Add Marks")

    conn = get_connection()
    students = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if students.empty:
        st.warning("No students available")
        return

    student_map = {
        f"{row.roll_no} - {row.name}": row.id
        for _, row in students.iterrows()
    }

    with st.form("marks_form"):
        student = st.selectbox("Student", student_map.keys())
        subject = st.selectbox("Subject", ["Maths", "Science", "English", "CS"])
        marks = st.number_input("Marks", min_value=0, max_value=100)
        submit = st.form_submit_button("Add Marks")

    if submit:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (%s, %s, %s)",
            (student_map[student], subject, marks)
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("Marks added")
