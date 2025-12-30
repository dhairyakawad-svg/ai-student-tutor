import streamlit as st
from PIL import Image
import pytesseract
import openai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Student Tutor",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Student Tutor")
st.write("Ask questions by typing or uploading a photo")

# ---------------- API KEY SAFE HANDLING ----------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key not found.")
    st.info("👉 Go to Streamlit Cloud → Manage App → Settings → Secrets and add your API key.")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------- INPUT METHOD ----------------
mode = st.radio(
    "Choose how you want to ask:",
    ["✍️ Type Question", "📷 Upload Image"]
)

question_text = ""

if mode == "✍️ Type Question":
    question_text = st.text_area(
        "Type your question here",
        placeholder="Example: Solve 2x + 5 = 15"
    )

elif mode == "📷 Upload Image":
    uploaded_file = st.file_uploader(
        "Upload homework image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Reading text from image..."):
            question_text = pytesseract.image_to_string(image)

        st.text_area(
            "Extracted Text (editable)",
            value=question_text,
            height=150
        )

# ---------------- STUDENT LEVEL ----------------
level = st.selectbox(
    "Select student level",
    ["School", "University"]
)

# ---------------- GET ANSWER ----------------
if st.button("✅ Get Answer"):
    if not question_text.strip():
        st.warning("⚠️ Please enter a question or upload an image.")
    else:
        with st.spinner("AI is thinking..."):
            try:
                prompt = f"""
You are an AI tutor.
Student level: {level}

Instructions:
- Use very simple language
- Be clear and direct
- If math/science, explain step by step
- Keep it student-friendly

Question:
{question_text}
"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI tutor for students."},
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message.content

                st.success("📘 Answer")
                st.write(answer)

            except Exception as e:
                st.error("❌ Something went wrong while generating the answer.")
                st.exception(e)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & OpenAI")
