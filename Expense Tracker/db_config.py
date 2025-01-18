import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",         # Replace with your database host (e.g., localhost)
        user="root",     # Replace with your MySQL username
        password="1379", # Replace with your MySQL password
        database="expense_tracker" # Replace with your database name
    )
