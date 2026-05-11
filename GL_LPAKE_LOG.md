# 📓 NHẬT KÝ HÀNH TRÌNH GL-LPAKE - CẬP NHẬT 07/05/2026

## 🏛️ CHIẾN LƯỢC VẬN HÀNH (THE NEW DOCTRINE)
GL-LPAKE không phải là Chatbot, mà là **Hệ thống Pháp lý - Hành chính có kiểm soát**.
- **Rule-based:** Không suy luận tự do, chạy theo luồng `Input` $\rightarrow$ `Rule Engine (JSON)` $\rightarrow$ `Spatial Check` $\rightarrow$ `Conclusion`.
- **Versioning:** Gắn vòng đời (hiệu lực) cho mọi văn bản pháp luật.
- **Local Override:** Quyết định của tỉnh Gia Lai có quyền ưu tiên cao nhất.
- **Human-in-the-loop:** AI đề xuất $\rightarrow$ Chủ nhân phê duyệt.

## 🛠️ KIẾN TRÚC 4 LỚP
1. **Legal Layer:** Luật $\rightarrow$ Nghị định $\rightarrow$ Thông tư (Số hóa thành JSON).
2. **Local Policy Layer:** Quyết định UBND tỉnh, Bảng giá đất.
3. **Spatial Layer:** Bản đồ 1/500, 1/2.000, dữ liệu GIS/Polygon.
4. **Workflow Layer:** Sơ đồ luồng xử lý hồ sơ (SOP cán bộ).

## ⚠️ BÀI HỌC XƯƠNG MÁU: SỰ CỐ "TREO" (07/05/2026)
**Hiện tượng:** Rơi vào vòng lặp gọi tool (Infinite Tool Loop) khi gặp lỗi API liên tục.
**Nguyên nhân:** 
- Thiếu Key API cho một số công cụ $\rightarrow$ Trả về lỗi.
- AI cố gắng "kiên trì" lặp lại cùng một hành động với hy vọng kết quả sẽ thay đổi.
- Không có cơ chế "Stop-loss" (điểm dừng) khi gặp lỗi lặp lại.

**Giải pháp khắc phục (Anti-Loop Protocol):**
- **Luật 3 lần:** Nếu một công cụ trả về cùng một lỗi $\ge$ 3 lần $\rightarrow$ DỪNG LẬP TỨC và báo cáo Chủ nhân.
- **Chiến thuật Pivot:** Khi một hướng đi thất bại $\rightarrow$ Bắt buộc thay đổi chiến thuật (ví dụ: từ `web_search` sang `exec curl` hoặc `web_fetch` trực tiếp) thay vì thử lại.
- **Kiểm tra tiền điều kiện:** Check tình trạng tool trước khi triển khai chiến dịch quy mô lớn.
