import os
import requests
from bs4 import BeautifulSoup
import zipfile
import pandas as pd
from io import BytesIO
from datetime import datetime
import logging
from github import Github

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base URL of the Open Data portal
base_url = "https://opendata.citywindsor.ca"

# URL of the specific dataset
dataset_url = "https://opendata.citywindsor.ca/Details/218"

# Teams Webhook URL 
TEAMS_WEBHOOK_URL = "https://stclairconnect.webhook.office.com/webhookb2/d91ec366-59e9-4835-a616-8242da44c5a9@c986676f-9b39-4d08-b4f8-a668e0e8c6a5/IncomingWebhook/6b04fdd45fea43aa839e0ac40e091f46/ed79718a-72e7-4443-a257-aa80b30707c2/V2v04MMrkaIbd4pDceUUX-eQAZnsFwSgZawF8phu_m1Rg1"

# Function to get the latest ZIP file URL
def get_latest_zip_url(dataset_url):
    try:
        logging.info(f"Fetching dataset page: {dataset_url}")
        response = requests.get(dataset_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the download link based on the actual HTML structure
        download_link = soup.find('a', href=lambda href: href and 'google_transit.zip' in href)

        if download_link:
            zip_url = base_url + download_link['href']
            logging.info(f"Found ZIP file URL: {zip_url}")
            return zip_url
        else:
            logging.warning("Download link not found on the page.")
            return None
    except Exception as e:
        logging.error(f"Failed to get the latest ZIP file URL: {e}")
        logging.error("Please check the URL's validity and your network connection. If the issue persists, consider retrying later.")
        return None

# Function to download and convert ZIP content to Excel in buffer rather than local file
def download_and_convert_to_excel_in_memory(url):
    try:
        logging.info(f"Downloading ZIP file from: {url}")
        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            txt_files = [name for name in zip_file.namelist() if name.endswith(".txt")]

            if txt_files:
                # Create an in-memory Excel file
                output_excel = BytesIO()
                with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
                    for file in txt_files:
                        logging.info(f"Reading file: {file}")
                        with zip_file.open(file) as f:
                            try:
                                df = pd.read_csv(f, delimiter='\t', encoding='utf-8')
                                sheet_name = os.path.splitext(os.path.basename(file))[0]  # Use file name as sheet name
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                                logging.info(f"Added sheet: {sheet_name}")
                            except Exception as e:
                                logging.error(f"Failed to read {file}: {e}")

                output_excel.seek(0)  # Move to the beginning of the BytesIO buffer
                logging.info("Combined Excel file created in memory.")
                return output_excel
            else:
                logging.warning("No .txt files found to combine.")
                return None
    except Exception as e:
        logging.error(f"Failed to download or extract {url}: {e}")
        return None

# Function to upload file to GitHub
def upload_to_github(file_content, file_name, repo_name, branch_name, github_token):
    try:
        logging.info(f"Uploading {file_name} to GitHub repository {repo_name} on branch {branch_name}")
        
        # Initialize GitHub instance
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        branch = repo.get_branch(branch_name)

        # Create the file in the repository
        repo.create_file(
            path=f"{file_name}",  # Path in the repository
            message=f"Add {file_name}",  # Commit message
            content=file_content.read(),  # File content from BytesIO
            branch=branch_name 
        )

        logging.info(f"File {file_name} uploaded successfully to GitHub.")
        return True
    except Exception as e:
        logging.error(f"Failed to upload file to GitHub: {e}")
        return False

# Function to send Teams notification
def send_teams_notification(message):
    """
    Send a notification to Microsoft Teams using a Webhook.
    """
    if not TEAMS_WEBHOOK_URL:
        logging.error("Teams Webhook URL is not set.")
        return

    # Teams message payload
    payload = {
        "text": message
    }

    try:
        # Send the HTTP POST request to the Webhook URL
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()  # Raise an error for bad status codes
        logging.info("Teams notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send Teams notification: {e}")

# Main function to run the workflow
def main():
    zip_url = get_latest_zip_url(dataset_url)
    if zip_url:
        excel_content = download_and_convert_to_excel_in_memory(zip_url)
        if excel_content:
            logging.info("Processing completed successfully. Excel file created in memory.")

            # Define file name based on current timestamp
            file_name = f"combined_bus_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            # Get GitHub token from environment variable
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                logging.error("GitHub token is not set in the environment variables.")
                return

            repo_name = "iTroyHector/Capstone" 
            branch_name = "gfts_data"  # branch name
            logging.info(f"GITHUB_TOKEN: {os.getenv('GITHUB_TOKEN')}")

            if upload_to_github(excel_content, file_name, repo_name, branch_name, github_token):
                # Send Teams notification
                message = (
                    "Weekly Web-scraping Dataset Update\n\n"
                    f"The file **{file_name}** has been successfully uploaded to the GitHub repository "
                    f"**{repo_name}** on branch **{branch_name}**."
                )
                send_teams_notification(message)
    else:
        logging.error("Could not find the latest ZIP file URL.")

# Run the main function immediately when the script is executed
if __name__ == "__main__":
    logging.info("Starting the workflow...")
    main()  # Directly call main() for immediate execution
