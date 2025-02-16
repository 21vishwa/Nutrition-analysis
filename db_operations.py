# db_operations.py
import mysql.connector
from mysql.connector import Error
import streamlit as st

def create_connection():
    """ Create a database connection """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='Vishwa@123',  # Replace with your MySQL password
            database='nutrition_tracker'  # Use the created database
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def insert_meal(user_name, meal_date, meal_time, nutrition_analysis):
    """ Insert a new meal record into the meals table """
    connection = create_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return

    cursor = connection.cursor()
    query = """
    INSERT INTO meals (user_name, meal_date, meal_time, nutrition_analysis)
    VALUES (%s, %s, %s, %s);
    """
    try:
        cursor.execute(query, (user_name, meal_date, meal_time, nutrition_analysis))
        connection.commit()
        print("Meal record inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def insert_user(user_name, password):
    """ Insert a new user into the users table """
    connection = create_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return

    cursor = connection.cursor()
    query = """
    INSERT INTO users (user_name, password)
    VALUES (%s, %s);
    """
    try:
        cursor.execute(query, (user_name, password))
        connection.commit()
        print("User record inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def user_exists(user_name):
    """ Check if a user exists in the database """
    connection = create_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return False

    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE user_name = %s"
    cursor.execute(query, (user_name,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user is not None

def verify_user(user_name, password):
    """ Verify user credentials """
    connection = create_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return False

    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE user_name = %s AND password = %s"
    cursor.execute(query, (user_name, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user is not None

def get_meals_for_user(user_name, meal_date):
    """ Retrieve meals for a user on a specific date """
    connection = create_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return []

    cursor = connection.cursor()
    query = """
    SELECT meal_time, nutrition_analysis 
    FROM meals 
    WHERE user_name = %s AND meal_date = %s;
    """
    cursor.execute(query, (user_name, meal_date))
    meals = cursor.fetchall()
    cursor.close()
    connection.close()
    return meals
