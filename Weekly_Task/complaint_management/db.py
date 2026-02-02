import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mohan@2406",
            database="complaint_db"
        )
        return conn
    except Error as e:
        print("Database connection error:", e)
        return None
