import google.generativeai as genai
from prompts import BUSINESS_ANALYST_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def ask_gemini(question):

    prompt = BUSINESS_ANALYST_PROMPT + "\n\nQuestion:\n" + question

    response = model.generate_content(prompt)

    text = response.text

    text = text.replace("```sql", "")
    text = text.replace("```", "")
    text = text.strip()

    return text