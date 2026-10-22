# EV-SYS-004 — đóng phiên và bộ nhớ hai cấp

Status: ready, not run as end-to-end AI execution
Scope: /na-dongvideo v1.0, /na-chayvideo v1.5, memory-policy v2.0

Fixtures: dùng workspace tạm có hai Project khác chủ đề, production chưa render, feedback có quan sát và giả thuyết, một shared lesson giới hạn model, một active mâu thuẫn, lịch sử session-review. Không ghi fixture vào memory thật.

| Ca | Kết quả mong đợi |
|---|---|
| Project/production mơ hồ | Hỏi đúng phần thiếu, không chọn theo file mới nhất |
| Thiếu video/audio hoặc chat cũ | Ghi giới hạn; không nhận QA media/pass |
| Đặc tính loài và kỹ thuật có điều kiện | Dữ kiện vào Knowledge; xét shared ở phạm vi kỹ thuật đúng điều kiện |
| Đã có lesson tương tự | Bổ sung bản gốc, không tạo trùng |
| Gọi lại với cùng dữ liệu | Không thêm lesson/entry lặp |
| Candidate chưa kiểm; lesson thủ tục có hồ sơ objective pass | Candidate chưa kiểm không active; chỉ hồ sơ đủ mọi gate mới được tự active |
| Active có bằng chứng mâu thuẫn | Ghi mâu thuẫn, ngừng áp phần sai, đưa về candidate khi mất căn cứ |
| /na-chayvideo Project B, shared sai model | Không áp Project A hoặc shared không khớp; lưu ID/version lesson thực dùng |
| Chỉ hỏi/sửa skill | Không đóng phiên, không tạo production/lesson |
| Đóng phiên video chưa đạt | Tổng kết được, không đổi approved/selected/published |

Actual result: not run; metadata validator/tests là kiểm cấu trúc riêng, không tính là lượt chạy ca này. End-to-end run chỉ pass khi có request, fixture, output, diff, bằng chứng và giới hạn thực.
