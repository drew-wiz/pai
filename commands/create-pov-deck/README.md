# Create PoV Deck

This command creates a new Proof of Value Executive Readout slide deck.

## Description
Uses a Google Slides template to generate a new presentation, replacing placeholders for customer name, AE, and region. It also uses an LLM to summarize use case notes and insert them into the deck.

## Usage
Before attempting to run this script, you need to:
- crate a venv in this directory
- activate the venv
- install the deps into the venv

Only run the script inside the venv that you create. Never outside of that venv.

To run this command, execute the `run.py` script with the following named arguments:
`--customer-name "Customer Name"`
`--ae-name "AE Name"`
`--region "Region"`
`--notes-file "path/to/notes.txt"`
