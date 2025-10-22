import os
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def main(file_path, target_folder):
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

        file_name = os.path.basename(file_path)
        file_name_without_ext, file_ext = os.path.splitext(file_name)
        new_file_name = f"{file_name_without_ext}-UPLOADED-BY-PAI{file_ext}"

        file_metadata = {"name": new_file_name, "parents": [customer_folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        
        file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a file to a folder in Google Drive.")
    parser.add_argument("--file-path", type=str, required=True, help="The path to the file to upload.")
    parser.add_argument("--target-folder", type=str, required=True, help="The name of the folder to upload to.")
    args = parser.parse_args()
    main(args.file_path, args.target_folder)
