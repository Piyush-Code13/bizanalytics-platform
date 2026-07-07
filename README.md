# AI-Powered Business Analytics Platform

A conversational BI tool for the Olist Brazilian E-Commerce dataset. Ask a business question in plain English, get back the generated SQL, live results from BigQuery, a chart, and a written business insight — no SQL or dashboard-clicking required.

**Live demo:** https://bizanalytics-platform.streamlit.app/


## What it does

1. You type a question — e.g. *"Show top 10 product categories by revenue"*
2. Gemini converts it into a SQL query
3. The query runs against a BigQuery warehouse built from the Olist dataset
4. Results render as a table and an interactive Plotly chart
5. A written business insight (Observation → Impact → Risk → Recommendation) summarizes what the numbers mean

Natural language question
        ↓
Gemini → SQL generation
        ↓
BigQuery execution
        ↓
Pandas DataFrame
        ↓
Plotly chart  +  Business insight
        ↓
Streamlit UI


The underlying data warehouse is built with **dbt** on top of raw Olist tables loaded into BigQuery, so the SQL the model generates runs against modeled fact/dimension tables rather than raw CSV exports.


## Tech stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data warehouse | Google BigQuery |
| Transformation | dbt |
| AI / NL-to-SQL | Google Gemini (`gemini-2.5-flash`) |
| Visualization | Plotly |
| Frontend | Streamlit |
| Deployment | Streamlit Community Cloud |


## Project structure

├── ai_dashboard.py              # Streamlit entry point (deployed)
├── ai_query.py                  # Orchestrates the question → SQL → chart → insight pipeline
├── text_to_sql.py               # Gemini-based natural language → SQL
├── bigquery_helper.py           # Executes SQL against BigQuery, returns a DataFrame
├── chart_generator.py           # Builds the Plotly chart for a result set
├── insight_generator.py         # Gemini-based business insight for a result set
├── gemini_helper.py             # Shared Gemini client (model config, prompt call, error handling)
├── prompts.py                   # Prompt templates
├── dbt_project/                 # dbt models — fact/dimension tables on top of raw Olist data
├── Notebooks/                   # Build sequence: explore → clean → load to BigQuery → connection test → Gemini integration
├── data/                        # Local data assets
└── requirements.txt
```

> Note: `app.py`, `ai_dashboard2.py`, `ai_insights.py`, `business_analyst.py`, and `recommendation_engine.py` are earlier iterations / in-progress experiments and are not part of the deployed app. They're kept in the repo for reference while those features are finished.


## Running it locally


git clone https://github.com/Piyush-Code13/bizanalytics-platform.git
cd bizanalytics-platform
pip install -r requirements.txt

Create a `.env` file in the project root:

GOOGLE_API_KEY=your_gemini_api_key


You'll also need a GCP service account with BigQuery access, configured the way `bigquery_helper.py` expects (see that file for the exact credential loading method).

Then run:
streamlit run ai_dashboard.py
## Example questions to try

- Show top 10 product categories by revenue
- Which states have the highest revenue?
- Which categories have the most orders?
- Show average review score by category
- Which sellers generate the highest revenue?

---

## Author

Piyush Bande
