import streamlit as st
from db import get_connection

st.title(" Admin Complaint Management")

menu = st.sidebar.selectbox(
    "Admin Menu",
    ["View All Complaints", "Search Complaint", "Update Complaint Status"]
)

# ----------------- VIEW ALL -----------------
if menu == "View All Complaints":
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
        complaints = cursor.fetchall()
        cursor.close()
        conn.close()

        for c in complaints:
            with st.expander(f"Complaint ID: {c['id']} | Status: {c['status']}"):
                st.write("**Name:**", c["name"])
                st.write("**Email:**", c["email"])
                st.write("**Category:**", c["category"])
                st.write("**Description:**", c["description"])
                st.write("**Created At:**", c["created_at"])

# ----------------- SEARCH -----------------
elif menu == "Search Complaint":
    cid = st.text_input("Enter Complaint ID")
    if st.button("Search"):
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM complaints WHERE id = %s", (cid,))
            c = cursor.fetchone()
            cursor.close()
            conn.close()

            if c:
                st.success("Complaint Found")
                st.write(c)
            else:
                st.error("Complaint not found")

# ----------------- UPDATE STATUS -----------------
elif menu == "Update Complaint Status":
    cid = st.text_input("Complaint ID")
    new_status = st.selectbox("Update Status", ["Open", "In Progress", "Closed"])

    if st.button("Update"):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE complaints SET status = %s WHERE id = %s",
                (new_status, cid)
            )
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()

            if affected:
                st.success("Status updated successfully")
            else:
                st.error("Invalid Complaint ID")
