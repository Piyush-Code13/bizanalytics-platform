from gemini_helper import ask_gemini


def generate_insights(question, df):
    """
    Generates a business-analyst style insight for a query result using Gemini.

    Computes summary statistics locally (top/bottom performer, average, total,
    concentration share) and passes them to Gemini as grounding context, so the
    model explains real numbers from this result rather than inventing them.
    """
    first_col = df.columns[0]
    second_col = df.columns[1]

    top_item = df.iloc[0][first_col]
    top_value = df.iloc[0][second_col]
    bottom_item = df.iloc[-1][first_col]
    bottom_value = df.iloc[-1][second_col]

    average_value = df[second_col].mean()
    total_value = df[second_col].sum()
    share = (top_value / total_value) * 100 if total_value else 0

    if share > 50:
        concentration_risk = "High"
    elif share > 30:
        concentration_risk = "Medium"
    else:
        concentration_risk = "Low"

    prompt = f"""You are a senior business analyst reviewing a query result
for an e-commerce analytics platform.

Business question asked: "{question}"

Computed data summary:
- Top performer: {top_item} ({top_value:,.2f})
- Lowest performer: {bottom_item} ({bottom_value:,.2f})
- Average value across all rows: {average_value:,.2f}
- Total value across all rows: {total_value:,.2f}
- Top performer's share of total: {share:.2f}% (concentration risk: {concentration_risk})

Using ONLY the numbers above, write a concise business insight with these
sections, each 1-3 sentences:

Observation: What the data shows.
Business Impact: Why this matters for the business.
Risk: Any concentration, dependency, or downside risk implied by the numbers.
Recommendation: One clear, actionable next step.

Keep the whole response under 150 words. Do not invent numbers not given above.
"""

    return ask_gemini(prompt)