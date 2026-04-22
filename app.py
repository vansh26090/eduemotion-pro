import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EduEmotion Pro AI+", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.title("🔐 EduEmotion Pro Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "teacher" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧠 EduEmotion AI+ System")

menu = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "👤 Student Capture",
    "📤 Batch Analysis",
    "📊 Class Analytics",
    "📜 History"
])

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- FAKE AI ----------------
emotions = ["Happy", "Sad", "Angry", "Surprise", "Neutral"]

def detect_emotion():
    return random.choice(emotions)

def emotion_score(emotion):
    score_map = {
        "Happy": 100,
        "Surprise": 80,
        "Neutral": 60,
        "Sad": 30,
        "Angry": 20
    }
    return score_map.get(emotion, 50)

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.title("📊 AI Dashboard")

    total = len(st.session_state.history)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Scans", total)
    col2.metric("AI Mode", "Emotion Tracking")
    col3.metric("System Status", "Active")
    col4.metric("Accuracy", "Demo Mode")

    st.markdown("---")

    if total > 0:
        df = pd.DataFrame(st.session_state.history)

        chart = df["emotion"].value_counts().reset_index()
        chart.columns = ["Emotion", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Emotion Distribution")
            st.plotly_chart(px.pie(chart, names="Emotion", values="Count"))

        with col2:
            st.subheader("📈 Emotion Trend")
            st.plotly_chart(px.bar(chart, x="Emotion", y="Count"))

    else:
        st.info("Start capturing emotions to see analytics")

# ---------------- STUDENT CAPTURE ----------------
elif menu == "👤 Student Capture":
    st.title("📸 Student Emotion Capture")

    student_id = st.text_input("Enter Student Name / ID")

    img = st.camera_input("Capture Face")

    if img and student_id:
        image = Image.open(img)
        st.image(image)

        if st.button("Analyze"):
            emotion = detect_emotion()
            score = emotion_score(emotion)

            st.success(f"Emotion: {emotion}")
            st.info(f"Performance Score: {score}/100")

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "student": student_id,
                "emotion": emotion,
                "score": score
            })

# ---------------- BATCH ----------------
elif menu == "📤 Batch Analysis":
    st.title("📂 Batch Analysis")

    files = st.file_uploader(
        "Upload images",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if files:
        results = []

        for file in files:
            emotion = detect_emotion()
            score = emotion_score(emotion)

            results.append([emotion, score])

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "student": "Batch",
                "emotion": emotion,
                "score": score
            })

        df = pd.DataFrame(results, columns=["Emotion", "Score"])

        st.dataframe(df)

        st.plotly_chart(px.bar(df, x="Emotion", y="Score"))

        # Download report
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇ Download Report",
            csv,
            "emotion_report.csv",
            "text/csv"
        )

# ---------------- CLASS ANALYTICS ----------------
elif menu == "📊 Class Analytics":
    st.title("🏫 Class Performance Analytics")

    if len(st.session_state.history) == 0:
        st.warning("No data available")
    else:
        df = pd.DataFrame(st.session_state.history)

        avg_score = df["score"].mean()

        st.metric("Class Average Score", f"{avg_score:.2f}/100")

        st.subheader("Student-wise Performance")

        st.dataframe(df)

        st.plotly_chart(
            px.bar(df, x="student", y="score", color="emotion")
        )

# ---------------- HISTORY ----------------
elif menu == "📜 History":
    st.title("📜 Full History Log")

    if len(st.session_state.history) == 0:
        st.warning("No history yet")
    else:
        df = pd.DataFrame(st.session_state.history)

        st.dataframe(df)

        # Filter
        emotion_filter = st.selectbox("Filter by Emotion", ["All"] + emotions)

        if emotion_filter != "All":
            df = df[df["emotion"] == emotion_filter]

        st.dataframe(df)
