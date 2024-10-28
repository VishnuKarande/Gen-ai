import streamlit as st
import pdfplumber
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def initialize_llm(model_type):
    return Groq(model=model_type, api_key=api_key)

def summarize_text(llm, text, summary_type):
    if summary_type == "Long Summary":
        prompt = f"Give a summary of the text: {text}"
    elif summary_type == "Short Summary":
        prompt = f"Give a 100 word summary of the text: {text}"
    elif summary_type == "Creative Summary":
        prompt = f"Give a creative summary of the text: {text}"
    elif summary_type == "Bullet Point Summary":
        prompt = f"Give a summary of the text in 3 bullet points: {text}"

    response = llm.complete(prompt)
    return response

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

st.title("📄 Text Summarizer 🤖")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
else:
    extracted_text = ""


text_area = st.text_area("Extracted text from PDF", value=extracted_text, height=300, disabled=True)


summary_type = st.selectbox(
    "Select Summary Type",
    ("Long Summary", "Short Summary", "Creative Summary", "Bullet Point Summary")
)


model_type = st.selectbox(
    "Select Model Type",
    ("Gemma-7b-It", "llama3-70b-8192", "Mixtral-8x7b-32768")
)


llm = initialize_llm(model_type)


if st.button("Generate Summary"):
    if extracted_text:
        summary = summarize_text(llm, extracted_text, summary_type)
        st.write(f"### {summary_type} using {model_type}")
        st.write(summary)
    else:
        st.write("Please upload a PDF to summarize.")

# Add a footer
st.markdown("---")
st.markdown("Made by Vishnu")