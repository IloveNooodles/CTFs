from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load the service account key from the JSON object
credentials = service_account.Credentials.from_service_account_info(
    json_keyfile_dict,  # Replace with your JSON object
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Create a client or service object
# Replace 'service' with the specific service you want to access (e.g., 'drive', 'pubsub', etc.)
service = build('service', 'v1', credentials=credentials)

# Use the client or service object to interact with Google Cloud services
# Perform API calls or operations specific to the service