from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st

# Project ID
PROJECT_ID = "bizanalytics-project"

# Read credentials from Streamlit Secrets
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# BigQuery client
client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)