from google.cloud import bigquery
from google.oauth2 import service_account

# Path to service account key
SERVICE_ACCOUNT_FILE = "credentials/gcp-key.json"

# Your GCP project ID
PROJECT_ID = "bizanalytics-project"

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)

# BigQuery client
client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)