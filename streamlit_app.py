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

# Create a database connection
conn = create_connection()
# Create the appointments table if it doesn't exist
create_table(conn)

# Page layout
st.set_page_config(page_title="Appointment Scheduler", page_icon="🏥", layout="wide")

# Title
st.title("Welcome to the Appointment Scheduler")

# Sidebar for user authentication
user_type = st.sidebar.radio("Login as", ("Doctor", "Patient"))

# Login form based on user type
if user_type == "Doctor":
    st.sidebar.header("Doctor Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        # Check if username and password are correct (dummy authentication for demonstration)
        if username == "doctor" and password == "password":
            st.success("Doctor login successful!")
        else:
            st.error("Invalid username or password.")
elif user_type == "Patient":
    st.sidebar.header("Patient Login")
    patient_id = st.sidebar.text_input("Patient ID")

    if st.sidebar.button("Login"):
        # Check if patient ID exists in the database (dummy authentication for demonstration)
        if patient_id:
            st.success("Patient login successful!")
        else:
            st.error("Invalid patient ID.")

# Display scheduled appointments
st.header("Scheduled Appointments")
appointments_df = get_all_appointments(conn)
if not appointments_df.empty:
    st.write(appointments_df)
else:
    st.info("No appointments scheduled yet.")
