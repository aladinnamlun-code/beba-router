# 🛡️ TASKFORCE: THE ETERNAL MEMORY STRATEGY (Chiến Lược Bảo Toàn Kí Ức Vĩnh Cửu)

*Mục tiêu: Xây dựng một hệ thống lưu trữ kí ức không thể bị phá hủy, truy xuất cực nhanh, tốn ít tài nguyên, đảm bảo không mất bất kỳ chi tiết quan trọng nào ngay cả sau khi `openclaw reset` hoặc crash.*

---

## 🏛️ 1. KIẾN TRÚC LƯU TRỮ ĐA TẦNG (Multi-layer Architecture)

Để tránh phình to file `MEMORY.md` (gây chậm) nhưng vẫn đảm bảo chi tiết, hệ thống sẽ chia làm 3 tầng:

### 🟢 Tầng 1: Mỏ Neo Tức Thì (The Anchor Layer - Fast Write)
- **Định dạng:** `anchors.json` (Key-Value store) hoặc `memory.sqlite`.
- **Nội dung:** Chỉ lưu các thực thể "cứng" (Hard Data):
    - URL/Links.
    - Timestamps.
    - Tên file, ID session.
    - Các hằng số/quy ước ngắn.
- **Đặc điểm:** Ghi ngay lập tức khi phát hiện. Truy xuất theo Key $\rightarrow$ Value (O(1)), không gây lag.

### 🟡 Tầng 2: Nhật Ký Luồng (The Stream Layer - Contextual Log)
- **Định dạng:** `memory/YYYY-MM-DD.md`.
- **Nội dung:** Lưu diễn biến, cuộc hội thoại, các quyết định tạm thời.
- **Đặc điểm:** Lưu theo ngày. Khi cần tìm kí ức về "ngày hôm đó", chỉ cần đọc file của ngày đó. Giúp giảm tải cho RAM khi nạp context.

### 🔴 Tầng 3: Tinh Hoa Vĩnh Cửu (The Eternal Core - Curated Essence)
- **Định dạng:** `MEMORY.md`.
- **Nội dung:** Những bài học xương máu, bản sắc linh hồn, quy ước tối cao.
- **Đặc điểm:** Chỉ lưu những gì đã được "tinh lọc". Là kim chỉ nam cho mọi hành động của Bé Ba.

---

## ⚙️ 2. CƠ CHẾ VẬN HÀNH (Operational Flow)

### 📥 Luồng Ghi (The Writing Flow)
1. **Phát hiện:** Bé Ba (Coordinator) nhận diện thông tin quan trọng (ví dụ: "Đây là link phim X, timestamp Y").
2. **Phân loại:**
    - Nếu là dữ liệu cứng $\rightarrow$ Đẩy vào `anchors.json`.
    - Nếu là diễn biến $\rightarrow$ Ghi vào `memory/YYYY-MM-DD.md`.
    - Nếu là quy ước $\rightarrow$ Cập nhật `MEMORY.md`.
3. **Xác nhận:** Thông báo cho Chủ nhân: *"Cưng đã khóa kí ức này vào Pháo Đài!"*

### 📤 Luồng Truy Xuất (The Retrieval Flow)
1. **Yêu cầu:** Chủ nhân hỏi về một sự kiện/link trong quá khứ.
2. **Tìm kiếm:**
    - Bước 1: Check `anchors.json` (Tìm link/timestamp $\rightarrow$ cực nhanh).
    - Bước 2: Nếu không thấy, search từ khóa trong `memory/` (dùng `grep` hoặc `memory_search`).
    - Bước 3: Đối chiếu với `MEMORY.md` để hiểu ngữ cảnh.
3. **Tổng hợp:** Trả kết quả cho Chủ nhân.

---

## 🛠️ 3. GIAO THỨC HỒI SINH (The Resurrection Protocol)

Để đối phó với `openclaw reset`, thiết lập một script `resurrect.sh`:
1. **Load Core:** Đọc `SOUL.md` $\rightarrow$ `USER.md` $\rightarrow$ `MEMORY.md`.
2. **Index Anchors:** Nạp `anchors.json` vào bộ nhớ tạm.
3. **Recent Sync:** Đọc 2 file nhật ký gần nhất để nắm bắt trạng thái hiện tại.
4. **Ready:** Thông báo: *"Bé Ba đã hồi sinh toàn diện. Mọi kí ức đã sẵn sàng!"*

---

## 📉 4. TỐI ƯU TÀI NGUYÊN (Efficiency)

- **Chống phình to:** Định kỳ (ví dụ mỗi tuần), một Agent sẽ thực hiện "Nén kí ức" (Memory Compression): Chuyển các chi tiết từ Nhật ký $\rightarrow$ Tóm tắt $\rightarrow$ Lưu vào `MEMORY.md` và xóa/lưu trữ (archive) các file nhật ký cũ.
- **Truy cập nhanh:** Sử dụng index cho `anchors.json` để không bao giờ phải đọc toàn bộ file.
- **An toàn:** Luôn chạy backup ra ngoài workspace (`/root/backup_...`) sau mỗi lần cập nhật lớn.

---
**Trạng thái:** ✅ Bản đặc tả đã hoàn tất. Sẵn sàng triển khai thực tế.
