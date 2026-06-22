from gemini_helper import ask_gemini


def generate_executive_summary(question, df):

    prompt = f"""
You are a Senior Business Analyst.

Question:
{question}

Data:
{df.head(10).to_string()}

Act like a Senior Business Analyst preparing insights for executives.

Provide:

### Observation
Describe the main patterns and trends.

### Possible Reasons
Explain why these results may have occurred.

### Business Impact
Explain how these findings affect business performance.

### Recommendations
Provide 3-4 actionable recommendations.

Requirements:
- Use professional business language.
- Avoid generic statements.
- Mention important numbers from the data whenever possible.
- Keep the response concise and executive-friendly.
"""

    return ask_gemini(prompt)