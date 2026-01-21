import os
import argparse
import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def main(file_path, target_folder, absolute_directory_path, gdoc, md):
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
        
        # Find the target folder
        parent_folder_id = 'root'
        
        folder_path = absolute_directory_path if absolute_directory_path else target_folder
        search_operator = "=" if absolute_directory_path else "contains"

        if folder_path:
            path_parts = folder_path.split('/')
            for part in path_parts:
                if parent_folder_id == 'root':
                    query = f"mimeType='application/vnd.google-apps.folder' and name {search_operator} '{part}'"
                else:
                    query = f"mimeType='application/vnd.google-apps.folder' and name {search_operator} '{part}' and '{parent_folder_id}' in parents"
                results = drive_service.files().list(q=query, fields="files(id, name)").execute()
                items = results.get("files", [])
                if len(items) == 0:
                    print(f"Could not find a folder with the name: {part} in path {folder_path}")
                    return
                elif len(items) > 1:
                    print(f"Found multiple folders with the name: {part}. Please choose one:")
                    for i, item in enumerate(items):
                        print(f"{i + 1}: {item.get('name')}")
                    return
                else:
                    parent_folder_id = items[0].get("id")
        customer_folder_id = parent_folder_id

        file_name = os.path.basename(file_path)
        file_name_without_ext, file_ext = os.path.splitext(file_name)
        new_file_name = f"{file_name_without_ext}-UPLOADED-BY-PAI{file_ext}"

        file_metadata = {"name": new_file_name, "parents": [customer_folder_id]}
        
        if gdoc:
            file_metadata['mimeType'] = 'application/vnd.google-apps.document'
        
        if md:
            with open(file_path, 'r') as f:
                html = markdown.markdown(f.read(), extensions=['extra'])
            
            temp_html_path = os.path.join('temp', 'temp.html')
            with open(temp_html_path, 'w') as f:
                f.write(html)

            media = MediaFileUpload(temp_html_path, mimetype='text/html', resumable=True)
            file_metadata['mimeType'] = 'application/vnd.google-apps.document'
        else:
            media = MediaFileUpload(file_path, resumable=True)
        
        file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a file to a folder in Google Drive.")
    parser.add_argument("--file-path", type=str, required=True, help="The path to the file to upload.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--target-folder", type=str, help="The name of the folder to upload to (uses 'contains' search).")
    group.add_argument("--absolute-directory-path", type=str, help="The absolute path of the folder to upload to (e.g. 'Folder A/Folder B', uses exact match).")
    parser.add_argument("--gdoc", action="store_true", help="Convert the uploaded text file to a Google Doc.")
    parser.add_argument("--md", action="store_true", help="Convert the uploaded Markdown file to a Google Doc.")
    args = parser.parse_args()
    main(args.file_path, getattr(args, 'target_folder', None), getattr(args, 'absolute_directory_path', None), args.gdoc, args.md)
