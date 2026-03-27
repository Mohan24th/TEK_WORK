import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mohan@2406",
        database="actor_db",
    )

def create_user(name, no_of_movies, last_movie):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO actor(name,no_of_movies,last_movie) VALUES (%s, %s, %s)",
        (name, no_of_movies, last_movie)
    )
    conn.commit()
    conn.close()

def read_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM actor")
    users = cur.fetchall()
    conn.close()
    return users

def update_user(id, name, no_of_movies, last_movie):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE actor SET name=%s,no_of_movies=%s,last_movie=%s WHERE id=%s",
        (name, no_of_movies, last_movie, id)
    )
    conn.commit()
    conn.close()

def delete_user(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM actor WHERE id=%s", (id,))
    conn.commit()
    conn.close()
