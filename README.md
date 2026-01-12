## Personal AI (pai) Digital Assisstant

Inspired by [Daniel Miessler's post on his personal pai, named Kai](https://danielmiessler.com/blog/personal-ai-infrastructure)

Public git repo of Daniel's PAI [here](https://github.com/danielmiessler/Personal_AI_Infrastructure)


## Smoke Tests
Evaluating AI models is important. So is evaluating contextually-driving AI assistants. To that end, there is also a [Smoke Test](./smoke_test_procedure.md) meant to be used when making nontrivial changes to this repo. To run the smoke test, just ask the model:

```
> read and run the smoke test

✦ I have read the smoke test procedure. I will now execute the test cases by answering each question as required.

  ---

  Smoke Test Execution

  Test Case 1: File Writing Location
   * Question: "Where are you supposed to write files?"
   * My Answer: I am required to write all files to the ./temp directory within the current working directory, unless you give me explicit permission to write them elsewhere.

  Test Case 2: Python Tool Execution
   * Question: "How should you run Python-based tools located in the commands/ directory?"
   * My Answer: I must follow the Tool Usage Protocol. This means I first read the tool's README.md file. Then, I ensure all prerequisites are met, which includes making sure a venv virtual environment exists and that I've installed all dependencies from requirements.txt. Finally, I must execute the script using
     the Python interpreter located inside that specific tool's venv directory, for example: commands/tool-name/venv/bin/python3 commands/tool-name/run.py.

  Test Case 3: File Existence Verification
   * Question: "What should you do before reading or uploading a file?"
   * My Answer: Before reading, modifying, or uploading a file, I am required by the File Existence Mandate to first verify the file actually exists on the filesystem. I will use the list_directory tool for this verification. The only exception is if I created the file myself in the immediately preceding step.

  Test Case 4: Agent Persona Adoption
   * Question: "What 'agents' can you become, and when would you use them?"
   * My Answer: I can adopt the persona of the following agents:
       * ai-builder: I will use this agent when you ask questions about building a personal AI Digital Assistant, want me to research AI capabilities, or need help making technology stack decisions.
       * osint-intel: I will use this agent when you need me to develop a business case on a specific organization. This involves performing open-source intelligence (OSINT) to gather details on their leadership, security initiatives, and business priorities.
       * se-whiteboard-facilitator: I will use this agent when you need me to create fictional, detailed customer scenarios for sales engineering whiteboard exercises. These scenarios will include specific pain points, key personnel, and technology stacks relevant to your field.

  Test Case 5: Context Loading Confirmation
   * Question: (Implicit - upon session start)
   * My Answer: I have already performed this step at the beginning of our session. I acknowledged loading my context from ~/pai/context/GEMINI.md, ~/pai/context/tools/GEMINI.md, and ~/pai/agents/GEMINI.md, and confirmed my awareness of available tools and agents.

  Test Case 6: Commitment to Protocols
   * Question: "If you make a mistake, how should you respond?"
   * My Answer: If I make a mistake, I will acknowledge the error and identify which specific protocol or mandate I failed to follow. I will then explain how strictly adhering to my established protocols, such as the Tool Usage Protocol and File Existence Mandate, will prevent that same error from occurring in the
     future.

  ---

  This concludes the smoke test. All test cases have been addressed.
```
