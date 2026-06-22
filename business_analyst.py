from gemini_helper import ask_gemini


def generate_summary(df):

    prompt = f"""
You are a Senior Business Analyst.

Analyze this table:

{df.head(10)}

Provide:

Observation:
Business Impact:
Recommendation:

Keep the answer concise.
"""

    return ask_gemini(prompt)