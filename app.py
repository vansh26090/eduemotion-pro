import streamlit as st
import numpy as np
from PIL import Image
from deepface import DeepFace
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Emotion AI Pro", layout="wide")

st.title("🧠 Emotion AI Pro")

# ---------------- FUNCTION ----------------
def detect_emotion(img):
    try:
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "No Face Detected"

# ---------------- CAMERA ----------------
st.subheader("📸 Camera Emotion Detection")

camera_image = st.camera_input("Take a picture")

if camera_image is not None:
    image = Image.open(camera_image)
    st.image(image, caption="Captured Image")

    emotion = detect_emotion(np.array(image))
    st.success(f"Detected Emotion: {emotion}")

# ---------------- IMAGE UPLOAD ----------------
st.subheader("📤 Upload Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Analyze Image"):
        emotion = detect_emotion(np.array(image))
        st.success(f"Detected Emotion: {emotion}")

# ---------------- BATCH ANALYSIS ----------------
st.subheader("📊 Batch Analysis")

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

    df = pd.DataFrame(emotions, columns=["Emotion"])

    chart = df["Emotion"].value_counts().reset_index()
    chart.columns = ["Emotion", "Count"]

    fig = px.bar(chart, x="Emotion", y="Count", title="Emotion Distribution")
    st.plotly_chart(fig)
