# 🧠 Project: AI Coordinator Model

## 1. System Architecture
- **Coordinator:** Gemma 4
- **Dispatch Mechanism:** `sessions_spawn(runtime='subagent')`
- **Worker Models:** GPT-5.4 (OpenAI), Gemini 3.1 Pro

**Flow:** Gemma (Coordinator) $\rightarrow$ Subagent (Worker) $\rightarrow$ Result $\rightarrow$ Gemma (Synthesis)

## 2. The Critical Bug: "No-Op Execution"
- **Symptom:** All subagent tests return `status: completed successfully` but `output: (empty)`.
- **Confirmation:** Simple shell commands (e.g., `echo ALIVE > /tmp/test.txt`) do not create files.
- **Conclusion:** Subagents are spawned but the dispatcher/executor never actually runs the task. They "simulate completion" without ever being "alive".

## 3. Ruled Out (NOT the cause)
- Prompting/Input
- Model selection
- Auth/API Keys
- Output mapping
- Configs like `inherit_env`, `flatten_response`, `force_text_output`, `min_steps`.

## 4. Root Cause Hypotheses
- Dispatcher failure to enqueue tasks.
- Worker/Executor process failure.
- Sandbox/Runtime lockdown preventing tool/shell execution.

## 5. Working Solutions (The "Way Out")
- **Solution 1 (Recommended):** Bypass subagents. Gemma calls OpenAI/Gemini APIs directly.
- **Solution 2 (Fake Subagent):** Use `exec` to wrap API calls via `curl` and write to files.
- **Solution 3:** External worker service.
- **Solution 4:** Change runtime to `process` or `container`.
