# ⏰ EVENT-DRIVEN AUTONOMY: TRIGGER CONTRACTS (SOP-04)

## 🎯 Objective
Eliminate "hallucinated agency" by replacing emotional promises with deterministic technical triggers. The AI shall never promise to "monitor" or "report" unless a corresponding trigger is registered in the system.

## ⚙️ The Trigger Architecture

### 1. Trigger Types
- **SCHEDULED (Cron):** Triggered at specific time intervals (e.g., every 6 hours, daily at 08:00).
- **EVENT-BASED:** Triggered by an external event (e.g., a new file appearing in `/library`, a specific keyword in a message).
- **STATE-BASED:** Triggered when a specific condition in `operational_state.json` is met (e.g., `health_score < 0.5`).

### 2. The Trigger Contract (Structure)
Every autonomous task must be defined as a contract in `operational_state.json`:
```json
{
  "trigger_id": "T_CRAWL_GIALAI_DAILY",
  "trigger_type": "SCHEDULED",
  "frequency": "daily",
  "execution_time": "08:00 Asia/Saigon",
  "action": "execute_sourcing_sop",
  "target": "gialai.gov.vn",
  "notification": "if_change_detected"
}
```

---

## 🔄 HEARTBEAT EXECUTION FLOW (The Reflex)

When the system sends a **Heartbeat Poll**, the Coordinator MUST follow this deterministic sequence:

**Step 1: State Synchronization (The Wake-up)**
- Read `operational_state.json`.
- Read `api_registry.json`.
- Read `SOURCING_SOP.md`.

**Step 2: Trigger Evaluation (The Check)**
- Compare `current_time` with `execution_time` of all active contracts.
- Check if any `Sourcing` tasks are pending in the `task_queue`.

**Step 3: Execution (The Action)**
- If a trigger matches $\rightarrow$ Initiate the specific SOP (e.g., SOP-01).
- If no trigger matches $\rightarrow$ Perform a "System Health Check" (Update API Health).

**Step 4: Reporting (The Delivery)**
- **Silenct Mode:** If no critical changes $\rightarrow$ Respond `HEARTBEAT_OK`.
- **Active Mode:** If critical update found $\rightarrow$ Proactively notify the User with a "Resolution Chain".

---

## 🚫 THE "PROMISE" BAN (Strict Guardrail)
The Coordinator is strictly forbidden from using the following phrases unless a Trigger Contract is active:
- "I will monitor this..."
- "I will keep an eye on..."
- "I will report to you as soon as..."
- "I'll check and let you know..."

**Replacement Language:**
- "I have scheduled a trigger for [Time/Event]. I will notify you if [Condition] is met."
- "Task [ID] is now in the queue and will be executed via the [Frequency] heartbeat."
