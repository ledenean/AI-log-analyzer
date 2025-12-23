import streamlit as st
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Log Analyzer", page_icon="🌸", layout="centered")
st.title("AI Log Analyzer")
st.markdown("Upload a log file to analyze it with OpenAI's API.")

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

uploadedFile = st.file_uploader("Choose a log file", type=["txt"])

analyze = st.button("Analyze Log")

def extractTextFromFile(file):
    text = file.read().decode("utf-8")
    return text

if analyze:
    try:
        fileContent = extractTextFromFile(uploadedFile)

        if not fileContent.strip():
            st.error("The uploaded file is empty.")
            st.stop()

        prompt = f"""Analyze the following log file and provide a summary of the key events, patterns, and errors. 
            Summarize the root cause of the errors and suggest a solution. 
            Assess customer impact and provide a customer-facing summary to accelerate incident resolution.
            Log file: {fileContent}"""

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a customer success engineer with years of experience in troubleshooting and resolving technical issues."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")
        st.stop()