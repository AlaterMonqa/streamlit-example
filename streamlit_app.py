import altair as alt
import numpy as np
import pandas as pd
import streamlit as st





import sqlite3
from datetime import datetime, date

# Connect to SQLite database
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
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    patient_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    issues TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY,
                    patient_name TEXT,
                    doctor_name TEXT,
                    appointment_date TEXT,
                    appointment_time TEXT
                 )''')

# Streamlit UI
st.title("Hospital Management System")
# Sidebar
option = st.sidebar.selectbox("Menu", ["Login", "Create Account"])
# Function to add a new user
def add_user(username, password, user_type):
    c.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", (username, password, user_type))
    conn.commit()

# Function to add a new patient
def add_patient(username, patient_name, age, gender, issues):
    c.execute("INSERT INTO patients (username, patient_name, age, gender, issues) VALUES (?, ?, ?, ?, ?)",
              (username, patient_name, age, gender, issues))
    conn.commit()

# Function to authenticate user
def authenticate(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone()

# Function to get patient details
def get_patient_details(username):
    c.execute("SELECT * FROM patients WHERE username = ?", (username,))
    return c.fetchone()

# Function to schedule appointment
def schedule_appointment(patient_name, doctor_name, appointment_date, appointment_time):
    c.execute("INSERT INTO appointments (patient_name, doctor_name, appointment_date, appointment_time) VALUES (?, ?, ?, ?)",
              (patient_name, doctor_name, appointment_date, appointment_time))
    conn.commit()

# Create tables if they don't exist
create_tables()
#Main page
def PD_Page():
      st.header("Please fill the patient details")
      patient_name = st.text_input("Enter patient name")
      age = st.number_input("Enter age", min_value=1, max_value=150)
      gender = st.radio("Select gender", ("Male", "Female", "Other"))
      issues = st.text_area("Enter patient issues")
      add_patient(new_username, patient_name, age, gender, issues)
      st.success("Patient details added successfully!")

#Patient dashboard
def  Patient_Dashboard():
 st.header("Patient details")
 patient_details = get_patient_details(username)
 st.write("Username:", username)
 st.write("Patient Name:", patient_details[2])  # 2nd column is patient_name
# Display other patient details here
#Doctor dashboard
def Dr():
   st.header("Doctor Dashboard")

    



# Login Page
if option == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = authenticate(username, password)
        if user:
            st.success("Login successful!")
            user_type = user[3]  # 3rd column is user_type
            if user_type == 'patient':
                Patient_Dashboard()
                
            else:
               Dr()
                # Display doctor dashboard
        else:
            st.error("Invalid username or password. Please try again.")

# New Account Creation
elif option == "Create Account":
    st.header("Create Account")
    new_username = st.text_input("Enter username")
    new_password = st.text_input("Enter password", type="password")
    user_type = st.radio("Select account type", ("Patient", "Doctor"))
    create_account_button = st.button("Create Account")

    if create_account_button:
        add_user(new_username, new_password, user_type)
        st.success("Account created successfully!")
        st.session_state.runpage = PD_Page
        st.session_state.runpage
        st.rerun()
        st.experimental_rerun()
       # if user_type == "Patient":
          
# Additional functionalities like appointment scheduling can be added here
