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

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LOGIN ----------------
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
st.sidebar.title("🧠 EduEmotion AI")

menu = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "👤 Student Capture",
    "📤 Batch Analysis",
    "📜 History"
])

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- FAKE AI (replace later with DeepFace if needed) ----------------
emotions = ["Happy", "Sad", "Angry", "Surprise", "Neutral"]

def detect_emotion():
    return random.choice(emotions)

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.title("📊 AI Emotion Dashboard")

    total = len(st.session_state.history)

    emotion_count = {}
    for h in st.session_state.history:
        e = h["emotion"]
        emotion_count[e] = emotion_count.get(e, 0) + 1

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Scans", total)
    col2.metric("Happy", emotion_count.get("Happy", 0))
    col3.metric("Sad", emotion_count.get("Sad", 0))
    col4.metric("Neutral", emotion_count.get("Neutral", 0))

    st.markdown("---")

    if total > 0:
        df = pd.DataFrame(st.session_state.history)

        chart = df["emotion"].value_counts().reset_index()
        chart.columns = ["Emotion", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Emotion Pie Chart")
            fig = px.pie(chart, names="Emotion", values="Count")
            st.plotly_chart(fig)

        with col2:
            st.subheader("📈 Emotion Bar Chart")
            fig2 = px.bar(chart, x="Emotion", y="Count")
            st.plotly_chart(fig2)

    else:
        st.info("No data yet. Start capturing emotions.")

    st.markdown("---")

    st.subheader("🕒 Recent Activity")

    if total > 0:
        for h in st.session_state.history[-5:][::-1]:
            st.write(f"🧠 {h['time']} → {h['emotion']}")
    else:
        st.warning("No activity yet")

# ---------------- STUDENT CAPTURE ----------------
elif menu == "👤 Student Capture":
    st.title("📸 Student Emotion Capture")

    img = st.camera_input("Take a picture")

    if img:
        image = Image.open(img)
        st.image(image, caption="Captured Image")

        if st.button("Analyze Emotion"):
            emotion = detect_emotion()

            st.success(f"Detected Emotion: {emotion}")

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "emotion": emotion
            })

# ---------------- BATCH ----------------
elif menu == "📤 Batch Analysis":
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

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "emotion": emotion
            })

        df = pd.DataFrame(results, columns=["Emotion"])

        chart = df["Emotion"].value_counts().reset_index()
        chart.columns = ["Emotion", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(chart)

        with col2:
            fig = px.bar(chart, x="Emotion", y="Count")
            st.plotly_chart(fig)

# ---------------- HISTORY ----------------
elif menu == "📜 History":
    st.title("📜 Emotion History Log")

    if len(st.session_state.history) == 0:
        st.warning("No history yet")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
