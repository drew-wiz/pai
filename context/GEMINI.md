# Personal AI Infrastructure (PAI)

This is the master context for my Personal AI Infrastructure.

## Core Principles
- **Modular Tools:** My capabilities are defined by the tools in the `commands/` directory.
- **Context-Driven:** My understanding of the world is shaped by the files in the `context/` directory.
- **Model-Agnostic:** The context files are written in plain markdown and are not tied to any specific AI model. They will always be named `_index.md`

## Key Directories
On startup, you MUST read the file named `_index.md` in each of these directories. If the contents of any of these files mention other `_index.md` files, then read those files as well.

READ THE `GEMINI.md` FILE INSIDE EACH OF THE DIRECTORIES BEFORE RESPONDING TO EVERY PROMPT.

- `skills/`: Contains the skills that I can perform. 
- `context/`: Contains the knowledge base that informs my actions.
- `personas/`: Where I store various personas that you will assume solve particular problems.
