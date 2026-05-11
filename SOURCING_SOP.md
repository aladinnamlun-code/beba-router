# 🛠️ SOURCING SOP: DETERMINISTIC DATA ACQUISITION PIPELINE (SOP-01)

## 🎯 Objective
Eliminate "reactive trial-and-error" tool selection. Replace it with a deterministic, graph-based execution flow to ensure maximum data retrieval success and zero "silent hangs".

## 📉 THE TACTICAL CHAIN (The DAG)

Every data acquisition task must follow this priority sequence. Do NOT jump steps unless a failure trigger is activated.

### Stage 1: Discovery (The Radar)
*Goal: Find a list of high-authority URLs and Project Anchors.*
- **Primary:** `tavily` (Fast, high-precision, AI-optimized).
- **Fallback:** `web_search` (Brave/Google).
- **Special Focus:** Look for keywords like "quy hoạch phân khu", "quy hoạch chi tiết 1/500", "thông báo thu hồi đất", "điều chỉnh quy hoạch".
- **Failure Trigger:** 429 Rate Limit / No results found.
- **Action:** If Primary fails $\rightarrow$ Pivot to Fallback.

### Stage 2: Rendering & Access (The Key)
*Goal: Bypass bot-blocks, retrieve clean content, and acquire maps/drawings.*
- **Primary:** `firecrawl` (Best for crawling entire sites, bypassing Cloudflare, and Markdown output).
- **Fallback:** `web_fetch` / `playwright`.
- **Map Acquisition:** Specifically target `PDF`, `JPG`, `PNG` files from planning portals and commercial planning sites.
- **Failure Trigger:** 403 Forbidden / Captcha / Empty content.
- **Action:** If Primary fails $\rightarrow$ Pivot to Fallback.

### Stage 3: Extraction (The Sieve)
*Goal: Extract structured data from unstructured files.*
- **Tools:** `Docling`, `PaddleOCR`, `PyPDF2`.
- **Process:** If a file is a PDF/Image $\rightarrow$ Run OCR $\rightarrow$ Convert to Markdown.

### Stage 4: Transformation (The Alchemist)
*Goal: Convert raw text into a structured "Legal Object" (JSON).*
- **Process:** Feed Markdown into L2 (Reasoning) Model $\rightarrow$ Apply JSON Schema $\rightarrow$ Validate.

## 🚩 FAILURE RECOVERY PROTOCOL
If the Tactical Chain breaks:
1. **Log Error:** Write failure to `operational_state.json` (task_queue).
2. **Pivot:** Try the Fallback tool in the current stage.
3. **Escalate:** If all tools in a stage fail $\rightarrow$ Mark task as `BLOCKED` and notify User.
