import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EduEmotion Pro", layout="wide")

# ================= LOGIN =================
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
            st.error("Wrong username or password")

    st.stop()

# ================= MAIN APP =================
st.sidebar.title("🧠 EduEmotion Pro")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🧠 EduEmotion Pro Dashboard")

mode = st.sidebar.selectbox("Choose Feature", [
    "👤 Student View",
    "📤 Teacher Batch Analysis"
])

# ================= STUDENT VIEW =================
if mode == "👤 Student View":
    st.subheader("📸 Capture Emotion")

    img = st.camera_input("Take a photo")

    if img is not None:
        st.image(img)
        st.success("✅ Image captured (emotion detection can be added later)")

# ================= TEACHER VIEW =================
elif mode == "📤 Teacher Batch Analysis":
    st.subheader("📤 Upload Student Images")

    files = st.file_uploader("Upload images", accept_multiple_files=True)

    if files:
        st.success(f"{len(files)} files uploaded")

        # Dummy data (safe for deployment)
        data = {
            "Emotion": ["Happy", "Sad", "Neutral"],
            "Count": [10, 5, 8]
        }

        df = pd.DataFrame(data)

        fig = px.bar(df, x="Emotion", y="Count", title="Class Emotion Overview")
        st.plotly_chart(fig)