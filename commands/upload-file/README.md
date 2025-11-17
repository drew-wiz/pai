# Upload File Command

This command uploads a file to a specified folder in Google Drive.

The command will search for the specified folder in your Google Drive. If it finds multiple folders matching the provided name, it will list them and exit. You can then re-run the command with the exact folder name.

## Prerequisites

Before running this command, you must create a virtual environment and install the required dependencies. If a `venv` directory already exists, you can skip these steps.

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv commands/upload-file/venv
    ```

2.  **Install dependencies:**
    ```bash
    commands/upload-file/venv/bin/python -m pip install -r commands/upload-file/requirements.txt
    ```

## Usage

```bash
commands/upload-file/venv/bin/python commands/upload-file/run.py --file-path <FILE_PATH> (--target-folder <TARGET_FOLDER> | --absolute-directory-path <ABSOLUTE_DIRECTORY_PATH>) [--gdoc] [--md]
```

Replace `<FILE_PATH>` with the path to the file you want to upload.

You must specify one of the following options for the destination folder:
-   `--target-folder <TARGET_FOLDER>`: The name of the folder to upload to. This performs a "contains" search, so partial names are allowed.
-   `--absolute-directory-path <ABSOLUTE_DIRECTORY_PATH>`: The absolute path of the folder to upload to (e.g., 'Folder A/Folder B'). This performs an exact match search.

Use the `--gdoc` flag to convert the uploaded text file to a Google Doc.
Use the `--md` flag to convert the uploaded Markdown file to a Google Doc.
