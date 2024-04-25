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

    c.execute('''INSERT INTO
