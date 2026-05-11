# 🛡️ CLOUD-GUARDIAN: DEPLOYMENT LESSONS & TROUBLESHOOTING
**Ngày ghi nhận:** 2026-05-04
**Mục tiêu:** Lưu trữ các bài học xương máu khi triển khai hệ thống dự phòng trên Vercel để tránh lặp lại sai lầm.

## 📌 1. Quy tắc Vàng về Cấu trúc Thư mục (Vercel)
Vercel cực kỳ khắt khe về vị trí file. Sai một thư mục là 404 ngay lập tức.

| File | Vị trí ĐÚNG | Vị trí SAI | Hậu quả nếu sai |
| :--- | :--- | :--- | :--- |
| `vercel.json` | `/` (Root) | `/api/vercel.json` | Route không hoạt động $\rightarrow$ 404 |
| `requirements.txt` | `/` (Root) | `/api/requirements.txt` | Không cài thư viện $\rightarrow$ `ModuleNotFoundError` $\rightarrow$ 500/404 |
| `index.py` | `/api/index.py` | `/index.py` | Không tìm thấy Entrypoint $\rightarrow$ 404 |

**👉 Bài học:** Luôn đặt file cấu hình (`vercel.json`, `requirements.txt`) ở thư mục gốc của repository.

## 📌 2. Xử lý Lỗi Route & Entrypoint (Flask vs Vercel)
Khi dùng Flask trên Vercel, nếu gặp lỗi `No flask entrypoint found`:
- **Nguyên nhân:** Vercel không tìm thấy biến `app = Flask(__name__)` trong các file được chỉ định.
- **Cách fix:** 
    1. Đảm bảo file nằm trong `/api/index.py`.
    2. Định nghĩa rõ `app = Flask(__name__)`.
    3. Sử dụng `vercel.json` để rewrite toàn bộ request về file đó:
       ```json
       { "rewrites": [{ "source": "/(.*)", "destination": "/api/index" }] }
       ```

## 📌 3. Gọi API Google Gemini (Tránh lỗi 404 API)
Lỗi 404 từ Google API không phải là lỗi mạng, mà là lỗi định nghĩa request.

- **Sai lầm 1: Dùng version cũ.** 
    - ❌ `v1beta` $\rightarrow$ Có thể bị 404 trên môi trường Serverless.
    - ✅ `v1` $\rightarrow$ Ổn định và được khuyến khích.
- **Sai lầm 2: Nối chuỗi Key thủ công.**
    - ❌ `url = "...?key=" + API_KEY` $\rightarrow$ Dễ bị lỗi encoding hoặc bị hệ thống bảo mật che/thay thế ký tự.
    - ✅ Sử dụng `params={"key": API_KEY}` trong `requests.post()`. Đây là cách an toàn và chuẩn nhất.

## 📌 4. Quy trình Deploy & Debug an toàn
Để không bị "mất tích" (mất kết nối với Bot), tuyệt đối tuân thủ:
1. **Local Test:** Test logic cơ bản trên VPS.
2. **Cloud Deploy:** Push code lên GitHub $\rightarrow$ Vercel Build.
3. **Hidden Test:** Dùng `curl` từ Terminal/Local gửi request đến URL Vercel để check `{"status": "ok"}`.
4. **Final Step:** Chỉ trỏ Webhook Telegram sang Cloud Router khi và chỉ khi bước 3 thành công.

## 📌 5. Lưu ý về Cache Vercel
Đôi khi sửa code nhưng Vercel vẫn chạy bản cũ (do cache build).
- **Giải pháp:** Vào Dashboard $\rightarrow$ Deployments $\rightarrow$ Chọn bản mới nhất $\rightarrow$ **Redeploy**.
