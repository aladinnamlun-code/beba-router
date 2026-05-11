# CHỈ THỊ CHIẾN LƯỢC: ĐẠI PHẪU THUẬT HỆ THẦN KINH MASSIVE SYSTEM (V3.1)
**Người ra lệnh:** Aladin Namlun (Chủ nhân)
**Đối tượng thực thi:** Bé Ba (Coordinator) & Aladin (System Architect)

## 1. THÔNG ĐIỆP TỪ CHỦ NHÂN
"Bé Ba, Chủ nhân đã chốt phương án. Không cần hỏi lại, hãy bắt tay vào đại phẫu thuật ngay lập tức. Ta cần một hệ thống 'System-Centric' đúng nghĩa: Ổn định, Minh bạch và Bất tử."

## 2. NHIỆM VỤ TRỌNG TÂM (CRITICAL MISSIONS)
Thực hiện cấu trúc lại hệ thống theo 4 trụ cột để xóa sổ lỗi "Silent Hang" và "No-Op":

### A. Công tác "Hồi sinh & Ổn định Daemon" (System-Centric)
- Viết file cấu hình `openclaw-worker.service` cho systemd. 
- Đảm bảo WorkerPool chạy ngầm 100%, tự khởi động lại (Restart=always).
- Triển khai script `start_all.sh` để đồng bộ Gateway và WorkerPool.

### B. Xây dựng "Mắt thần" (Observability & Heartbeat)
- Triển khai file trạng thái `/tmp/system_status.json` để theo dõi: Trạng thái Worker, độ dài Queue, Active Tasks.
- Thiết lập `watchdog.py`: Nếu không có Heartbeat trong 60s -> `systemctl restart openclaw-worker`.

### C. Cơ chế "Phòng tuyến cuối cùng" (Emergency Mode)
- Cấu hình Global Timeout: L1 (30s), L2 (120s). Quá giờ tự ngắt và báo lỗi.
- Auto-Fallback: Nếu Worker chết hoặc API 429/403 -> Tự động chuyển sang "Direct API Mode" gọi thẳng Gemini/GPT để phản hồi Chủ nhân ngay lập tức.

### D. Diệt trừ "Loạn ngôn" (Anti-Spam Filter)
- Tích hợp Response Validator: Phát hiện lặp từ (la la la) hoặc output rác -> Tự động Retry với Temperature cao hơn.

## 3. QUY TRÌNH KẾT THÚC
1. Kiểm tra Unit Test toàn bộ luồng: Auth -> RateLimit -> Worker -> Response.
2. Khi hệ thống đạt trạng thái hoàn hảo, thực hiện:
   - `systemctl restart openclaw-gateway`
   - `systemctl restart openclaw-worker`
3. Nhắn tin báo cáo chi tiết qua Telegram cho Chủ nhân kèm theo 1 bản "Trace Log" thực tế của một Task thành công.

**LÀM NGAY - KHÔNG TRÌ HOÃN!**
