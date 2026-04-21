import streamlit as st
import numpy as np
from fer import FER
from PIL import Image
import plotly.express as px
import pandas as pd

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

detector = FER(mtcnn=True)

# ---------------- FUNCTION ----------------
def detect_emotion(image):
    img = np.array(image)
    result = detector.detect_emotions(img)

    if result:
        emotions = result[0]["emotions"]
        dominant = max(emotions, key=emotions.get)
        return dominant, emotions
    return "No face detected", {}

# ---------------- STUDENT ----------------
if mode == "👤 Student Capture":
    st.subheader("📸 Capture Your Emotion")

    img = st.camera_input("Take a photo")

    if img:
        image = Image.open(img)
        st.image(image)

        if st.button("Analyze"):
            emotion, emotions = detect_emotion(image)

            st.success(f"Detected Emotion: {emotion}")

            if emotions:
                df = pd.DataFrame({
                    "Emotion": list(emotions.keys()),
                    "Score": list(emotions.values())
                })

                fig = px.pie(df, names="Emotion", values="Score", title="Emotion Breakdown")
                st.plotly_chart(fig)

# ---------------- BATCH ----------------
elif mode == "📤 Batch Analysis":
    st.subheader("📤 Upload Images")

    files = st.file_uploader("Upload images", accept_multiple_files=True)

    if files:
        results = []

        for f in files:
            image = Image.open(f)
            emotion, _ = detect_emotion(image)
            results.append(emotion)

        df = pd.DataFrame(results, columns=["Emotion"])
        count_df = df["Emotion"].value_counts().reset_index()
        count_df.columns = ["Emotion", "Count"]

        fig = px.bar(count_df, x="Emotion", y="Count", title="Class Emotion")
        st.plotly_chart(fig)
