import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

st.set_page_config(
    page_title="Lesson Plan Generator",
    page_icon=":book:"
)

st.title("Children's Lesson Plan Generator")

st.write(
    """
    Upload an image (e.g., of lego blocks) and get a fun lesson plan with activities
    that a child can do with these objects!
    """
)

uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded image.', use_container_width=True)

    files = {
        "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
    }

    max_retries = 3
    attempt = 0
    success = False

    while attempt < max_retries and not success:
        with st.spinner(f'Generating lesson plan, attempt {attempt + 1}/{max_retries}...'):
            try:
                response = requests.post(f"http://localhost:{os.environ.get("FLASK_PORT")}/generate_plan", files=files)
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Generated Lesson Plan:")
                    st.write(data['lesson_plan'])
                    success = True
                else:
                    st.error("Error generating lesson plan: " + response.text)
                    attempt += 1
                    if attempt < max_retries:
                        st.info("Retrying...")
                        time.sleep(2)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                attempt += 1
                if attempt < max_retries:
                    st.info("Retrying...")
                    time.sleep(2)

    if not success:
        st.error("Failed to generate lesson plan after multiple attempts.")
