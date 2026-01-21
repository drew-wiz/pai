---
name: download-file-from-google-drive
description: Downloads files from Google Drive. Use when the user needs to retrieve a file, notes, or documents from Drive.
---

# Download File from Google Drive

This skill allows you to download files from Google Drive.

## Capability
The `scripts/run.py` script handles the download process. It supports:
- Downloading files by name.
- Searching within a specific parent folder (`--parent-folder`).

## Usage

### 1. Prerequisites
Ensure the virtual environment is set up and dependencies are installed.
- **Check/Create Venv:** `pai/skills/download-file-from-google-drive/scripts/venv`
- **Install Requirements:** `pai/skills/download-file-from-google-drive/scripts/requirements.txt`

### 2. Execution
Run the script using the python interpreter in the virtual environment.

```bash
skills/download-file-from-google-drive/scripts/venv/bin/python skills/download-file-from-google-drive/scripts/run.py --file-name <FILE_NAME> [OPTIONS]
```

**Required Arguments:**
- `--file-name <NAME>`: The name of the file to download.

**Optional Arguments:**
- `--parent-folder <FOLDER_NAME>`: The name of the parent folder to search within (e.g., 'career/whiteboards' or 'Customer Name').

### Example
To download "notes" from the "Acme Corp" folder:
```bash
skills/download-file-from-google-drive/scripts/venv/bin/python skills/download-file-from-google-drive/scripts/run.py --file-name "notes" --parent-folder "Acme Corp"
```
