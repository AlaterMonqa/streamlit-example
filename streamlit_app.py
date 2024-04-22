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

# Sidebar
st.sidebar.header("Patient Details")
patient_name = st.sidebar.text_input("Patient Name")
patient_age = st.sidebar.number_input("Patient Age", min_value=0, max_value=150, step=1)
patient_gender = st.sidebar.selectbox("Patient Gender", ["Male", "Female", "Other"])
patient_issues = st.sidebar.text_area("Patient Issues")

# Date and time picker
appointment_date = st.sidebar.date_input("Appointment Date")
appointment_time = st.sidebar.time_input("Appointment Time")

# Button to schedule appointment
if st.sidebar.button("Schedule Appointment"):
    # Convert time to string
    appointment_time_str = appointment_time.strftime("%H:%M")
    # Insert the appointment into the database
    appointment_data = (patient_name, patient_age, patient_gender, patient_issues, str(appointment_date), appointment_time_str)
    insert_appointment(conn, appointment_data)
    # Confirmation message
    st.success("Appointment scheduled successfully!")

# Display scheduled appointments
st.header("Scheduled Appointments")
appointments_df = get_all_appointments(conn)
if not appointments_df.empty:
    st.write(appointments_df)
else:
    st.info("No appointments scheduled yet.")
