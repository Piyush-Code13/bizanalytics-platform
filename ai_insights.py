from gemini_helper import ask_gemini
def generate_sales_insight(revenue_df):
        """Revenue trend insight using existing AI connection."""
        summary = revenue_df.describe().to_string()
        prompt = f"""As a senior business analyst, analyze this revenue
        data summary and give: Observation, Possible Reason,
        Business Impact, Recommendation.
        Data: {summary}"""
        return ask_gemini(prompt)
def generate_customer_insight(customer_df):
    """Customer distribution and concentration insight."""
    top_states = customer_df.groupby('state').size().nlargest(5)
    prompt = f"""Analyze this customer distribution by state and
    explain market concentration risk: {top_states.to_dict()}"""
    return ask_gemini(prompt)
def generate_category_insight(category_df):
    """Product category performance insight."""
    prompt = f"""Identify the best and worst performing product
    categories from this data and explain why:
    {category_df.to_string()}"""
    return ask_gemini(prompt)
def generate_risk_analysis(revenue_df):
    """Flag revenue drops or anomalies."""
    pct_change = revenue_df['revenue'].pct_change()
    risky_periods = pct_change[pct_change < -0.15]
    prompt = f"""These periods show revenue drops over 15%:
    {risky_periods.to_dict()}. Explain likely business risk."""
    return ask_gemini(prompt)
def generate_recommendation(all_kpis_dict):
    """Top-level executive recommendation across all KPIs."""
    prompt = f"""Given these business KPIs: {all_kpis_dict},
    provide ONE clear, prioritized recommendation for next quarter."""
    return ask_gemini(prompt)
