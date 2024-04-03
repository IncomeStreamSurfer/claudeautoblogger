import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get the Shopify store URL and access token from environment variables
store_url = os.getenv("SHOPIFY_STORE_URL")
access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

# Define the page types to retrieve
page_types = ["custom_collections", "pages", "products", "blogs"]

# Set the headers for the API requests
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": access_token
}

# Iterate over each page type
for page_type in page_types:
    # Set the API endpoint for the page type
    api_url = f"{store_url}/admin/api/2021-07/{page_type}.json"

    # Send a GET request to the Shopify API to retrieve the page data
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the page information
        pages = data[page_type]

        # Save the page information to a .txt file with UTF-8 encoding
        with open(f"{page_type}.txt", "w", encoding="utf-8") as file:
            for page in pages:
                handle = page["handle"]
                
                # Determine the page type based on the API endpoint
                if page_type == "custom_collections":
                    page_type_prefix = "collections"
                elif page_type == "pages":
                    page_type_prefix = "pages"
                elif page_type == "products":
                    page_type_prefix = "products"
                elif page_type == "blogs":
                    page_type_prefix = "blogs"
                else:
                    page_type_prefix = ""
                
                file.write(f"ID: {page['id']}\n")
                file.write(f"Handle: /{page_type_prefix}/{handle}\n")
                file.write(f"Title: {page['title']}\n")

        print(f"{page_type.capitalize()} information saved to {page_type}.txt")
    else:
        print(f"Error retrieving {page_type}: {response.status_code} - {response.text}")
