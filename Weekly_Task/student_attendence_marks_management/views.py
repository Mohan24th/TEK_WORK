import streamlit as st
import pandas as pd
from db import get_connection

def view_attendance():
    st.header("Attendance History")

    conn = get_connection()
    df = pd.read_sql("""
        SELECT s.roll_no, s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
    """, conn)
    conn.close()

    st.dataframe(df)

def view_performance():
    st.header("Performance Overview")

    conn = get_connection()

    marks_df = pd.read_sql("""
        SELECT s.name, m.subject, m.marks
        FROM marks m
        JOIN students s ON m.student_id = s.id
    """, conn)

    attendance_df = pd.read_sql("""
        SELECT s.name,
        SUM(a.status='Present') / COUNT(*) * 100 AS attendance_percentage
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        GROUP BY s.name
    """, conn)

    conn.close()

    marks_df["Result"] = marks_df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

    st.subheader("Marks")
    st.dataframe(marks_df)

    st.subheader("Attendance Percentage")
    st.dataframe(attendance_df)

    st.subheader("Pass / Fail Status")
    st.dataframe(marks_df)
