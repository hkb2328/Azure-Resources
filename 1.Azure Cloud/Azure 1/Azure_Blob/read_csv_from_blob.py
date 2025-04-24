# Install this package if not installed
# pip install azure-storage-blob

from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import StringIO

# Azure Blob Storage account credentials
account_name = 'storageaccountgds'
account_key = '******************'
container_name = 'sales-data'
blob_name = 'customer_subscription.csv'

# Connection string (you can use this instead of account name and key)
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# Get the blob client
blob_client = container_client.get_blob_client(blob_name)

# Download blob content as a string
blob_data = blob_client.download_blob().content_as_text()

# Read the content into a pandas DataFrame
df = pd.read_csv(StringIO(blob_data))

# Display the DataFrame
print(df)
