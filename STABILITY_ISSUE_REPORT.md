# 🚨 TECHNICAL INCIDENT REPORT: INTERMITTENT 500 ERRORS & HANGING

**Target Expert:** GPT-5.4 (Deep Tech & Coding Expert)
**Subject:** Troubleshooting persistent 500 Internal Errors and System Hangs in the OpenClaw Worker Bridge implementation.

---

## 1. SYSTEM ARCHITECTURE
The current implementation uses a custom "Worker Bridge" to coordinate LLM calls:
`User (Telegram)` $\rightarrow$ `OpenClaw Gateway` $\rightarrow$ `Worker Bridge (Python)` $\rightarrow$ `CLI: openclaw infer model run` $\rightarrow$ `LLM Provider` $\rightarrow$ `Output Parsing` $\rightarrow$ `User`.

## 2. IMPLEMENTED FIXES (The "Stability" Layer)
We have already implemented the following in `worker_bridge.py`:
- **Combined Output:** Reading both `stdout` and `stderr`.
- **Specific Parsing:** Splitting by `"outputs: 1"` to remove OpenClaw metadata.
- **Anti-Loop:** Detecting repeating lines in output to prevent infinite loops.
- **Circuit Breaker:** Temporary blocking of models that fail repeatedly.
- **Timeout & Retry:** Standard `subprocess.run` timeout of 60s and exponential backoff.
- **Context Management:** `reserveTokensFloor: 20000` in `config.yaml` to avoid context overflow.

## 3. CURRENT SYMPTOMS
Despite the above, the following persists:
- **Symptom A:** Intermittent `LLM error: { "error": { "code": 500, "message": "Internal error encountered.", "status": "INTERNAL" } }` on Telegram.
- **Symptom B:** Total "Hanging" where the agent does not respond for several minutes, even when the underlying model (checked via CLI) is healthy.
- **Observation:** The CLI command `openclaw infer model run` works perfectly in the terminal, but the same call via the `worker_bridge` occasionally triggers a 500 or a hang.

## 4. HYPOTHESES
1. **Gateway-Worker Timeout Mismatch:** The Gateway may be timing out before the `worker_bridge` finishes its `TIMEOUT = 60` or its retries, leading to a 500 error returned to the user.
2. **Blocking I/O:** The current `worker_bridge` might be blocking the main execution thread, causing other requests to queue or time out.
3. **Resource Contention:** When heavy tasks (like `video_worker` transcription) are running, the system resources may be constrained, causing the `worker_bridge` to lag or crash.
4. **Zombie Processes:** Previous failed attempts might be leaving orphaned `openclaw infer` processes that lock resources.

## 5. REQUEST FOR SOLUTION
We need a **Production-Grade Architecture** for the Worker Bridge. Please provide:
1. **Asynchronous Execution:** How to move from `subprocess.run` (blocking) to an `asyncio` based approach to prevent hanging.
2. **Robust Timeout Handling:** A synchronized timeout strategy between the Gateway, the Bridge, and the Provider.
3. **Advanced Error Mapping:** A way to differentiate between a "Provider Error" (429/500) and a "Bridge Error" (Parse failure/Timeout) to provide better feedback.
4. **Resource Isolation:** Suggestions on how to run the bridge and heavy workers (like video) without affecting the responsiveness of the main chat.

---
*Note to Expert: The goal is a system where the user never sees a "500 Internal Error" unless the provider is actually down, and where "Hanging" is mathematically impossible.*
