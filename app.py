import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EduEmotion Pro AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🔐 EduEmotion Pro Login")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Username")

    with col2:
        password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "teacher" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 EduEmotion AI Dashboard")

menu = st.sidebar.radio("Navigation", [
    "🏠 Home Dashboard",
    "👤 Student Emotion Capture",
    "📊 Batch Analysis",
    "📜 History Log"
])

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- FAKE AI (replace later with real model) ----------------
emotions = ["Happy", "Sad", "Angry", "Surprise", "Neutral"]

def detect_emotion():
    return random.choice(emotions)

# ---------------- HOME DASHBOARD ----------------
if menu == "🏠 Home Dashboard":
    st.title("📊 AI Emotion Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sessions", len(st.session_state.history))
    col2.metric("Model Accuracy", "85% (Demo)")
    col3.metric("Active Mode", "Real-Time AI")

    st.markdown("---")

    st.info("Welcome to EduEmotion Pro — AI powered student emotion tracking system")

# ---------------- STUDENT CAPTURE ----------------
elif menu == "👤 Student Emotion Capture":
    st.title("📸 Live Emotion Capture")

    img = st.camera_input("Capture Student Emotion")

    if img:
        image = Image.open(img)
        st.image(image, caption="Captured Image")

        if st.button("Analyze Emotion"):
            emotion = detect_emotion()

            st.success(f"Detected Emotion: {emotion}")

            # save history
            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "emotion": emotion
            })

# ---------------- BATCH ANALYSIS ----------------
elif menu == "📊 Batch Analysis":
    st.title("📂 Batch Emotion Analysis")

    files = st.file_uploader(
        "Upload multiple images",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if files:
        results = []

        for file in files:
            emotion = detect_emotion()
            results.append(emotion)

        df = pd.DataFrame(results, columns=["Emotion"])

        count = df["Emotion"].value_counts().reset_index()
        count.columns = ["Emotion", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(count)

        with col2:
            fig = px.bar(count, x="Emotion", y="Count", title="Emotion Distribution")
            st.plotly_chart(fig)

# ---------------- HISTORY ----------------
elif menu == "📜 History Log":
    st.title("🧾 Emotion Detection History")

    if len(st.session_state.history) == 0:
        st.warning("No history yet")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
