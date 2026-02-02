import streamlit as st
import pandas as pd
from datetime import date
from db import get_connection

def mark_attendance():
    st.header("Mark Attendance")

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

    with st.form("attendance_form"):
        student = st.selectbox("Student", student_map.keys())
        att_date = st.date_input("Date", date.today())
        status = st.radio("Status", ["Present", "Absent"])
        submit = st.form_submit_button("Submit Attendance")

    if submit:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
            (student_map[student], att_date, status)
        )
        conn.commit()
        cursor.close()
        conn.close()

        st.success("Attendance marked")
