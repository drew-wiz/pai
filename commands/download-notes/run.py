import os
import io
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/drive.file"]

def main(target_folder):
    creds = None
    creds_dir = os.path.expanduser("~/.pai_credentials/google")
    creds_path = os.path.join(creds_dir, "credentials.json")
    token_path = os.path.join(creds_dir, "token.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        drive_service = build("drive", "v3", credentials=creds)
        
        # Find the "customers" folder
        customers_folder_id = None
        query = "mimeType='application/vnd.google-apps.folder' and name='customers'"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get("files", [])
        if items:
            customers_folder_id = items[0].get("id")
        
        if not customers_folder_id:
            print("Could not find the 'customers' folder.")
            return

        # Find the target folder
        customer_folder_id = None
        query = f"mimeType='application/vnd.google-apps.folder' and name contains '{target_folder}' and '{customers_folder_id}' in parents"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get("files", [])

        if len(items) == 0:
            print(f"Could not find a folder with the name: {target_folder}")
            return
        elif len(items) > 1:
            print("Found multiple customer folders. Please re-run the command with the exact customer name from the list below:")
            for item in items:
                print(item.get('name'))
            return
        else:
            customer_folder_id = items[0].get("id")

        # Find the notes file
        notes_file_id = None
        notes_file_mime_type = None
        query = f"name contains 'notes' and '{customer_folder_id}' in parents"
        results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        items = results.get("files", [])
        if items:
            notes_file_id = items[0].get("id")
            notes_file_mime_type = items[0].get("mimeType")

        if not notes_file_id:
            print(f"Could not find the notes file in folder: {target_folder}")
            return

        if "google-apps" in notes_file_mime_type:
            request = drive_service.files().export_media(fileId=notes_file_id, mimeType='text/plain')
        else:
            request = drive_service.files().get_media(fileId=notes_file_id)
        
        # Create a temporary directory if it doesn't exist
        temp_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        file_path = os.path.join(temp_dir, f"notes-{target_folder.replace(' ', '-')}.txt")
        
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
            
        print(f"File downloaded to {file_path}")

    except HttpError as error:
        print(f"An error occurred: {error}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a Google Doc from a folder.")
    parser.add_argument("--target-folder", type=str, required=True, help="The name of the folder to download from.")
    args = parser.parse_args()
    main(args.target_folder)
