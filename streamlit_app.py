import altair as alt
import numpy as np
import pandas as pd
import streamlit as st




import sqlite3
from datetime import datetime

# Function to create a database connection
def create_connection():
    conn = sqlite3.connect("appointments.db")
    return conn

# Function to create the appointments table in the database
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        patient_age INTEGER,
        patient_gender TEXT,
        patient_issues TEXT,
        appointment_date TEXT,
        appointment_time TEXT
    );
    """
    conn.execute(create_table_sql)

# Function to insert an appointment into the database
def insert_appointment(conn, appointment):
    insert_sql = """
    INSERT INTO appointments (patient_name, patient_age, patient_gender, patient_issues, appointment_date, appointment_time)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    conn.execute(insert_sql, appointment)
    conn.commit()

# Function to retrieve all appointments from the database
def get_all_appointments(conn):
    select_sql = "SELECT * FROM appointments"
    return pd.read_sql(select_sql, conn)

# Function to create the users table in the database
def create_users_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL
    );
    """
    conn.execute(create_table_sql)

# Function to insert a new user into the database
def insert_user(conn, username, password, user_type):
    insert_sql = """
    INSERT INTO users (username, password, user_type)
    VALUES (?, ?, ?)
    """
    conn.execute(insert_sql, (username, password, user_type))
    conn.commit()

# Create a database connection
conn = create_connection()
# Create the appointments table if it doesn't exist
create_table(conn)
# Create the users table if it doesn't exist
create_users_table(conn)

# Page layout
st.set_page_config(page_title="Appointment Scheduler", page_icon="🏥", layout="wide")

# Title
st.title("Welcome to the Appointment Scheduler")

# Sidebar for user authentication and registration
option = st.sidebar.radio("Choose an option", ("Login", "Register"))

if option == "Login":
    # Login form
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        # Check if username and password are correct (dummy authentication for demonstration)
        # Query the users table for the provided credentials
        user_data = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        if user_data:
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid username or password.")
elif option == "Register":
    # Registration form
    st.sidebar.header("Register")
    new_username = st.sidebar.text_input("New Username")
    new_password = st.sidebar.text_input("New Password", type="password")
    user_type = st.sidebar.selectbox("User Type", ("Doctor", "Patient"))

    if st.sidebar.button("Register"):
        # Check if the username already exists in the database
        existing_user = conn.execute("SELECT * FROM users WHERE username = ?", (new_username,)).fetchone()
        if existing_user:
            st.error("Username already exists. Please choose a different one.")
        else:
            # Insert the new user into the database
            insert_user(conn, new_username, new_password, user_type)
            st.success("Registration successful! You can now login.")
