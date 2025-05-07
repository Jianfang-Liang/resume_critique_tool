import streamlit as st
import fitz
from openai import OpenAI
import os
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(),filetype="pdf")
    text =""
    for page in doc:
        text += page.get_text()
    return text 

def get_resume_feedback(resume_text):
    prompt = f"You are an expert career advisor. Please provide constructive, detailed feedback on this resume:\n\n{resume_text}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful and professional resume critique assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


st.title("AI-Powered Resume Critique Tool")

st.write("Upload your resume and get feedback powered by GPT-4!")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    if st.button("Get GPT Feedback"):
        with st.spinner("Analyzing your resume..."):
            feedback = get_resume_feedback(resume_text)
            st.subheader("AI Feedback")
            st.write(feedback)
