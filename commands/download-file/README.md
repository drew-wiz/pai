# Download File Command

This command downloads a file from Google Drive.

## Prerequisites

Before running this command, you must create a virtual environment and install the required dependencies. If a `venv` directory already exists, you can skip these steps.

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv commands/download-file/venv
    ```

2.  **Install dependencies:**
    ```bash
    commands/download-file/venv/bin/python -m pip install -r commands/download-file/requirements.txt
    ```

## Usage

```bash
commands/download-file/venv/bin/python commands/download-file/run.py --file-name <FILE_NAME> [--parent-folder <PARENT_FOLDER>]
```

Replace `<FILE_NAME>` with the name of the file you want to download and `<PARENT_FOLDER>` with the path to the parent folder to search within (e.g., `career/whiteboards`).

## Workflows

### General Workflows
Use your existing context to decide how to use this command. See below for specific workflows. If none of the workflows below are asked for, then fall back to using your existing context to decide how to use this command.

### Downloading Customer Notes

To download customer notes, use the following command, replacing `<CUSTOMER_NAME>` with the name of the customer:

```bash
commands/download-file/venv/bin/python commands/download-file/run.py --file-name "notes" --parent-folder "<CUSTOMER_NAME>"
