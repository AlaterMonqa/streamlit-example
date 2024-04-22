import altair as alt
import numpy as np
import pandas as pd
import streamlit as st



# Page layout
st.set_page_config(page_title="Appointment Scheduler", page_icon="🏥", layout="wide")

# Title
st.title("Welcome to the Appointment Scheduler")

# Sidebar
st.sidebar.header("Patient Details")
patient_name = st.sidebar.text_input("Patient Name")
patient_age = st.sidebar.number_input("Patient Age", min_value=0, max_value=150, step=1)
patient_gender = st.sidebar.selectbox("Patient Gender", ["Male", "Female", "Other"])

# Date and time picker
appointment_date = st.sidebar.date_input("Appointment Date")
appointment_time = st.sidebar.time_input("Appointment Time")

# Button to schedule appointment
if st.sidebar.button("Schedule Appointment"):
    # Create a DataFrame to store appointment details
    appointments_df = pd.DataFrame({
        "Patient Name": [patient_name],
        "Patient Age": [patient_age],
        "Patient Gender": [patient_gender],
        "Appointment Date": [appointment_date],
        "Appointment Time": [appointment_time]
    })

    # Append new appointment to existing appointments (if any)
    if "Appointments" in st.session_state:
        st.session_state.Appointments = st.session_state.Appointments.append(appointments_df, ignore_index=True)
    else:
        st.session_state.Appointments = appointments_df

    # Confirmation message
    st.success("Appointment scheduled successfully!")

# Display scheduled appointments
st.header("Scheduled Appointments")
if "Appointments" in st.session_state:
    st.write(st.session_state.Appointments)
else:
    st.info("No appointments scheduled yet.")
