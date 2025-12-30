import streamlit as st
from PIL import Image
import pytesseract
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Student Tutor",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Student Tutor")
st.write("Ask questions by typing or uploading a photo")

# ---------------- API KEY CHECK ----------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API key missing")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- INPUT METHOD ----------------
mode = st.radio(
    "Choose input method",
    ["✍️ Type Question", "📷 Upload Image"]
)

question_text = ""

if mode == "✍️ Type Question":
    question_text = st.text_area(
        "Type your question",
        placeholder="Example: Solve 2x + 5 = 15"
    )

else:
    uploaded_file = st.file_uploader(
        "Upload homework image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Reading image..."):
            question_text = pytesseract.image_to_string(image)

        question_text = st.text_area(
            "Extracted text (you can edit it)",
            value=question_text,
            height=150
        )

# ---------------- STUDENT LEVEL ----------------
level = st.selectbox("Student level", ["School", "University"])

# ---------------- ANSWER BUTTON ----------------
if st.button("✅ Get Answer"):
    if not question_text.strip():
        st.warning("⚠️ Please enter a question")
    else:
        with st.spinner("AI is thinking..."):
            try:
                prompt = f"""
You are an AI tutor.

Student level: {level}

Rules:
- Use very simple language
- Be clear and short
- Explain step by step if needed

Question:
{question_text}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You help students understand homework."},
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message.content

                st.success("📘 Answer")
                st.write(answer)

            except Exception as e:
                st.error("❌ AI error")
                st.code(str(e))

st.markdown("---")
st.caption("AI Student Tutor • Streamlit")
