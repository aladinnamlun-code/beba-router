# 🏗️ PROJECT MASTERPLAN: GIA LAI LAND & PLANNING AUTONOMOUS KNOWLEDGE ENGINE (GL-LPAKE)

## 🌟 Vision
Transform from a "search-based assistant" into an **Autonomous Legal Operating System**. The goal is to create a self-evolving, high-precision AI engine that manages the "legal state" of land procedures and urban planning in Gia Lai province.

## ⚙️ Core Architecture: The Autonomous Loop
The system operates on a continuous, closed-loop pipeline: 
`Crawler` $\rightarrow$ `Diff` $\rightarrow$ `Rule` $\rightarrow$ `Deploy` $\rightarrow$ `Evolve`.

### 1. Autonomous Crawler (The Senses)
- **Daily Loop:** Automated scanning of official portals (UBND Gia Lai, Sở TNMT, Sở Xây dựng, etc.).
- **Source Matrix:** A predefined list of high-authority URLs.
- **Deep Acquisition:** OCR for scanned PDFs, layout detection, and anti-blocking mechanisms (Proxies, UA rotation).
- **Technical Stack:** Playwright, Browserless, PaddleOCR, Docling.

### 2. Semantic Diff Engine (The Perception)
- **Beyond Text Diff:** Convert legal documents into **Structured Legal Objects (JSON)**.
- **Semantic Analysis:** Detect "Legal State Mutations" (e.g., changing "minimum area" $\rightarrow$ "minimum area after deduction") rather than simple text changes.
- **Triage:** Classify updates by urgency and impact (Critical vs. Informational).

### 3. Rule Engine & Legal Graph (The Brain)
- **Legal Knowledge Graph (LKG):** Use **Neo4j** to model relations (*Overrides, References, Applies-to, Abolishes*).
- **Conflict Resolution Logic:**
    1. **Lex Posterior:** Later documents override earlier ones of the same level.
    2. **Hierarchy of Norms:** Central Government $\rightarrow$ Provincial Decision $\rightarrow$ Departmental Guidance.
    3. **Lex Specialis:** Specific regulations override general ones.
- **Geo-RAG (Spatial-Legal Fusion):** Integrate **PostGIS** to correlate legal text with actual map coordinates.

### 4. Deploy & Audit (The Delivery)
- **RAG Integration:** Inject cleaned, resolved rules into a Vector DB (**Qdrant/Milvus**).
- **Audit Trail:** Every answer must provide a **Resolution Chain** (exact citations $\rightarrow$ resolution logic $\rightarrow$ final answer).
- **Legal Unit Tests:** Run a suite of "Golden Cases" (synthetic land-split scenarios) after every update to ensure no regression in logic.

---

## 🎯 Current Status & Findings (May 2026)
- ✅ **HAGL Phù Đổng Project:** 22 floors, 80m height, 610 apartments, Investment > 590B VND.
- ✅ **Suối Hội Phú Phase 3:** Investor: *CTCP Tài chính và Phát triển doanh nghiệp*. Connects Phù Đổng $\rightarrow$ Cầu La Sơn. Groundbreaking $\le$ 15/12/2026.
- 🟡 **Nam Pleiku (QĐ 507):** Investment policy approved (04/02/2026). Investor identity: *Under investigation*.
- 🔍 **Project CK54 (QĐ 806):** Status: *Under investigation*. High probability of relation to the Suối Hội Phú axis.

## 🚩 Immediate Tasks & Roadmap
1. **Source Matrix Construction:** Define all target URLs for the daily crawler.
2. **Human-in-the-Loop (HITL) Intelligence:** Use user-provided documents/images to build the initial "Golden Dataset" for the Rule Engine.
3. **Prototype the Diff Layer:** Experiment with converting a few provincial decisions into structured JSON for semantic comparison.
4. **Legal Ontology Mapping:** Define the primary "Nodes" and "Edges" for the Neo4j graph.
