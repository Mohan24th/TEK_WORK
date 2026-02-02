import streamlit as st
from db import get_connection
import re

st.title(" Online Complaint Registration System")

# ----------------- Complaint Submission -----------------
st.header("Submit a Complaint")

name = st.text_input("Name")
email = st.text_input("Email")
category = st.selectbox("Category", ["Technical", "Service", "Billing", "Other"])
description = st.text_area("Complaint Description")

if st.button("Submit Complaint"):
    if not name or not email or not description:
        st.error("All fields are required")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Invalid email format")
    else:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO complaints (name, email, category, description)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, category, description))
            conn.commit()
            complaint_id = cursor.lastrowid
            cursor.close()
            conn.close()

            st.success(f"Complaint submitted successfully!")
            st.info(f"Your Complaint ID is: {complaint_id}")

# ----------------- Complaint Status Check -----------------
st.header("Check Complaint Status")

search_id = st.text_input("Enter Complaint ID")

if st.button("Check Status"):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM complaints WHERE id = %s", (search_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            with st.expander("Complaint Details"):
                st.write("**Name:**", result["name"])
                st.write("**Category:**", result["category"])
                st.write("**Description:**", result["description"])
                st.write("**Status:**", result["status"])
                st.write("**Created At:**", result["created_at"])
        else:
            st.error("Complaint ID not found")

