import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load model and encoders (replace with your actual objects if saved)
# Or define again here if everything is in one script
le_gender = LabelEncoder().fit(['Male', 'Female'])  # Ensure this matches your training
le_status = LabelEncoder().fit(['Stable', 'Observation', 'Critical'])  # Adjust if needed
scaler = StandardScaler()
model = RandomForestClassifier()

# Dummy fit for demonstration, REPLACE with loading from pickle or real training
X_dummy = pd.DataFrame({
    'age': [60, 70],
    'gender': le_gender.transform(['Male', 'Female']),
    'temp': [37.5, 39.0],
    'heartRate': [95, 110],
    'SpO2': [92, 85]
})
scaler.fit(X_dummy)
model.fit(scaler.transform(X_dummy), le_status.transform(['Stable', 'Critical']))

# Streamlit UI
st.set_page_config(page_title="Patient Health Status Predictor", layout="centered")
st.title("🧑‍⚕️ Patient Health Status Predictor")
st.markdown("Enter patient details below to predict their current health status.")

# Input fields
age = st.number_input("Age", min_value=0, max_value=120, value=65)
gender = st.selectbox("Gender", ["Male", "Female"])
temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0)
heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=180, value=90)
spo2 = st.number_input("SpO2 (%)", min_value=70, max_value=100, value=95)

if st.button("Predict Status"):
    input_data = pd.DataFrame([{
        'age': age,
        'gender': le_gender.transform([gender])[0],
        'temp': temp,
        'heartRate': heart_rate,
        'SpO2': spo2
    }])

    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)
    status = le_status.inverse_transform(prediction)[0]

    # Show result with style
    status_color = {
        'Critical': '🔴',
        'Observation': '🟡',
        'Stable': '🟢'
    }.get(status, '⚪')

    st.success(f"### {status_color} Predicted Status: **{status}**")

    st.markdown("___")
    st.markdown("📝 *Note: This prediction is based on ML model estimations.*")