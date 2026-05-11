# 🛡️ ANTI-HANG & STABILITY GUIDE (Sổ Tay Chống Treo & Lặp)

*Tài liệu này ghi lại toàn bộ hành trình cứu rỗi Bé Ba từ trạng thái hỗn loạn (Treo/Loop) trở về trạng thái vận hành ổn định (Production). Đây là kim chỉ nam để khắc phục sự cố nếu hệ thống có dấu hiệu bất ổn.*

## 🧠 1. TRẠNG THÁI SỰ CỐ BAN ĐẦU (The Chaos)
Hệ thống từng rơi vào trạng thái không thể sử dụng được với các triệu chứng:
- **Treo toàn hệ:** Không phản hồi Telegram.
- **Lặp vô hạn:** Sinh ra các chuỗi từ vô nghĩa, lặp lại liên tục (Looping).
- **Lỗi hệ thống:** Trả về `500 / INTERNAL ERROR` hoặc fallback liên tục.
- **Mất kết nối:** Không trả lời hoặc trả lời sai lệch hoàn toàn.

## 🔥 2. NGUYÊN NHÂN GỐC (Root Causes)
Một chuỗi lỗi liên hoàn từ tầng Model đến tầng Runtime:
1. **Model Loop:** Model sinh ra nội dung lặp mà không có cơ chế chặn.
2. **Subprocess Deadlock:** Subprocess không có timeout $\rightarrow$ treo toàn hệ thống.
3. **Sai lệch Model/CLI:** Dùng model bị chặn, dùng lệnh `agent run` không tồn tại hoặc option `--max-tokens` không tương thích.
4. **Mất dữ liệu Output:** 
    - Chỉ đọc `stdout` trong khi output thật nằm ở `stderr`.
    - Parse sai do dính metadata của OpenClaw.
    - Sanitize quá gắt $\rightarrow$ tự loại bỏ output hợp lệ.
5. **Tràn Context:** Không kiểm soát được lượng token $\rightarrow$ `Context limit exceeded`.

## 🛠️ 3. QUÁ TRÌNH XỬ LÝ (The Recovery Journey)

### ⚡ Giai đoạn 1: Khôi phục khả năng chạy
Sửa `worker_bridge.py`, thêm cơ chế: **Retry**, **Timeout**, và **Circuit Breaker**.

### ⚡ Giai đoạn 2: Chuẩn hóa Model
Loại bỏ các model bị chặn $\rightarrow$ Chuyển sang: `google/gemma-4-31b-it`.

### ⚡ Giai đoạn 3: Sửa lệnh CLI
Thay thế các lệnh lỗi bằng lệnh chuẩn:
`openclaw infer model run --model google/gemma-4-31b-it`

### ⚡ Giai đoạn 4: Thu thập dữ liệu toàn diện
Fix luồng lấy output: `combined = (out or "") + "\n" + (err or "")`. (Lấy cả stdout và stderr).

### ⚡ Giai đoạn 5: Làm sạch Output (Parsing)
Loại bỏ metadata OpenClaw: `text = combined.split("outputs: 1")[-1].strip()`.

### ⚡ Giai đoạn 6: Tối ưu hóa Sanitize
Thay vì reject tất cả, chỉ thực hiện: **Check rỗng** và **Giới hạn độ dài**.

### ⚡ Giai đoạn 7: Chống lặp vô hạn (Anti-Loop)
Triển khai thuật toán phát hiện lặp:
```python
lines = text.split("\n")
if len(lines) > 10:
    last = lines[-1]
    if lines.count(last) > 5:
        raise ValueError("Loop detected")
```

### ⚡ Giai đoạn 8: Chuẩn hóa cú pháp (Syntax Fix)
Sửa toàn bộ lỗi patch tay: fix ký tự `\n`, dấu ngoặc `)` thừa và lỗi `return`.

### ⚡ Giai đoạn 9: Ổn định Telegram Flow
Restart worker đúng cách, đảm bảo chạy nền và verify luồng gửi/nhận.

### ⚡ Giai đoạn 10: Quản lý Context
Thêm cấu hình compaction vào `config.yaml`:
```yaml
agents:
  defaults:
    compaction:
      reserveTokensFloor: 20000
```

## 🚀 4. KẾT QUẢ CUỐI CÙNG
- ✅ Trả lời Telegram mượt mà.
- ✅ Tuyệt đối không treo / không loop vô hạn.
- ✅ Không còn fallback giả hay lỗi CLI.
- ✅ Output đầy đủ, chính xác.

## 🎯 TỔNG KẾT CHIẾN LƯỢC
**Bản chất công việc:** Tái cấu trúc toàn bộ pipeline xử lý AI runtime từ tầng Model Call $\rightarrow$ Subprocess $\rightarrow$ Parsing $\rightarrow$ Protection $\rightarrow$ Integration $\rightarrow$ Context Management.

**Mô tả ngắn gọn:** *“Cứu một hệ AI khỏi trạng thái hỗn loạn, và đưa nó về trạng thái vận hành ổn định production.”*
