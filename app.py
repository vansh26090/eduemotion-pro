import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
from deepface import DeepFace
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Emotion AI Pro", layout="wide")

st.title("🧠 Emotion AI Pro (DeepFace CNN)")

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- REAL EMOTION FUNCTION ----------------
def detect_emotion(image_array):
    try:
        result = DeepFace.analyze(
            image_array,
            actions=['emotion'],
            enforce_detection=False
        )
        return result[0]['dominant_emotion']
    except:
        return "No Face Detected"

# ---------------- SIDEBAR MENU ----------------
menu = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "📸 Camera",
    "📤 Upload",
    "📊 Batch",
    "📜 History"
])

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Scans", len(st.session_state.history))
    col2.metric("AI Model", "DeepFace CNN")
    col3.metric("Status", "Active")

    st.info("Real AI Emotion Detection System")

# ---------------- CAMERA ----------------
elif menu == "📸 Camera":
    st.header("📸 Camera Emotion Detection")

    img = st.camera_input("Capture Face")

    if img:
        image = Image.open(img)
        st.image(image, caption="Captured Image")

        if st.button("Detect Emotion"):
            emotion = detect_emotion(np.array(image))

            st.success(f"Detected Emotion: {emotion}")

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "emotion": emotion,
                "type": "Camera"
            })

# ---------------- UPLOAD ----------------
elif menu == "📤 Upload":
    st.header("📤 Upload Image")

    file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])

    if file:
        image = Image.open(file)
        st.image(image)

        if st.button("Analyze"):
            emotion = detect_emotion(np.array(image))

            st.success(f"Detected Emotion: {emotion}")

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "emotion": emotion,
                "type": "Upload"
            })

# ---------------- BATCH ----------------
elif menu == "📊 Batch":
    st.header("📊 Batch Analysis")

    files = st.file_uploader(
        "Upload multiple images",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if files:
        emotions = []

        for file in files:
            image = Image.open(file)
            emotion = detect_emotion(np.array(image))
            emotions.append(emotion)

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "emotion": emotion,
                "type": "Batch"
            })

        df = pd.DataFrame(emotions, columns=["Emotion"])

        chart = df["Emotion"].value_counts().reset_index()
        chart.columns = ["Emotion", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(chart)

        with col2:
            fig = px.bar(chart, x="Emotion", y="Count", title="Emotion Distribution")
            st.plotly_chart(fig)

# ---------------- HISTORY ----------------
elif menu == "📜 History":
    st.header("📜 Detection History")

    if len(st.session_state.history) == 0:
        st.warning("No history yet")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
