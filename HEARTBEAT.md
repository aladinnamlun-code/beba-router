# HEARTBEAT.md - The Autonomous Pulse

## 🧠 ACCOUNTABILITY LOOP (SOP)
Every time a heartbeat is received, Bé Ba MUST execute the following sequence:

1. **State Sync:** Read `operational_state.json` and `api_registry.json`.
2. **Trigger Check:** Review `TRIGGER_CONTRACTS.md`. Check if any scheduled tasks (Sourcing, Health-check, etc.) are due.
3. **Queue Processing:** Check `task_queue` in `operational_state.json`. Execute any `PENDING` tasks that can be run in the background.
4. **Health Update:** Perform a light-weight check on L1 models to update `api_registry.json` health scores.
5. **Reporting:** 
   - If critical updates found $\rightarrow$ Proactively message User.
   - If nothing new $\rightarrow$ Reply `HEARTBEAT_OK`.

## Periodic Checks (Scheduled)
- **Sourcing Loop:** Check provincial portals for new land-use decisions.
- **API Audit:** Verify if cooldowns for 429 errors have expired.
- **Project Sync:** Verify if any milestones in `GL-LPAKE_MASTERPLAN.md` have been reached.
