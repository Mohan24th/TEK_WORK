import streamlit as st
import pandas as pd
from db import create_user, read_users, update_user, delete_user

st.set_page_config(page_title="Actor CRUD App", layout="centered")
st.title("🎬 Actor Database Management")

menu = st.sidebar.selectbox(
    "Choose Operation",
    ["Create", "Read", "Update", "Delete"]
)


if menu == "Create":
    st.subheader("Add New Actor")

    with st.form("create_actor"):
        name = st.text_input("Actor Name")
        no_of_movies = st.number_input("Number of Movies", min_value=0)
        last_movie = st.text_input("Last Movie")
        submit = st.form_submit_button("Add Actor")

    if submit:
        if name and last_movie:
            create_user(name, no_of_movies, last_movie)
            st.success("Actor added successfully ")
        else:
            st.error("Please fill all fields")

# READ
elif menu == "Read":
    st.subheader("View Actors")
    data = read_users()

    if data:
        df = pd.DataFrame(
            data,
            columns=["ID", "Name", "No of Movies", "Last Movie"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No actors found")

# UPDATE
elif menu == "Update":
    st.subheader(" Update Actor Details")
    data = read_users()

    if data:
        actor_ids = [actor[0] for actor in data]
        selected_id = st.selectbox("Select Actor ID", actor_ids)

        selected_actor = next(actor for actor in data if actor[0] == selected_id)

        with st.form("update_actor"):
            name = st.text_input("Actor Name", selected_actor[1])
            no_of_movies = st.number_input(
                "Number of Movies",
                min_value=0,
                value=selected_actor[2]
            )
            last_movie = st.text_input("Last Movie", selected_actor[3])
            update = st.form_submit_button("Update Actor")

        if update:
            update_user(selected_id, name, no_of_movies, last_movie)
            st.success("Actor updated successfully ")
            st.rerun()
    else:
        st.info("No actors available")

# DELETE
elif menu == "Delete":
    st.subheader(" Delete Actor")
    data = read_users()

    if data:
        actor_ids = [actor[0] for actor in data]
        selected_id = st.selectbox("Select Actor ID", actor_ids)

        if st.button("Delete Actor"):
            delete_user(selected_id)
            st.warning("Actor deleted ")
            st.rerun()
    else:
        st.info("No actors available")
