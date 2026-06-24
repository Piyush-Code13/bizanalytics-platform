from gemini_helper import ask_gemini
from sql_prompt import SYSTEM_PROMPT

def generate_sql(question):

    prompt = f"""
{SYSTEM_PROMPT}

User Question:

{question}

IMPORTANT:

Return ONLY SQL.
Do not write:
Observation
Possible Reasons
Business Impact
Recommendation

Start directly with SELECT.
"""

    sql_query = ask_gemini(prompt)

    print("Generated SQL:")
    print(sql_query)

    if "SELECT" in sql_query.upper():
        sql_query = sql_query[sql_query.upper().find("SELECT"):]

    return sql_query