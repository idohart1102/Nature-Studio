# Underwater — QA first frame

Version: 1.3 | Updated: 2026-10-22 | UF-D021, UF-D025

Đọc concept/brief và format hiện hành, dùng gate chung tại [first-frame.md](../../00-Standards/first-frame.md). Không cần cảnh nào cũng có cá/mồi trong khung nếu concept t=0 đã khóa chúng chưa xuất hiện.

- Đúng loài, số lượng, nhận dạng/vây/mắt/miệng/hoa văn, tỷ lệ cá–con mồi–địa hình. Kiểm chi tiết ảnh thật với dữ kiện phù hợp, không dùng vẻ “khổng lồ” thay tỷ lệ có căn cứ.
- Ảnh ở t=0 trước sự kiện key, không cắn/ngậm/bắt sẵn con mồi khi chuyện yêu cầu tiếp cận trước. Cua/cá mồi ở đúng trạng thái đã chọn; không tự thêm móc/dây vào săn mồi tự nhiên.
- Hook UF-D025: đối tượng thu hút (mồi/rig, con mồi hoặc phần cá) nhận ra được khi thu nhỏ ảnh khoảng 1/4; có không gian/đường vào cho tín hiệu mới trước 3.0s theo [Hook 3 giây đầu](format.md#hook-3-giây-đầu--uf-d025).
- Nếu có rig/tackle: số móc, cách gắn, đầu nối, dây/leader và phần nhìn thấy phải thống nhất. Không bịa sợi nối bị che hoặc suy đã đúng chỉ từ prompt.
- Sinh cảnh, vật liệu đáy, cây, độ sâu, thời gian/ánh sáng, màu nước và màu thân hợp nghiên cứu. Màu nước và độ trong là hai kiểm riêng; có suy giảm chi tiết/tương phản theo cự ly, không phủ màu lên ảnh rõ như không khí.
- Khung t=0 từ camera cầm tay chìm có thể quay thật; ảnh tĩnh không chứng minh có chuyển động cầm tay. Chừa không gian cho đường máy đã chọn và kiểm nền đúng phối cảnh trên video thật; phối cảnh, nguồn sáng và kích thước vật thể cùng hợp lý. Không dùng góc điện ảnh không được giao, tăng đục hoặc che chủ thể để giấu lỗi.
- Bố cục giữ không gian cho đường bơi/đường tiếp cận/thoát theo concept, không để vật che ngăn key đọc được. Không tự thêm khe gỗ, bùn hoặc con mồi để ép cảnh vào chuyện cũ.
- File ảnh đo pixel thật; tỷ lệ đầu vào 9:16 theo dung sai ≤0.1% tại first-frame.md, export chính xác kiểm riêng. Không tự crop/căng ảnh hoặc cắt mất chủ thể để báo đúng tỷ lệ; sửa bằng image_gen trong budget hoặc nêu giới hạn. Không nhạc/audio trong ảnh, không chữ/caption/logo AI tự vẽ; dấu bắt buộc của nền tảng ghi giới hạn, không tự xóa trái công cụ.

Các mục trên bắt buộc khi áp dụng. Ảnh đạt không chứng minh video giữ được giải phẫu, t_key_start >5s, chuyển động hay audio; các phần đó phải kiểm riêng trên video thật. QA không đổi brief/câu chuyện/caption, không tự duyệt bởi người dùng.


- Khi có setting: kiểm vùng/mùa/giai đoạn, nước ngọt/lợ/mặn, nền đáy/cây/dòng nước và màu/độ trong theo hồ sơ vùng được chọn. Phân bố đúng chưa đủ chứng nhận nền ảnh; chưa kiểm nguồn hoặc ảnh thực thì ghi not_checked. Giữ màu tannin tự nhiên có căn cứ, không coi mọi màu vàng nước là ám màu lỗi. Không suy địa điểm thật từ ảnh AI.
