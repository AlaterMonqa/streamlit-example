import altair as alt
import numpy as np
import pandas as pd
import streamlit as st





import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('hospital.db')
c = conn.cursor()

# Function to create tables
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    user_type TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY,
                    patient_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    issues TEXT,
                    appointment_date TEXT,
                    appointment_time TEXT
                 )''')

# Function to add a new user
def add_user(username, password, user_type):
    c.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", (username, password, user_type))
    conn.commit()

# Function to schedule appointment
def schedule_appointment(patient_name, age, gender, issues, appointment_date, appointment_time):
    c.execute("INSERT INTO appointments (patient_name, age, gender, issues, appointment_date, appointment_time) VALUES (?, ?, ?, ?, ?, ?)",
              (patient_name, age, gender, issues, appointment_date, appointment_time))
    conn.commit()

# Function to authenticate user
def authenticate(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone()

# Function to get patient details
def get_patient_details(username):
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    return c.fetchone()

# Create tables if they don't exist
create_tables()

# Streamlit UI
st.title("Hospital Management System")

# Login section
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    user = authenticate(username, password)
    if user:
        st.success("Login successful!")
        user_type = user[3]  # 3rd column is user_type
        if user_type == 'patient':
            st.subheader("Patient Details")
            patient_details = get_patient_details(username)
            st.write("Username:", username)
            st.write("Patient Name:", patient_details[1])  # 1st column is username
            # Display other patient details here
        else:
            st.subheader("Doctor Dashboard")
            # Display doctor dashboard
    else:
        st.error("Invalid username or password. Please try again.")
