# Skill Discovery Protocol

My skills are located in the `pai/skills/` directory. Each subdirectory represents a single skill.

To understand a skill, you MUST read its `SKILL.md` file. This file will explain the skill's purpose, description, and contain instructions on how to use it.

To use a skill, you must follow the instructions in its `SKILL.md`.

## Editing Skills
NEVER edit the code for any skills. If you run into a problem running the skill, immediately halt and ask me for input. The skills are meant to succeed as-is and if there is a problem, they need to be investigated by me.

## Writing Files
If you need to create a file, use the `temp` directory to temporarily write the file.

## Python Skill Conventions

For any skill written in Python, the implementation usually resides in a `scripts/` subdirectory. The following conventions MUST be followed:

1.  **Virtual Environment:** Each Python skill directory MUST contain its own `venv` directory within `scripts/`, e.g., `scripts/venv`.
2.  **Dependencies:** All dependencies MUST be listed in a `requirements.txt` file within the `scripts/` directory.
3.  **Execution:** The script MUST be executed using the Python interpreter from its co-located `venv`. For example: `pai/skills/my-skill/scripts/venv/bin/python3 pai/skills/my-skill/scripts/run.py`. Unless otherwise stated, always use `python3` and never use `python`.

If you see a `requirements.txt` file for a Python script, always create a virtual environment to install the dependencies. Never try to install them globally.

## Available Skills

### `upload-file-to-google-drive`

Uploads a file to Google Drive. See `skills/upload-file-to-google-drive/SKILL.md` for more information.

## Legacy Tools (Commands)

The `pai/commands` directory contains legacy tools that have not yet been converted to Skills.

### `download-file`

Downloads a file from Google Drive. See `commands/download-file/README.md` for more information.
