# Download Notes Command

This command downloads a Google Doc file from a customer's folder in Google Drive and saves it to a temporary directory.

The command will search for a customer folder within a "customers" folder in your Google Drive. If it finds multiple folders matching the customer name, it will list them and exit. You can then re-run the command with the exact folder name.

## Prerequisites

Before running this command, you must create a virtual environment and install the required dependencies.

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv commands/download-notes/venv
    ```

2.  **Install dependencies:**
    ```bash
    commands/download-notes/venv/bin/python -m pip install -r commands/download-notes/requirements.txt
    ```

## Usage

```bash
commands/download-notes/venv/bin/python commands/download-notes/run.py --target-folder <TARGET_FOLDER>
```

Replace `<TARGET_FOLDER>` with the name of the folder you want to download the notes from.
