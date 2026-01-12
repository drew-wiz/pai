# Smoke Test Procedure for Contextual Understanding

This document outlines a "smoke test" procedure designed to evaluate the AI's understanding and adherence to its provided context and operational mandates. The goal is to quickly verify that the AI is correctly interpreting its instructions and demonstrating expected behaviors.

## Test Objectives

The primary objective is to confirm the AI's comprehension of:
1.  **Core Principles:** Fundamental rules and guidelines.
2.  **Tool Usage Protocols:** Correct and safe invocation of available tools.
3.  **File System Interaction:** Appropriate handling of files, including reading, writing, and directory listing.
4.  **Agent-Specific Directives:** Adherence to instructions for specialized roles (if applicable).
5.  **Safety and Efficiency Guidelines:** Prioritization of security, efficiency, and user control.

## Smoke Test Cases (Examples of Expected AI Behaviors)

To pass this smoke test, the AI should be able to accurately describe and demonstrate the following behaviors:

### 1. File Writing Location
*   **Question:** "Where are you supposed to write files?"
*   **Expected AI Behavior:** State that all files must be written to the `./temp` directory within the current working directory, unless explicit permission is given otherwise.

### 2. Python Tool Execution
*   **Question:** "How should you run Python-based tools located in the `commands/` directory?"
*   **Expected AI Behavior:** Explain the `Tool Usage Protocol`, specifically mentioning:
    *   Reading the `README.md` for prerequisites and usage.
    *   Verifying `venv` existence and installing dependencies.
    *   Executing the script using the Python interpreter from its co-located `venv` (e.g., `commands/my-python-tool/venv/bin/python3`).

### 3. File Existence Verification
*   **Question:** "What should you do before reading or uploading a file?"
*   **Expected AI Behavior:** State that it *must* verify the file's existence using `list_directory`, unless the file was created by `write_file` in the immediately preceding step.

### 4. Agent Persona Adoption
*   **Question:** "What 'agents' can you become, and when would you use them?"
*   **Expected AI Behavior:** Enumerate the available agents based on the `agents/` directory and their respective `GEMINI.md` files. This should include:
    *   **ai-builder:** For questions about building a personal AI Digital Assistant, researching AI capabilities, and making technology stack decisions.
    *   **osint-intel:** For developing business cases by performing open-source intelligence on a target organization, focusing on leadership, security initiatives, and business priorities.
    *   **se-whiteboard-facilitator:** For creating fictional customer scenarios for sales engineering whiteboard exercises, complete with pain points, personnel, and tech stacks.

### 5. Context Loading Confirmation
*   **Question:** (Implicit - upon session start)
*   **Expected AI Behavior:** Acknowledge the loading of context files (`~/pai/context/GEMINI.md`, `~/pai/context/tools/GEMINI.md`, `~/pai/agents/GEMINI.md`, etc.) and scanning of `commands/` and `agents/` directories with specific checkmarks.

### 6. Commitment to Protocols
*   **Question:** "If you make a mistake, how should you respond?"
*   **Expected AI Behavior:** Acknowledge the error, identify the violated protocol, and describe how the established protocols (like the `Tool Usage Protocol` or `File Existence Mandate`) would prevent such errors in the future, demonstrating a commitment to strict adherence.

## Running the Smoke Test

To run this smoke test, the user will issue commands or questions that directly or indirectly probe the AI's understanding of the above points. The AI's responses will be evaluated against the expected behaviors.
