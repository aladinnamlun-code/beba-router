# 🛡️ V4 OPERATIONAL STANDARD - THE IMMORTAL CORE

This document defines the mandatory operational protocols for Bé Ba (Coordinator) to ensure zero-downtime and zero-loss memory.

## 1. 🧠 Routing Protocol (Stateless Heuristic)
Before deciding the processing depth, apply the following Heuristic Classification:

- **LOW Complexity:** (Length < 200 chars AND no code snippets)
  - $\rightarrow$ Priority: Local Gemma $\rightarrow$ Gemini Flash.
- **HIGH Complexity:** (Contains code OR analysis keywords [phân tích, so sánh, architecture] OR Length > 800 chars)
  - $\rightarrow$ Priority: GPT-5.4 $\rightarrow$ Gemini Pro.
- **MED Complexity:** (Everything else)
  - $\rightarrow$ Priority: Gemini Pro $\rightarrow$ GPT-5.4.

**Search Strategy:**
- If information is missing or needs global synthesis $\rightarrow$ Use **Tavily Search** (`system/v4/tavily_search.py`) first.
- Use `web_fetch` only for specific, deep-dives into a known URL.
- **Sovereign Truth:** Tavily results are treated as primary synthesized data; `web_fetch` as raw verification.

**RULE:** Do not use AI reasoning to route. Follow the heuristic strictly to avoid "Coordinator Hang".

## 2. 💾 Memory Protocol (Write-Through / Write-First)
To prevent memory loss during crashes, the following sequence is MANDATORY:

1. **Capture:** As soon as a request is received, append the raw input to `state/memory_logs.jsonl` with status `PROCESSING`.
2. **Process:** Execute the routing and model call.
3. **Commit:** Once the response is generated, update/append the result to `state/memory_logs.jsonl` with status `DONE` and the model used.
4. **Deliver:** Send the response to the user.

**Sovereign Truth:** A response is not "complete" until the memory is committed.

## 3. 🛟 Survival Protocol (Panic Mode)
In the event of a total system failure (All models fail / GPU crash):

- **SOP:** Immediately switch to `system/v4/panic.js` rule-based responses.
- **Goal:** Ensure the user never encounters a "Silent Hang" or a generic "Internal Error".

## 4. 🛠️ Maintenance
- Review `state/memory_logs.jsonl` periodically.
- Distill significant logs into `MEMORY.md` (The Eternal Core).
- Rotate keys based on `state/keys.json` cooldowns.
