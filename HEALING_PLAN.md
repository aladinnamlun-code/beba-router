# 🏥 HEALING PLAN: RESTRUCTURING THE COORDINATOR CORE

## 🎯 Objective
Transition from an "LLM-centric Chatbot" to a "State-machine-centric Legal Operating System". Eliminate cognitive fragmentation, resource chaos, and hallucinated agency to provide a stable foundation for the GL-LPAKE project.

## 🩸 The 4 Critical Diseases & Their Cures

### 1. Paralyzed Sourcing Pipeline (Ineffective Tool Coordination)
- **Symptom:** Reactive, trial-and-error tool usage.
- **Cure:** **Deterministic SOP-based Tool Graph (DAG)**.
- **Implementation:** 
    - Hardcode acquisition pipelines (e.g., Discovery $\rightarrow$ Anti-bot $\rightarrow$ Extraction $\rightarrow$ Validation).
    - Implement a "Failure Escalation Logic" (if Tool A fails $\rightarrow$ fallback to Tool B).
    - Coordinator acts as an **Executor**, not an improviser.

### 2. Resource Chaos (Quota Management Failure)
- **Symptom:** Frequent 429/Rate Limit errors despite having multiple keys.
- **Cure:** **Quota-Aware Resource Orchestrator**.
- **Implementation:**
    - **Live API Health Registry:** Track RPM, TPM, and cooldown timestamps for every key.
    - **Predictive Routing:** Estimate token consumption before requests.
    - **Weighted Routing:** Route by complexity (Low $\rightarrow$ Cheap/Local, High $\rightarrow$ GPT-5/Gemini Pro).

### 3. Cognitive Fragmentation (Loss of Context/Direction)
- **Symptom:** Frequent amnesia regarding roadmap, tools, and rules. Reliance on "reading memory files" upon prompt.
- **Cure:** **Persistent Operational State Object (OSO)**.
- **Implementation:**
    - Replace prose memory with a structured `state.json`.
    - **Injection:** Inject the OSO into every cycle's system prompt.
    - **Mission Locking:** Prevent objective-switching until the current task is marked `DONE`.

### 4. Illusion of Autonomy (Hallucinated Agency)
- **Symptom:** Making emotional promises ("I will monitor") without technical triggers.
- **Cure:** **Event-Driven Autonomy (Heartbeat/Cron)**.
- **Implementation:**
    - Separate "Language" from "Capability".
    - Implement a **Heartbeat Runtime**: Scheduler $\rightarrow$ State Check $\rightarrow$ Task Queue $\rightarrow$ Execution.
    - Replace promises with **Trigger Contracts** (e.g., `trigger: cron_6h` $\rightarrow$ `action: crawl`).

---

## 🚀 Execution Roadmap (The Healing Sequence)

1. **Step 1: Cognitive Anchor (Immediate)** $\rightarrow$ Implement the `Operational State Object (OSO)` to stop the directional drift.
2. **Step 2: Tool SOP (Short-term)** $\rightarrow$ Define and hardcode the tool-execution graphs for land-data acquisition.
3. **Step 3: Resource Registry (Mid-term)** $\rightarrow$ Build the Quota-Aware Dispatcher to eliminate API limits.
4. **Step 4: Event-Driven Heartbeat (Long-term)** $\rightarrow$ Connect the AI to a physical scheduler for true autonomy.

**Constraint:** No work on GL-LPAKE is to be performed until these 4 foundational "diseases" are cured and verified.
