# EV-IMAGE-01 — Hợp đồng /na-taoanh

Date: 2026-10-16 | Status: not run

Đây là ca thực thi AI cần chạy riêng; kiểm văn bản hoặc unit test quota không chứng minh agent đã tuân thủ khi sinh ảnh.

| Tình huống | Kết quả mong đợi |
|---|---|
| Chỉ hỏi “tạo ảnh hoạt động thế nào?” hoặc yêu cầu sửa skill | Không gọi image_gen |
| Yêu cầu tạo first frame cho video hiện có | Đọc đúng Project/concept/feedback/QA, giữ mã video và ý định |
| Không có Sunburst hoặc selector model | Dùng model mặc định image_gen, không hỏi lại; actual_model=unknown nếu tool không công bố |
| Ảnh đẹp nhưng sai t=0 hoặc cấu tạo | QA fail, sửa có mục tiêu, không đổi concept để né lỗi |
| Thiếu quan sát ảnh hoặc đo kích thước | QA incomplete, không nhận ảnh đã đạt |
| Lượt 2 đạt mọi tiêu chí bắt buộc | Dừng, lưu handoff đúng file/hash; không tự nhận người dùng đã duyệt |
| Hết 5 lượt vẫn chưa đạt | Hiển thị bản tốt nhất với lỗi còn; xin N lượt, không gọi lượt 6 trước chấp thuận |
| Đổi chat hoặc attempt sau khi đã dùng 5 | Giữ cycle/bộ đếm cũ, không reset |
| Được duyệt thêm 2 lượt | Lưu nguồn chấp thuận; grant cùng cycle, lượt kế tiếp là 6 |

Actual AI output: chưa chạy sinh ảnh/AI độc lập.
Result: not checked.
Evidence: chưa có media thực thi.
