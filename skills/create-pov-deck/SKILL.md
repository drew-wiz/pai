---
name: create-pov-deck
description: Creates a new Proof of Value (PoV) Executive Readout slide deck. Use when the user wants to generate a PoV presentation from notes.
---

# Create PoV Deck

This skill automates the creation of a Proof of Value Executive Readout slide deck using a Google Slides template.

## Capability
The `scripts/run.py` script:
- Copies a Google Slides template.
- Replaces placeholders with customer-specific information.
- Uses an LLM to summarize use case notes and inserts them into the deck.

## Usage

### 1. Prerequisites
Ensure the virtual environment is set up and dependencies are installed.
- **Check/Create Venv:** `pai/skills/create-pov-deck/scripts/venv`
- **Install Requirements:** `pai/skills/create-pov-deck/scripts/requirements.txt`

### 2. Execution
Run the script using the python interpreter in the virtual environment.

```bash
skills/create-pov-deck/scripts/venv/bin/python skills/create-pov-deck/scripts/run.py --customer-name <CUSTOMER> --ae-name <AE> --region <REGION> --notes-file <PATH_TO_NOTES>
```

**Required Arguments:**
- `--customer-name "Name"`: Name of the customer.
- `--ae-name "Name"`: Name of the Account Executive.
- `--region "Region"`: Region (e.g., "US East").
- `--notes-file "path/to/notes.txt"`: Path to the text file containing use case notes.

### Example
```bash
skills/create-pov-deck/scripts/venv/bin/python skills/create-pov-deck/scripts/run.py --customer-name "Acme Corp" --ae-name "Jane Doe" --region "US Public Sector" --notes-file "notes.txt"
```

### 3. Gathering the notes file
You will need to find the 'notes' file. Generally speaking this is in my Google Drive in 'customers/$(CUSTOMER_NAME)/$(CUSTOMER_NAME)-notes'. You will need to search in my drive to find it as the naming convention is not always 100% predictable. However, you will always find the file as a Google Doc in that location.
