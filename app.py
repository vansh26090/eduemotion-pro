import streamlit as st
import numpy as np
from PIL import Image
from deepface import DeepFace
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Emotion AI Pro", layout="wide")

st.title("🧠 Emotion AI Pro")

# ---------------- IMAGE EMOTION ----------------
st.subheader("📤 Upload Image Emotion Detection")

def detect_emotion(img):
    try:
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "No Face"

img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if img_file:
    image = Image.open(img_file)
    st.image(image)

    if st.button("Analyze Image"):
        emotion = detect_emotion(np.array(image))
        st.success(f"Detected Emotion: {emotion}")

# ---------------- BATCH ANALYSIS ----------------
st.subheader("📊 Batch Emotion Analysis")

files = st.file_uploader(
    "Upload Multiple Images",
    type=["jpg", "png"],
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
