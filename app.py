import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import requests

# Set page layout
st.set_page_config(page_title="Patient Monitoring", layout="wide")

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# Load JSON data
@st.cache_data(ttl=5)
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1G_YPaiBUsmjteaXvADJyr0t3g46OoF-K"
    response = requests.get(url)
    
    # Check what we're getting back
    if "application/json" not in response.headers.get("Content-Type", ""):
        st.error("❌ The file did not return valid JSON. Google Drive may be returning HTML or a warning page.")
        st.text(response.text[:500])  # Show part of the HTML/response
        st.stop()

    data = response.json()
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df = load_data()

# Header
st.title("🩺 Real-Time Patient Monitoring Dashboard")

# Select Patient
patient_id = st.selectbox("Select Patient ID", df["patientId"].unique())
patient_data = df[df["patientId"] == patient_id].sort_values("timestamp")

# Most recent entry
latest = patient_data.iloc[-1]

# Patient Info
st.markdown("## 👤 Patient Details")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Name", latest["name"])
col2.metric("Age", latest["age"])
col3.metric("Gender", latest["gender"])
col4.metric("Doctor", latest["assignedDoctor"])

# Vital Stats
st.markdown("## 📊 Current Vitals")
v1, v2, v3, v4 = st.columns(4)
v1.metric("🌡️ Temp (°C)", latest["temp (°C)"])
v2.metric("❤️ Heart Rate", latest["heartRate"])
v3.metric("🫁 SpO2 (%)", latest["SpO2 (%)"])
v4.metric("📋 Status", latest["status"])

# Time Series Plots
st.markdown("### 📈 Vital Sign Trends (24h)")

fig1 = px.line(patient_data, x="timestamp", y="temp (°C)", title="Temperature Over Time")
fig2 = px.line(patient_data, x="timestamp", y="heartRate", title="Heart Rate Over Time")
fig3 = px.line(patient_data, x="timestamp", y="SpO2 (%)", title="SpO2 Over Time")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("⏱️ Dashboard auto-refreshes every 5 seconds")
