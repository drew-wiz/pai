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
- **Install `uv`:** This skill uses `uv` for fast, unified Python package management.
  - MacOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Homebrew: `brew install uv`

### 2. Execution
Run the script using `uv run`. This will automatically handle virtual environment creation and dependency installation.

```bash
uv run --with-requirements skills/upload-file-to-google-drive/scripts/requirements.txt skills/upload-file-to-google-drive/scripts/run.py --file-path <FILE_PATH> [OPTIONS]
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
uv run --with-requirements skills/upload-file-to-google-drive/scripts/requirements.txt skills/upload-file-to-google-drive/scripts/run.py --file-path report.md --target-folder "Project X" --md
```
