# Upload File Command

This command uploads a file to a customer's folder in Google Drive.

The command will search for a customer folder within a "customers" folder in your Google Drive. If it finds multiple folders matching the customer name, it will list them and exit. You can then re-run the command with the exact folder name.

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
commands/upload-file/venv/bin/python commands/upload-file/run.py --file-path <FILE_PATH> --target-folder <TARGET_FOLDER> [--gdoc] [--md]
```

Replace `<FILE_PATH>` with the path to the file you want to upload and `<TARGET_FOLDER>` with the name of the folder to upload to.

Use the `--gdoc` flag to convert the uploaded text file to a Google Doc.
Use the `--md` flag to convert the uploaded Markdown file to a Google Doc.
