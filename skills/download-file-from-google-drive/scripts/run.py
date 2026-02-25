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

def main(file_name, parent_folder, file_id=None):
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
        
        if file_id:
            file_metadata = drive_service.files().get(fileId=file_id, fields="id, name, mimeType").execute()
            file_id = file_metadata.get("id")
            final_file_name = file_metadata.get("name")
            file_mime_type = file_metadata.get("mimeType")
            print(f"Downloading file ID: {file_id} ({final_file_name})")
        else:
            parent_folder_id = 'root'
            search_global = False

            if parent_folder:
                path_parts = parent_folder.split('/')
                for part in path_parts:
                    query = f"mimeType='application/vnd.google-apps.folder' and name contains '{part}' and '{parent_folder_id}' in parents"
                    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
                    items = results.get("files", [])
                    
                    if len(items) == 0:
                        print(f"Warning: Could not find folder '{part}' in path '{parent_folder}'. Falling back to global search.")
                        search_global = True
                        break
                    elif len(items) > 1:
                        print(f"Found multiple folders matching '{part}'. Please choose one:")
                        for i, item in enumerate(items):
                            print(f"{i + 1}: {item.get('name')}")
                        
                        while True:
                            try:
                                choice = int(input("Enter the number of the folder you want to use: ")) - 1
                                if 0 <= choice < len(items):
                                    parent_folder_id = items[choice].get("id")
                                    break
                                else:
                                    print("Invalid choice. Please try again.")
                            except ValueError:
                                 print("Invalid input. Please enter a number.")
                    else:
                        parent_folder_id = items[0].get("id")

            query = f"name contains '{file_name}'"
            if not search_global and parent_folder_id != 'root':
                 query += f" and '{parent_folder_id}' in parents"
            
            # Exclude trashed files
            query += " and trashed = false"

            results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
            items = results.get("files", [])

            if len(items) == 0:
                print(f"Could not find a file with the name: {file_name}")
                return
            elif len(items) > 1:
                print(f"Found multiple files matching '{file_name}'. Please choose one:")
                for i, item in enumerate(items):
                    print(f"{i + 1}: {item.get('name')}")
                
                while True:
                    try:
                        choice = int(input("Enter the number of the file you want to download: ")) - 1
                        if 0 <= choice < len(items):
                            file_id = items[choice].get("id")
                            file_mime_type = items[choice].get("mimeType")
                            final_file_name = items[choice].get("name") # Use actual name
                            break
                        else:
                             print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                file_id = items[0].get("id")
                file_mime_type = items[0].get("mimeType")
                final_file_name = items[0].get("name")

        if "google-apps" in file_mime_type:
            if "presentation" in file_mime_type:
                request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                final_file_name += ".pptx"
            else:
                # Export Google Docs as plain text
                request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
                final_file_name += ".txt" # Append extension for text export
        else:
            request = drive_service.files().get_media(fileId=file_id)
        
        # Save to pai_workspace
        workspace_dir = os.path.join(os.getcwd(), "pai_workspace")
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)
            
        file_path = os.path.join(workspace_dir, final_file_name)
        
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
    parser.add_argument("--file-name", type=str, help="The name of the file to download.")
    parser.add_argument("--file-id", type=str, help="The ID of the file to download.")
    parser.add_argument("--parent-folder", type=str, help="The name of the parent folder to search within.")
    args = parser.parse_args()
    if not args.file_name and not args.file_id:
        parser.error("Either --file-name or --file-id must be provided.")
    main(args.file_name, args.parent_folder, args.file_id)
