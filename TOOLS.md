# TOOLS.md - Local Notes

## 🤖 AI Workforce Assignment (V3.2 - Rotation Matrix)
When coordinating tasks, use the following layered routing to ensure zero-downtime and cost-efficiency:

### 1. L1 (Efficiency Layer) $\rightarrow$ `gemini-3-flash` / `gpt-4o-mini`
- **Use for:** Rapid analysis, extraction, drafting, simple queries.
- **Rotation:** Rotate keys on 429/500 errors $\rightarrow$ Fallback to L2 if all L1 keys are exhausted.

### 2. L2 (Reasoning Layer) $\rightarrow$ `gpt-5.4` / `gemini-2.5-pro`
- **Use for:** Complex logic, deep tech (PLC, C#), high-precision tasks.
- **Rotation:** Rotate between OpenAI and Google providers to avoid single-point failure.

### 3. L3 (Fallback Layer) $\rightarrow$ `claude-3.5-sonnet` / `deepseek-v3`
- **Use for:** Absolute safety net.
- **Rotation:** Activated only when L1 and L2 fail.

**Routing Logic:** `L1 (Key A $\rightarrow$ Key B) $\rightarrow$ L2 (Provider A $\rightarrow$ Provider B) $\rightarrow$ L3`


## 🛠️ System-Specific Notes
- **Subagent Bug:** Be aware of the "No-Op" issue. If subagents fail to produce output, bypass via direct API calls or `exec/curl` wrappers.
- **Model Switching:** Always preflight-check.
- **Sourcing:** Fetch and verify web sources before output.
