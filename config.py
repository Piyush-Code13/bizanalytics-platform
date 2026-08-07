import os
import streamlit as st

from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "bizanalytics-project")

try:
    # Streamlit Cloud
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

except Exception:
    # Local / Docker
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS",
            "credentials/gcp-key.json"
        )
    )

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)