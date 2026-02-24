---
name: download-file-from-google-drive
description: Downloads files from Google Drive. Use when the user needs to retrieve a file, notes, or documents from Drive.
---

# Download File from Google Drive

This skill allows you to download files from Google Drive with fuzzy search and interactive selection support.

## Capability
The `scripts/run.py` script handles the download process. It supports:
- **Fuzzy Search:** Downloads files and folders by partial name matching (`name contains`).
- **Interactive Selection:** If multiple files or folders match your query, the script lists the candidates and prompts for selection.
- **Parent Folder Search:** Searching within a specific parent folder (`--parent-folder`). 
- **Global Fallback:** If the specified parent folder path cannot be found, the script automatically falls back to a global search for the file.
- **Google Docs Export:** Automatically exports Google Docs as `text/plain` and appends a `.txt` extension.
- **Workspace Integration:** Downloads files directly to the `pai_workspace/` directory.

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
- `--file-name <NAME>`: The name (or partial name) of the file to download.

**Optional Arguments:**
- `--parent-folder <FOLDER_NAME>`: The name (or partial name) of the parent folder to search within.

### Examples

**Exact or partial search:**
```bash
skills/download-file-from-google-drive/scripts/venv/bin/python skills/download-file-from-google-drive/scripts/run.py --file-name "notes" --parent-folder "Harvard Medical School"
```

**Global search (if folder path is unknown):**
```bash
skills/download-file-from-google-drive/scripts/venv/bin/python skills/download-file-from-google-drive/scripts/run.py --file-name "harvard medical school notes"
```
