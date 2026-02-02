import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_connection

st.set_page_config(page_title="Student Performance System", layout="wide")
st.title(" Student Performance Management System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Student",
        "View Students",
        "Update Marks",
        "Delete Student",
        "Performance Analysis",
    ]
)

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":
    st.header("Add Student")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0, max_value=100, step=1)

    if st.button("Add Student"):
        if not name or not subject:
            st.error("All fields are required")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, age, subject, marks) VALUES (%s, %s, %s, %s)",
                (name, age, subject, marks),
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Student added successfully")

# ---------------- VIEW STUDENTS ----------------
elif menu == "View Students":
    st.header("All Students")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    st.dataframe(df)

# ---------------- UPDATE MARKS ----------------
elif menu == "Update Marks":
    st.header("Update Student Marks")

    student_id = st.number_input("Student ID", step=1)
    new_marks = st.number_input("New Marks", min_value=0, max_value=100)

    if st.button("Update"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET marks=%s WHERE id=%s",
            (new_marks, student_id),
        )
        conn.commit()

        if cursor.rowcount:
            st.success("Marks updated successfully")
        else:
            st.error("Invalid Student ID")

        cursor.close()
        conn.close()

# ---------------- DELETE STUDENT ----------------
elif menu == "Delete Student":
    st.header("Delete Student")

    student_id = st.number_input("Student ID", step=1)

    if st.button("Delete"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        conn.commit()

        if cursor.rowcount:
            st.success("Student deleted successfully")
        else:
            st.error("Invalid Student ID")

        cursor.close()
        conn.close()

# ---------------- PERFORMANCE ANALYSIS ----------------
elif menu == "Performance Analysis":
    st.header("Performance Analysis")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()

    if df.empty:
        st.warning("No data available")
    else:
        df["Status"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

        avg_marks = df["marks"].mean()
        pass_percentage = (df["Status"] == "Pass").mean() * 100
        top_scorer = df.loc[df["marks"].idxmax()]

        st.metric("Average Marks", round(avg_marks, 2))
        st.metric("Pass Percentage", f"{pass_percentage:.2f}%")
        st.metric("Top Scorer", f"{top_scorer['name']} ({top_scorer['marks']})")

        st.subheader("Average Marks per Subject")
        subject_avg = df.groupby("subject")["marks"].mean()

        fig, ax = plt.subplots()
        subject_avg.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.subheader("Pass / Fail Ratio")
        pf_counts = df["Status"].value_counts()

        fig2, ax2 = plt.subplots()
        ax2.pie(pf_counts, labels=pf_counts.index, autopct="%1.1f%%")
        st.pyplot(fig2)
