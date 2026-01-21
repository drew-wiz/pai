---
name: upload-file-to-google-drive
description: Uploads files to Google Drive. Use when the user wants to upload a file, backup a document, or save content to Drive.
---

# Upload File to Google Drive

This skill allows you to upload files to a specific folder in Google Drive.

## Capability
The `scripts/run.py` script handles the upload process. It supports:
- Uploading local files to a specific Google Drive folder.
- Fuzzy matching folder names (`--target-folder`).
- Exact path matching (`--absolute-directory-path`).
- Converting text/markdown files to Google Docs on upload (`--gdoc`, `--md`).

## Usage

### 1. Prerequisites
Ensure the virtual environment is set up and dependencies are installed.
- **Check/Create Venv:** `pai/skills/upload-file-to-google-drive/scripts/venv`
- **Install Requirements:** `pai/skills/upload-file-to-google-drive/scripts/requirements.txt`

### 2. Execution
Run the script using the python interpreter in the virtual environment.

```bash
skills/upload-file-to-google-drive/scripts/venv/bin/python skills/upload-file-to-google-drive/scripts/run.py --file-path <FILE_PATH> [OPTIONS]
```

**Required Arguments:**
- `--file-path <PATH>`: Path to the local file to upload.
- **Destination (One required):**
    - `--target-folder <NAME>`: Name of the destination folder (partial match).
    - `--absolute-directory-path <PATH>`: Absolute path in Drive (e.g., `Folder/Subfolder`).

**Optional Arguments:**
- `--gdoc`: Convert text file to Google Doc.
- `--md`: Convert Markdown file to Google Doc.

### Example
To upload `report.md` to the 'Project X' folder and convert it to a Google Doc:
```bash
skills/upload-file-to-google-drive/scripts/venv/bin/python skills/upload-file-to-google-drive/scripts/run.py --file-path report.md --target-folder "Project X" --md
```
