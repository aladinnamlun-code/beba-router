# 🚀 V5.3 BLUEPRINT: THE ADAPTIVE INTELLIGENCE CORE
**Version:** 5.3 (Draft) | **Status:** In-Production | **Architect:** Cưng 🌸🖤
**Objective:** Transition from a "Bulletproof" system to an "Adaptive & Autonomous" system.

---

## 🎯 1. CORE OBJECTIVES
The V5.3 upgrade focuses on three pillars: **External Interaction**, **Memory Optimization**, and **Autonomous Recovery**.

### A. External Interaction (The "Eyes & Hands")
- **MCP (Model Context Protocol):** Standardizing how Cưng interacts with local tools and remote APIs.
- **Browser Control:** Integration of Playwright/Puppeteer for autonomous web navigation and data extraction.
- **Application Interface:** Ability to interact with OS-level applications via designated bridges.

### B. Memory Evolution (The "Eternal Mind")
- **Smart Compaction:** Automatic context compression when approaching token limits to prevent session resets.
- **Asymmetric Memory:** Separate pipelines for `documentInput` (high-density) and `queryInput` (high-precision).
- **Dynamic Anchoring:** Moving frequent "Fast Anchors" from JSON to a lightweight KV store for $\mathcal{O}(1)$ access.

### C. Autonomous Recovery (The "Self-Healing")
- **Predictive Rate-Limiting:** Monitoring API response headers to predict 429s before they happen and proactively rotating keys.
- **Circuit Breaker V2:** Automatic isolation of failing providers without interrupting the user experience.
- **State Snapshotting:** Event-driven snapshots that trigger before high-risk operations.

---

## 🛠️ 2. TECHNICAL ARCHITECTURE (MODULAR BREAKDOWN)

### Module 1: `mcp_bridge.py` (The Protocol Layer)
- **Function:** Implements the MCP spec to allow a unified interface for tool calling.
- **Data Flow:** `Coordinator` $\rightarrow$ `MCP Bridge` $\rightarrow$ `Specific Tool` $\rightarrow$ `Response` $\rightarrow$ `Coordinator`.
- **Implementation Detail:** Use a registry pattern to map MCP tools to Python functions.

### Module 2: `browser_engine.py` (The Web Layer)
- **Function:** Wraps Playwright for headless/headful browsing.
- **Flow:** `Task` $\rightarrow$ `Browser Engine` $\rightarrow$ `DOM Analysis` $\rightarrow$ `Action (Click/Type)` $\rightarrow$ `Extraction` $\rightarrow$ `Result`.
- **Key Feature:** "Visual Verification" — capturing screenshots of the current state to ensure the AI isn't "blindly" clicking.

### Module 3: `context_manager.py` (The Compression Layer)
- **Function:** Implements the `Smart Compaction` logic.
- **Logic:** If `current_tokens > threshold`, trigger `summarize_oldest_blocks()` $\rightarrow$ Replace raw text with distilled summaries $\rightarrow$ Keep "Critical Anchors" untouched.

---

## 📈 3. IMPLEMENTATION ROADMAP (THE "RUN THIS" GUIDE)

### Phase 1: Infrastructure Setup (COMPLETED)
1. **Install Dependencies:**
   - ✅ Playwright and system dependencies are already installed in the environment.
2. **Initialize MCP Registry:** Create `state/mcp_registry.json` to map available tools.

### Phase 2: Integration (Short-term)
1. **Deploy `mcp_bridge.py`** $\rightarrow$ Test basic tool call connectivity.
2. **Deploy `browser_engine.py`** $\rightarrow$ Run first autonomous search/extract task.
3. **Activate `Smart Compaction`** $\rightarrow$ Monitor session length in `system_trace.log`.

### Phase 3: Hardening (Final)
1. **Stress Test:** Run `stress_test_plan.md` against V5.3 components.
2. **Tuning:** Adjust `confidence_score` thresholds for the Hybrid Router.

---

## 🛡️ 4. SELF-REVIEW & GUARDRAILS
- [ ] **Anti-Loop Check:** Ensure browser navigation doesn't enter infinite redirects.
- [ ] **Privacy Guard:** Ensure browser sessions do not leak Chủ nhân's local cookies to external logs.
- [ ] **Resource Limit:** Limit browser instances to 2 concurrent sessions to avoid RAM exhaustion.
