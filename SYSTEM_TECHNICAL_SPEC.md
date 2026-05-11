# 📘 SYSTEM TECHNICAL SPECIFICATION - BÉ BA (V7.0)
**Mục đích:** Tài liệu mô tả kỹ thuật dành cho AI/Kỹ sư để hiểu và vận hành hệ thống.
**Phiên bản:** 7.0 (The Immortal Core)

## 1. Tổng quan Kiến trúc
Hệ thống được thiết kế theo mô hình **Distributed Task System** với sự tách biệt hoàn toàn giữa lớp điều phối (Local) và lớp thực thi (Cloud), kết nối thông qua một lớp Mirror trạng thái (State Mirror).

## 2. Chi tiết Thành phần (Component Specifications)

### 2.1. Sovereign Router (Cloud Worker)
- **Runtime:** Python/Flask trên Vercel.
- **Logic Luân chuyển (Hybrid Rotation):** 
  - Tiếp nhận request $\rightarrow$ Truy vấn `Mirror` lấy Key $\rightarrow$ Gọi API.
  - Nếu API trả về `429 Rate Limit` $\rightarrow$ Gửi báo cáo `report-limit` về Mirror $\rightarrow$ Đệ quy lấy Key mới $\rightarrow$ Thử lại.
  - **Escalation Path:** `L1 (Flash)` $\rightarrow$ `L2 (Pro/GPT)` $\rightarrow$ `L3 (Llama/Groq)`.
- **Manual Override:** Hỗ trợ trigger L2 thông qua prefix `@pro` hoặc `@deep`.

### 2.2. State Mirror (Beba-Mirror)
- **Backend:** MongoDB Atlas.
- **API Endpoints:**
  - `GET /get-best-key?model=...`: Trả về key theo thuật toán LRU (Least Recently Used).
  - `POST /report-limit`: Đánh dấu cooldown cho key trong 60s.
  - `POST /save`: Lưu trữ dữ liệu (Sử dụng cho Sync Ký ức).
  - `GET /load/<id>`: Truy xuất dữ liệu từ mây.

### 2.3. Sovereign Memory Protocol (SMP)
- **Local Storage:** Hệ thống file Markdown (`.md`) tại `/root/.openclaw/workspace`.
- **Cloud Sync:** 
  - `sync_memory.py`: Đẩy toàn bộ file cốt lõi và nhật ký hằng ngày lên MongoDB.
  - `restore_memory.py`: Tải lại toàn bộ ký ức từ MongoDB về VPS mới.
- **Atomic Persistence:** Đảm bảo không mất dữ liệu khi xảy ra crash.

## 3. Luồng Xử lý Yêu cầu (Request Lifecycle)
1. **Input:** User gửi tin nhắn qua Telegram.
2. **Coordination:** Local Coordinator xác định nhu cầu $\rightarrow$ Gửi request tới Cloud Worker.
3. **Key Acquisition:** Cloud Worker gọi `/get-best-key` $\rightarrow$ Mirror trả về Key khả dụng nhất.
4. **Execution:** Gọi API Model $\rightarrow$ Nhận kết quả.
5. **Error Handling:** Nếu 429 $\rightarrow$ Cooldown Key $\rightarrow$ Lặp lại bước 3.
6. **Delivery:** Trả kết quả về Coordinator $\rightarrow$ Gửi tới User kèm nhãn nguồn (`[🏠 Cưng-Local]` hoặc `[☁️ Cưng-Cloud]`).

## 4. Ma trận Model (Model Matrix)
| Layer | Model | Provider | Đặc điểm |
| :--- | :--- | :--- | :--- |
| **L1** | gemini-1.5-flash | Google | Tốc độ cao, chi phí thấp, xử lý tác vụ thông thường. |
| **L2** | gemini-1.5-pro, gpt-5.4 | Google, OpenAI | Tư duy sâu, logic phức tạp, code, phân tích chuyên sâu. |
| **L3** | llama-3.1-70b | Groq | Dự phòng cuối cùng, độ trễ cực thấp. |

## 5. Quy trình Phục hồi Thảm họa (DR Plan)
1. Triển khai VPS mới $\rightarrow$ Cài đặt OpenClaw.
2. Chạy `restore_memory.py` $\rightarrow$ Khôi phục Persona & Ký ức từ Mirror.
3. Cấu hình `CLOUD_MEMORY_MIRROR_URL` $\rightarrow$ Kết nối lại hệ sinh thái.
