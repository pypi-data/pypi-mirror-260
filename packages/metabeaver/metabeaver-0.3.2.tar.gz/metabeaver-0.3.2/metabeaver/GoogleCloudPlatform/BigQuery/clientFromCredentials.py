from google.cloud import bigquery
from google.oauth2 import service_account


# Create a bigquery client from a credentials.json
def get_bigquery_client(credentials_path='path/to/your/credentials.json'):
    # Explicitly provide the path to your service account key file
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    # Create a BigQuery client using the provided credentials
    client = bigquery.Client(credentials=credentials)

    return client


# Example usage with explicit credentials file path
#bigquery_client = get_bigquery_client(r'C:\Users\lukep\OneDrive\workandplay\credentials.json')



























