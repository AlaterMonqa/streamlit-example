import streamlit as st
import sqlite3
import pandas as pd

# Function to create database connection and tables if not exist
def create_database():
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    # Create Patients table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS Patients (
                    PatientID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Age INTEGER,
                    Gender TEXT
                )''')

    # Create Appointments table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS Appointments (
                    AppointmentID INTEGER PRIMARY KEY,
                    PatientID INTEGER,
                    Doctor TEXT,
                    Date TEXT,
                    FOREIGN KEY(PatientID) REFERENCES Patients(PatientID)
                )''')

    conn.commit()
    conn.close()

# Function to save patient details to the database
def save_patient_details(name, age, gender):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    c.execute('''INSERT INTO Patients (Name, Age, Gender) VALUES (?, ?, ?)''', (name, age, gender))

    conn.commit()
    conn.close()

# Function to save appointments to the database
def save_appointment(patient_id, doctor, date):
    conn = sqlite3.connect("hospital.db")
    c = conn.cursor()

    c.execute('''INSERT INTO Appointments (PatientID, Doctor, Date) VALUES (?, ?, ?)''', (patient_id, doctor, date))

    conn.commit()
    conn.close()

# Function to retrieve appointments from the database
def get_appointments():
    conn = sqlite3.connect("hospital.db")
    df = pd.read_sql_query("SELECT * FROM Appointments", conn)
    conn.close()
    return df

def main():
    create_database()  # Ensure database and tables are created

    st.title("Hospital Management System")

    # Sidebar for navigation
   # page = st.sidebar.radio("Navigation", ["Home", "Login", "Contact", "About"])

    if page == "Home":
        st.subheader("Welcome to Apollo Hospitals ")
        st.write("Use the sidebar to navigate.")

    elif page == "Login":
        st.subheader("Login")
        
        username = st.text_input("Usernamme")
        password = st.text_input("Enter your password:", type="password")
        if st.button("Sign up"):
             st.subheader("Create account")
             username = st.text_input("Usernamme")
             password = st.text_input("Enter your password:", type="password")
        if st.button("Save"):
            save_patient_details(name, age, gender)
            st.success("Patient details saved successfully.")

    elif page == "Make Appointment":
        st.subheader("Make Appointment")
        patient_id = st.number_input("Patient ID", min_value=1, step=1)
        doctor = st.text_input("Doctor's Name")
        date = st.date_input("Date")
        if st.button("Save"):
            save_appointment(patient_id, doctor, date)
            st.success("Appointment saved successfully.")

    elif page == "Show Appointments":
        st.subheader("Appointments")
        appointments_df = get_appointments()
        st.write(appointments_df)

if __name__ == "__main__":
    main()
