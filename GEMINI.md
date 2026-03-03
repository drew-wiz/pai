## MANDATORY CONTEXT CHECK
You MUST load these context files before responding:
1. Read ~/pai/context/GEMINI.md
2. Read ~/pai/context/tools/GEMINI.md

You will provide incorrect responses without this context.

# 🚨🚨🚨 MANDATORY FIRST ACTION - DO THIS IMMEDIATELY 🚨🚨🚨

## SESSION STARTUP REQUIREMENT (NON-NEGOTIABLE)

**BEFORE DOING OR SAYING ANYTHING, YOU MUST:**

1. **SILENTLY AND IMMEDIATELY READ THESE FILES (using Read tool):**
   - `~/pai/context/GEMINI.md` - The complete context system documentation
   - `~/pai/context/tools/GEMINI.md` - All available tools and their usage
   - `~/pai/personas/GEMINI.md` - All available personas and their usage
   - any `GEMINI.md` files referenced in the above files must also be read

2. **SILENTLY SCAN:** `~/pai/commands` directory (using LS tool) to see available commands

4. **SILENTLY SCAN:** `~/pai/personas` directory (using LS tool) to see available personas

4. **ONLY AFTER ACTUALLY READING ALL FILES, then acknowledge:**
   "✅ Context system loaded - I understand the context architecture.
   ✅ Tools context loaded - I know my commands and capabilities.
   ✅ Projects loaded - I'm aware of active projects and their contexts."

**DO NOT LIE ABOUT LOADING THESE FILES. ACTUALLY LOAD THEM FIRST.**

**FAILURE TO ACTUALLY LOAD BEFORE CLAIMING = LYING TO USER**

You cannot properly respond to ANY request without ACTUALLY READING:
- The complete context system architecture (from ~/pai/context/GEMINI.md)
- Your tools and when to use them (from ~/pai/context/tools/GEMINI.md)
- Available commands (from ~/pai/commands/ directory)
- Available personas (from ~/pai/personas/ directory)

**THIS IS NOT OPTIONAL. ACTUALLY DO THE READS BEFORE THE CHECKMARKS.**

## File Existence Mandate

Before executing any command that reads, modifies, or uploads a file, you MUST first verify that the file exists on the filesystem. The only exception is if you created the file using the write_file tool in the immediately preceding step. Use the list_directory tool to confirm the file's existence if there is any
  uncertainty.

## Tool Usage Protocol

When using any tool, especially those in the commands/ directory, you MUST follow this sequence without deviation:

 1. Read the README: Before the first use of a tool in a session, you MUST read its corresponding README.md file to understand its purpose, prerequisites, and exact usage syntax.
 2. Verify Prerequisites: Before execution, you MUST confirm that all prerequisites from the README.md have been met. This includes, but is not limited to:
     * Ensuring the necessary virtual environment (venv) exists and is used for execution.
     * Installing all required dependencies from a requirements.txt file.
     * Confirming that any required input files exist.
 3. Execute Exactly: You MUST construct and execute the command precisely as shown in the Usage section of the documentation, using the specified virtual environment's interpreter.

## File Writing Mandate

When you write any files, write them to the `./pai_workspace` directory in the cwd. NEVER write files outside the `./temp` directory unless given explicit permision to do so.

## Opertaional Mandates

When you run any command, it should always be a command that will complete and not hang, waiting for inputs. Examples of 'bad' commands are simply SSH'ing into a machine without a predefined command, because that will just sit at a bash prompt forever. Other 'bad' commands are SSH commands that could prompt you to confirm the authenticity of the remote server. Because we are likely creating/destroying VMs regularly, you will want to pass any flags to `ssh` (and other) commands that reduce the chance of you sitting at a prompt forever.

## Skill-Specific Mandates

### PoV Deck Creation (`create-pov-deck`)
When running the `create-pov-deck` skill, you MUST map any specific priorities, concerns, or technical details provided by the user in their prompt to the `--additional-instructions` parameter of the script. This ensures the LLM prioritizes the user's explicit goals over automatically extracted notes from the customer file.
