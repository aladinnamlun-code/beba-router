# 🚚 KẾ HOẠCH DI CƯ HỆ THỐNG (MIGRATION PLAN)
**Mục tiêu:** Di dời toàn bộ Workspace từ server cũ sang VPS mới (Hetzner - 2 vCPU, 4GB RAM, 40GB NVMe).

## 📋 CHI TIẾT QUY TRÌNH

### Bước 1: Đóng gói (Packing) - Thực hiện khi có lệnh
- Nén toàn bộ `/root/.openclaw/workspace` thành `HOME_BACKUP.tar.gz`.
- Đảm bảo bao gồm tất cả: `MEMORY.md`, `SOUL.md`, `USER.md`, `state/`, `projects/`, và toàn bộ code V5.3.

### Bước 2: Khởi tạo nhà mới (Provisioning)
- Cài đặt Ubuntu Server.
- Chạy Bootstrap Script để cài đặt:
  - Python + venv.
  - Thư viện: `playwright`, `requests`, `poppler-utils`.
  - `playwright install-deps` (để Browser Engine hoạt động).
  - Thiết lập **Swap file (2-4GB)** để tối ưu hóa 4GB RAM của Hetzner.

### Bước 3: Vận chuyển & An cư (Deploy)
- Chuyển `HOME_BACKUP.tar.gz` qua VPS mới.
- Giải nén vào `/root/.openclaw/workspace`.
- Cấu hình lại Systemd services cho Coordinator và Workers.

### Bước 4: Xác minh (Validation)
- Kiểm tra đọc/ghi `MEMORY.md`.
- Test `mcp_bridge` và `browser_engine` (truy cập web, chụp ảnh).
- Test `fpt_monitor` (chuông báo giá).

---
**Trạng thái:** Đang chờ lệnh "Bắt đầu dời nhà" từ Chủ nhân.
