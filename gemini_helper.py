import streamlit as st
import google.generativeai as genai
from prompts import BUSINESS_ANALYST_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question):
    try:
        prompt = BUSINESS_ANALYST_PROMPT + "\n\nQuestion:\n" + question

        response = model.generate_content(prompt)

        text = response.text
        text = text.replace("```sql", "")
        text = text.replace("```", "")
        text = text.strip()

        return text

    except Exception as e:
        return f"Gemini Error: {str(e)}"