import streamlit as st
import numpy as np
from PIL import Image
import cv2
from deepface import DeepFace
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Emotion AI Pro", layout="wide")

st.title("🧠 Emotion AI Pro (Real Detection)")

# ---------------- CAMERA MODE ----------------
st.subheader("📸 Live Emotion Detection")

run = st.checkbox("Start Webcam")

frame_placeholder = st.image([])

camera = cv2.VideoCapture(0)

def detect_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "No Face"

if run:
    while True:
        ret, frame = camera.read()
        if not ret:
            st.error("Camera not working")
            break

        emotion = detect_emotion(frame)

        cv2.putText(frame, emotion, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame)

camera.release()

# ---------------- IMAGE UPLOAD ----------------
st.subheader("📤 Upload Image Emotion Detection")

img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if img_file:
    image = Image.open(img_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Analyze Image"):
        result = DeepFace.analyze(np.array(image), actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        st.success(f"Detected Emotion: {emotion}")

# ---------------- BATCH ANALYSIS ----------------
st.subheader("📊 Batch Emotion Analysis")

files = st.file_uploader("Upload Multiple Images", type=["jpg", "png"], accept_multiple_files=True)

if files:
    emotions = []

    for file in files:
        image = Image.open(file)
        result = DeepFace.analyze(np.array(image), actions=['emotion'], enforce_detection=False)
        emotions.append(result[0]['dominant_emotion'])

    df = pd.DataFrame(emotions, columns=["Emotion"])

    chart = df["Emotion"].value_counts().reset_index()
    chart.columns = ["Emotion", "Count"]

    fig = px.bar(chart, x="Emotion", y="Count", title="Emotion Distribution")
    st.plotly_chart(fig)
