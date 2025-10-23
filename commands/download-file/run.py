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

def main(file_name, parent_folder):
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
        
        parent_folder_id = 'root'
        if parent_folder:
            path_parts = parent_folder.split('/')
            for part in path_parts:
                query = f"mimeType='application/vnd.google-apps.folder' and name contains '{part}' and '{parent_folder_id}' in parents"
                results = drive_service.files().list(q=query, fields="files(id, name)").execute()
                items = results.get("files", [])
                if len(items) == 0:
                    print(f"Could not find a folder with the name: {part} in path {parent_folder}")
                    return
                elif len(items) > 1:
                    print(f"Found multiple folders with the name: {part}. Please choose one:")
                    for i, item in enumerate(items):
                        print(f"{i + 1}: {item.get('name')}")
                    
                    choice = int(input("Enter the number of the folder you want to use: ")) - 1
                    parent_folder_id = items[choice].get("id")
                else:
                    parent_folder_id = items[0].get("id")

        query = f"name contains '{file_name}'"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        items = results.get("files", [])

        if len(items) == 0:
            print(f"Could not find a file with the name: {file_name}")
            return
        elif len(items) > 1:
            print("Found multiple files. Please be more specific.")
            for item in items:
                print(item.get('name'))
            return
        else:
            file_id = items[0].get("id")
            file_mime_type = items[0].get("mimeType")

        if "google-apps" in file_mime_type:
            request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
        else:
            request = drive_service.files().get_media(fileId=file_id)
        
        temp_dir = os.path.join(os.getcwd(), "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        file_path = os.path.join(temp_dir, file_name)
        
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
    parser = argparse.ArgumentParser(description="Download a file from Google Drive.")
    parser.add_argument("--file-name", type=str, required=True, help="The name of the file to download.")
    parser.add_argument("--parent-folder", type=str, help="The name of the parent folder to search within.")
    args = parser.parse_args()
    main(args.file_name, args.parent_folder)
