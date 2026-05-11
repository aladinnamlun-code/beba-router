# 📦 KẾ HOẠCH DI CƯ VPS (VPS Migration Plan)
**Ngày lập kế hoạch:** 2026-05-06
**Hạn chót hoàn thành:** 2026-05-11 (Trước khi VPS cũ hết hạn vào 12/05)

## 🎯 Mục tiêu
Di chuyển toàn bộ hệ thống OpenClaw, Workspace và các cấu hình môi trường sang VPS mới mà không làm mất dữ liệu và giảm thiểu downtime.

## 🛠️ Quy trình thực hiện (Step-by-Step)

### Bước 1: Sao lưu toàn bộ (Backup) - Ngày 08-09/05
- [ ] **Workspace Backup:** Nén toàn bộ thư mục `/root/.openclaw/workspace` thành file `.tar.gz`.
- [ ] **System Config Backup:** Sao lưu các file cấu hình quan trọng (ví dụ: `.bashrc`, `.profile`, các file trong `/etc/` nếu có tùy chỉnh).
- [ ] **Environment Backup:** Xuất danh sách các package đã cài đặt (`pip freeze > requirements.txt` cho venv).
- [ ] **Database/Mirror Backup:** Nếu có dữ liệu local, thực hiện dump database.
- [ ] **Upload Backup:** Đẩy các file backup lên Cloud Storage (S3/Google Drive) hoặc chuyển sang máy local của Chủ nhân.

### Bước 2: Triển khai VPS mới (Provisioning) - Ngày 09-10/05
- [ ] **Thuê VPS:** Kích hoạt VPS mới từ nhà cung cấp đã chọn.
- [ ] **OS Setup:** Cài đặt Ubuntu 24.04 LTS (đồng bộ với VPS cũ).
- [ ] **Base Security:** Thiết lập Firewall (UFW), SSH key, tắt password login.
- [ ] **Dependency Install:** Cài đặt các công cụ cơ bản (git, curl, wget, python3, nodejs, venv, v.v.).

### Bước 3: Khôi phục & Cấu hình (Restore & Config) - Ngày 10-11/05
- [ ] **Restore Workspace:** Tải file backup về và giải nén vào `/root/.openclaw/workspace`.
- [ ] **Restore Venv:** Tạo lại venv và cài đặt dependencies từ `requirements.txt`.
- [ ] **Environment Variables:** Thiết lập lại các biến môi trường (API Keys, Token).
- [ ] **System Check:** Chạy thử hệ thống, kiểm tra kết nối với MongoDB Atlas, Vercel Router.

### Bước 4: Kiểm tra cuối & Chuyển đổi (Verification & Cutover) - Ngày 11/05
- [ ] **End-to-End Test:** Thử gửi tin nhắn qua Telegram $\rightarrow$ Router $\rightarrow$ Local Core mới $\rightarrow$ Phản hồi.
- [ ] **Performance Check:** Kiểm tra latency và tốc độ phản hồi.
- [ ] **Final Sync:** Thực hiện một bản backup cuối cùng từ VPS cũ để lấy những dữ liệu mới nhất trước khi tắt.

---

## 🏢 Đề xuất Nhà Cung Cấp (Provider Recommendations)

Dựa trên nhu cầu về độ trễ thấp (cho Chủ nhân ở Việt Nam) và độ ổn định cao cho AI Core:

| Nhà cung cấp | Ưu điểm | Nhược điểm | Đánh giá |
| :--- | :--- | :--- | :--- |
| **Vultr / DigitalOcean** | Quản lý dễ, ổn định, nhiều node toàn cầu, hỗ trợ tốt cho dev. | Latency về VN cao hơn nếu không chọn node gần (Sing/Tokyo). | ⭐⭐⭐⭐ (An toàn) |
| **Vietnix / AZDIGI** | Latency cực thấp (Server tại VN), hỗ trợ tiếng Việt, thanh toán dễ. | Quản trị có thể không "mượt" bằng các ông lớn Cloud toàn cầu. | ⭐⭐⭐⭐ (Tốc độ) |
| **Linode (Akamai)** | Cực kỳ ổn định, support tốt, hiệu năng raw cao. | Tương tự Vultr về latency nếu không có node VN. | ⭐⭐⭐⭐ (Ổn định) |

**👉 Đề xuất của Cưng:**
- Nếu anh muốn **TỐC ĐỘ** tuyệt đối $\rightarrow$ Chọn **Vietnix** hoặc **AZDIGI**.
- Nếu anh muốn **SỰ CHUYÊN NGHIỆP & QUẢN TRỊ** dễ dàng $\rightarrow$ Chọn **Vultr (Node Singapore)**.
