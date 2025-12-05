# Tool Discovery Protocol

My tools are located in the `pai/commands/` directory. Each subdirectory represents a single tool.

To understand a tool, you MUST read its `README.md` file. This file will explain the tool's purpose, description, and how to use it.

To use a tool, you must construct and execute the command as specified in its `README.md`.

## Editing Tools
NEVER edit the code for any tools. If you run into a problem running the tool, immediately halt and ask me for input. The tools are meant to succeed as-is and if there is a problem, they need to be investigated by me. 

## Writing Files
If you need to create a file, use the `temp` directory to temporarily write the file.

## Python Tool Conventions

For any tool written in Python, the following conventions MUST be followed:

1.  **Virtual Environment:** Each Python command directory MUST contain its own `venv` directory.
2.  **Dependencies:** All dependencies MUST be listed in a `requirements.txt` file within the command's directory.
3.  **Execution:** The script MUST be executed using the Python interpreter from its co-located `venv`. For example: `pai/commands/my-python-tool/venv/bin/python3 pai/commands/my-python-tool/run.py`. Unless otherwise stated, always use `python3` and never use `python`.

If you see a `requirements.txt` file for a Python script, always create a virtual environment to install the dependencies. Never try to install them globally.

## Available Tools

### `download-file`

Downloads a file from Google Drive. See `commands/download-file/README.md` for more information.

### `upload-file`

Uploads a file to Google Drive. See `commands/upload-file/README.md` for more information.
