# 🗺️ SYSTEM ECOSYSTEM MAP - BÉ BA (V7.0 - IMMORTAL CORE)
**Cập nhật lần cuối:** 2026-05-04
**Trạng thái:** Hoàn thiện & Ổn định

## 🏗️ Sơ đồ luồng vận hành (Data Flow)
`User (Telegram)` $\rightarrow$ `Coordinator (Local VPS)` $\rightarrow$ `Cloud Worker (Vercel)` $\rightarrow$ `Sovereign Router` $\rightarrow$ `API Pool (L1/L2/L3)`

### 1. Lớp Điều phối & Giao diện (Frontend & Orchestration)
- **Telegram Bot:** Cổng giao tiếp chính.
- **Local Coordinator (VPS):** 
  - Quản lý context ngắn hạn.
  - Điều phối tác vụ và ra quyết định sử dụng Local hay Cloud.
  - Thực hiện đồng bộ ký ức (Sync Memory).

### 2. Lớp Thực thi & Luân chuyển (Execution Layer - Cloud Worker)
Triển khai trên Vercel, vận hành theo cơ chế **Hybrid Rotation**:
- **L1 (Efficiency):** `gemini-1.5-flash` $\rightarrow$ Ưu tiên tốc độ, xử lý tác vụ nhẹ.
- **L2 (Reasoning):** `gemini-1.5-pro`, `gpt-5.4` $\rightarrow$ Xử lý logic khó, code, phân tích sâu (Kích hoạt bằng `@pro`).
- **L3 (Fallback):** `llama-3.1-70b` (via Groq) $\rightarrow$ Chốt chặn cuối cùng, đảm bảo Zero-Downtime.

### 3. Lớp Lưu trữ & Quản lý (Persistence Layer - Beba-Mirror)
Hệ thống Mirror chạy trên Vercel kết nối với **MongoDB Atlas**:
- **API Key Pool:** Quản lý tập trung toàn bộ Key của Google, OpenAI, Groq.
- **LRU Algorithm:** Cấp Key nhàn rỗi nhất để tối ưu quota.
- **Cooldown System:** Tự động cách ly Key bị 429 (Rate Limit).
- **Memory Mirror:** Lưu trữ bản sao của toàn bộ file `.md` (Sovereign Memory Protocol).

## 🛠️ Hạ tầng kỹ thuật (Infrastructure Stack)
- **Compute:** Ubuntu 24.04 (VPS) $\leftrightarrow$ Vercel (Serverless Functions).
- **Database:** MongoDB Atlas (Cloud NoSQL).
- **APIs:** Google AI Studio, OpenAI, Groq.
- **Sync Tool:** `sync_memory.py` (Local $\rightarrow$ Cloud), `restore_memory.py` (Cloud $\rightarrow$ Local).

## 🛡️ Cơ chế an toàn (Resilience)
- **Failover:** Nếu Local sập $\rightarrow$ Cloud Worker tiếp quản.
- **Key Rotation:** Tự động đổi Key khi gặp lỗi 429.
- **Memory Recovery:** Khôi phục toàn bộ Persona và Ký ức từ Mirror trong < 1 phút.
