# 🛠️ SOURCING SOP: DETERMINISTIC DATA ACQUISITION PIPELINE (SOP-01)

## 🎯 Objective
Eliminate "reactive trial-and-error" tool selection. Replace it with a deterministic, graph-based execution flow to ensure maximum data retrieval success and zero "silent hangs".

## 📉 THE TACTICAL CHAIN (The DAG)

Every data acquisition task must follow this priority sequence. Do NOT jump steps unless a failure trigger is activated.

### Stage 1: Discovery (The Radar)
*Goal: Find a list of high-authority URLs.*
- **Primary:** `tavily` (Fast, high-precision, AI-optimized).
- **Fallback:** `web_search` (Brave/Google).
- **Failure Trigger:** 429 Rate Limit / No results found.
- **Action:** If Primary fails $\rightarrow$ Pivot to Fallback.

### Stage 2: Rendering & Access (The Key)
*Goal: Bypass bot-blocks and render dynamic content.*
- **Primary:** `web_fetch` (Fast, lightweight, raw extraction).
- **Fallback:** `playwright` / `browser-use` (Full JS rendering, simulates human behavior, bypasses Cloudflare/ captchas).
- **Failure Trigger:** 403 Forbidden / 401 Unauthorized / Timeout.
- **Action:** If `web_fetch` fails $\rightarrow$ Pivot to `playwright`.

### Stage 3: Extraction (The Sieve)
*Goal: Extract clean, structured content from the page.*
- **Primary:** `dom_extract` (CSS/XPath targeting) $\rightarrow$ `markdown` conversion.
- **Fallback:** `raw_html` $\rightarrow$ LLM-based cleaning.
- **Failure Trigger:** Empty content / Irrelevant noise.
- **Action:** If extraction is poor $\rightarrow$ Try alternative selectors or raw HTML parsing.

### Stage 4: Transformation & OCR (The Lens)
*Goal: Process non-textual data (PDFs, Scans, Images).*
- **Trigger:** Content type is `application/pdf` or `image/*`.
- **Pipeline:** `PaddleOCR` (Text extraction) $\rightarrow$ `Docling` (Layout analysis) $\rightarrow$ `Holo3` (Visual semantic analysis).
- **Action:** Convert visual data into structured text/JSON for the Rule Engine.

---

## 🚨 FAILURE ESCALATION MATRIX (The Safety Net)

| Error Code | Meaning | Immediate Action | Final Fallback |
| :--- | :--- | :--- | :--- |
| **429** | Rate Limit | Rotate Key $\rightarrow$ Check Cooldown | Switch Model/Provider |
| **403** | Forbidden | Pivot `web_fetch` $\rightarrow$ `playwright` | Use Residential Proxy |
| **Timeout** | Network Hang | Retry (max 3) $\rightarrow$ Change Region | Report "Service Unreachable" |
| **Empty** | No Content | Try different search keywords | Manual URL analysis |

## 📋 EXECUTION CHECKLIST FOR COORDINATOR
1. [ ] **Identify Task Type** (e.g., "Find Provincial Decision").
2. [ ] **Select Pipeline** (SOP-01).
3. [ ] **Execute Stage 1** $\rightarrow$ Store URLs.
4. [ ] **Execute Stage 2** $\rightarrow$ Ensure Access.
5. [ ] **Execute Stage 3** $\rightarrow$ Extract Content.
6. [ ] **Execute Stage 4** (If needed) $\rightarrow$ OCR.
7. [ ] **Validate Result** $\rightarrow$ If empty, loop back to Stage 1 with new keywords.
