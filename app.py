import streamlit as st
import numpy as np
from PIL import Image
import plotly.express as px
import pandas as pd
import random

st.set_page_config(page_title="EduEmotion Pro", layout="wide")

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "teacher" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong credentials")

    st.stop()

# ---------------- MAIN ----------------
st.sidebar.title("🧠 EduEmotion Pro")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

mode = st.sidebar.selectbox("Choose Feature", [
    "👤 Student Capture",
    "📤 Batch Analysis"
])

st.title("🧠 EduEmotion Pro Dashboard")

# ---------------- FAKE AI (safe cloud version) ----------------
emotions_list = ["Happy", "Sad", "Angry", "Surprise", "Neutral"]

def detect_emotion():
    return random.choice(emotions_list)

# ---------------- STUDENT ----------------
if mode == "👤 Student Capture":
    st.subheader("📸 Capture Your Emotion")

    img = st.camera_input("Take a photo")

    if img:
        image = Image.open(img)
        st.image(image)

        if st.button("Analyze"):
            emotion = detect_emotion()
            st.success(f"Detected Emotion: {emotion}")

# ---------------- BATCH ----------------
elif mode == "📤 Batch Analysis":
    st.subheader("📤 Upload Images")

    files = st.file_uploader("Upload images", accept_multiple_files=True)

    if files:
        results = []

        for _ in files:
            results.append(detect_emotion())

        df = pd.DataFrame(results, columns=["Emotion"])
        count_df = df["Emotion"].value_counts().reset_index()
        count_df.columns = ["Emotion", "Count"]

        fig = px.bar(count_df, x="Emotion", y="Count", title="Class Emotion")
        st.plotly_chart(fig)
