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
- **Install `uv`:** This skill uses `uv` for fast, unified Python package management.
  - MacOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Homebrew: `brew install uv`

### 2. Execution
Run the script using `uv run`. This will automatically handle virtual environment creation and dependency installation.

```bash
uv run --with-requirements skills/create-pov-deck/scripts/requirements.txt skills/create-pov-deck/scripts/run.py --customer-name <CUSTOMER> --ae-name <AE> --region <REGION> --notes-file <PATH_TO_NOTES> [--additional-instructions <INSTRUCTIONS>]
```

**Required Arguments:**
- `--customer-name "Name"`: Name of the customer.
- `--ae-name "Name"`: Name of the Account Executive.
- `--region "Region"`: Region (e.g., "US East").
- `--notes-file "path/to/notes.txt"`: Path to the text file containing use case notes.

**Optional but Critical Arguments:**
- `--additional-instructions "Instructions"`: Specific user instructions, priorities, or concerns. **MANDATORY** to use this when the user provides specific goals in their prompt to ensure they take precedence over notes.

### Example
```bash
uv run --with-requirements skills/create-pov-deck/scripts/requirements.txt skills/create-pov-deck/scripts/run.py --customer-name "Acme Corp" --ae-name "Jane Doe" --region "US Public Sector" --notes-file "notes.txt"
```

### 3. Gathering the notes file
You will need to find the 'notes' file. Generally speaking this is in my Google Drive in 'customers/$(CUSTOMER_NAME)/$(CUSTOMER_NAME)-notes'. You will need to search in my drive to find it as the naming convention is not always 100% predictable. However, you will always find the file as a Google Doc in that location.

## Information Gathering and Accuracy
When preparing the input for this skill, follow these priority rules:
1. **User Prompt:** Prioritize any specific concerns or details provided by the user in their request. **You MUST pass these concerns to the script using the `--additional-instructions` flag.**
2. **Customer Notes:** Use the customer notes to fill in any blanks or provide context not present in the user prompt.
3. **No Speculation:** NEVER speculate or guess. If neither the prompt nor the notes provide a complete picture of the priorities, challenges, or impacts, YOU MUST ask the user for clarification and more details before proceeding.

## Output
Upon successful execution, the script will output a summary block. You MUST extract this information and present it clearly to the user, including:
- **Presentation Link:** `https://docs.google.com/presentation/d/<PRESENTATION_ID>/edit`
- **Folder Location:** `templates/ai-workspace` (Folder ID: `1pWnLJ6FlLmpgaYmMjnHpQEru1su7OTO9`)
- **Customer Name & AE**
