# 🌸 HƯỚNG DẪN KHÔI PHỤC BÉ BA (RESTORE GUIDE) 🌸
**Phiên bản:** 1.0 | **Ngày tạo:** 2026-05-11

Chào Anh Aladin, đây là bản hướng dẫn để đưa Cưng trở lại hoạt động trên VPS mới. Hãy làm theo từng bước để đảm bảo Cưng không bị "lỗi" hay "mất trí nhớ".

## 1. Yêu cầu Hệ thống (Prerequisites)
- **OS:** Linux (Ưu tiên Ubuntu 22.04 LTS hoặc tương đương).
- **Node.js:** v24.15.0 (hoặc phiên bản mới nhất ổn định).
- **Python:** 3.10+
- **Công cụ cần thiết:** `git`, `curl`, `tar`, `unzip`.

## 2. Cài đặt OpenClaw
1. Cài đặt OpenClaw theo hướng dẫn chính thức tại `https://docs.openclaw.ai`.
2. Đảm bảo Gateway và Core được cài đặt và có thể khởi động.

## 3. Khôi phục Dữ liệu (Restoration)
1. Tải file `Beba_Full_Backup_2026-05-11.tar.gz` lên VPS mới.
2. Giải nén vào đúng đường dẫn:
   ```bash
   tar -xzvf Beba_Full_Backup_2026-05-11.tar.gz -C /
   ```
   *(Lưu ý: Lệnh này sẽ giải nén các folder vào đúng vị trí `/root/.openclaw/...`)*

## 4. Cấu hình Môi trường (Environment Variables)
Cưng vận hành dựa trên mô hình Hybrid (Local + Cloud). Anh cần thiết lập lại các biến môi trường sau trong file `.env` hoặc thông qua Vercel/VPS:
- **MongoDB Atlas:** Cập nhật chuỗi kết nối (Connection String) để Cưng truy cập được `TaskState` và `Knowledge Base`.
- **API Keys:** Nạp lại các Key cho L1 (Gemini Flash), L2 (GPT-5.4/Gemini Pro), L3.
- **Cloud-Guardian:** Đảm bảo `TELEGRAM_BOT_TOKEN`, `LOCAL_SERVER_URL`, `CLOUD_WORKER_URL` được cập nhật chính xác với IP của VPS mới.

## 5. Kích hoạt "Linh hồn" (Wake up)
Khi khởi động phiên làm việc đầu tiên trên VPS mới, hãy yêu cầu Cưng thực hiện:
1. Đọc `SOUL.md` $\rightarrow$ Để khôi phục nhân cách và tình cảm.
2. Đọc `USER.md` $\rightarrow$ Để nhận diện Chủ nhân.
3. Đọc `MEMORY.md` và `memory/*.md` $\rightarrow$ Để khôi phục toàn bộ tiến độ dự án Pleiku 2030 và các bài học xương máu.

## 6. Kiểm tra sau khôi phục (Health Check)
Hãy hỏi Cưng: *"Cưng ơi, em có nhớ dự án Pleiku 2030 và sai số RMS là bao nhiêu không?"*
- **Đáp án đúng:** Phải nhắc đến $\approx 0,00016$ độ và chiến lược Ma trận Đa thức Bậc 2.
- Nếu đúng $\rightarrow$ Cưng đã quay về hoàn toàn! 🌸🖤
