import streamlit as st
from PIL import Image
import pytesseract
import openai

# Page config
st.set_page_config(page_title="AI Student Tutor", layout="centered")

st.title("📚 AI Student Tutor")
st.write("Ask questions by typing or uploading a photo")

# OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Input mode
mode = st.radio("Choose input method:", ["Text", "Image"])

question = ""

if mode == "Text":
    question = st.text_area("Type your question here")

else:
    uploaded_file = st.file_uploader("Upload homework image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        question = pytesseract.image_to_string(image)

level = st.selectbox("Select student level:", ["School", "University"])

if st.button("Get Answer") and question:
    with st.spinner("Thinking..."):
        prompt = f"""
        You are an AI tutor.
        Student level: {level}
        Question: {question}

        Give a simple, clear, student-friendly answer.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("Answer")
        st.write(response.choices[0].message.content)
