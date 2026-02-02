import streamlit as st
from auth import login
from student import add_student
from attendance import mark_attendance
from marks import add_marks
from views import view_attendance, view_performance

st.set_page_config(page_title="Attendance & Marks Portal", layout="wide")
st.title("📘 Student Attendance & Marks Portal")

if not login():
    st.stop()

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Student",
        "Mark Attendance",
        "Add Marks",
        "View Attendance",
        "View Performance"
    ]
)

if menu == "Add Student":
    add_student()
elif menu == "Mark Attendance":
    mark_attendance()
elif menu == "Add Marks":
    add_marks()
elif menu == "View Attendance":
    view_attendance()
elif menu == "View Performance":
    view_performance()
