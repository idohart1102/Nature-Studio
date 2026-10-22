# Đọc mẫu có bằng chứng

Version: 1.2 | Updated: 2026-10-17 | Quan sát và chức năng phục vụ chuyển thể

## Truy cập và khả năng thật

Kiểm công cụ trong phiên trước khi chọn đường đọc. File có thể dùng công cụ video/audio thật sẵn có; link thì mở đúng trang/media bằng connector hoặc browser phù hợp, tuân thủ skill công cụ nếu có. Không đoán rằng xem được trang là đã xem được video/âm. Cần đăng nhập thì cho người dùng tự đăng nhập; không thu mật khẩu/cookie. Link bị chặn/hết hạn hoặc không truy cập toàn video thì xin file thay thế. Không tải remote media để lách hạn chế hiển thị và không tự đăng ký API/tiêu tiền/cài tool để đọc.

Ưu tiên đọc video liên tục bằng công cụ hỗ trợ thật, rồi xem lại chuyển động nhanh/key/cut và nghe audio riêng khi cần. Có FFmpeg/ffprobe sẵn thì có thể lấy metadata/frame/audio local, nhưng giải mã/trích xuất không có nghĩa AI đã xem/nghe. Không bắt có FFmpeg nếu công cụ native đã đủ. Nếu chỉ có ảnh/frame lấy mẫu: ghi visual partial, không suy ra đầy đủ chuyển động giữa các frame, dù có frame ở đầu/cuối. Nếu chưa nghe thực thì audio partial/unavailable, không suy ra âm từ hình/transcript/waveform. Không giả công cụ video hoặc model phân tích đã tồn tại.

## Phân tích toàn thời lượng

Xác định duration/FPS/tỷ lệ/có audio theo metadata đã đọc, đánh dấu unknown khi chưa biết. Theo dõi cả hình và tiếng từ 0 tới hết; ghi đoạn đã xem/nghe, phương pháp và evidence (tool result, frame file, audio/video segment, timestamp). Quanh hành động nhanh lấy thêm frame đủ phân giải động tác, không áp một FPS mẫu cứng cho mọi clip. Coverage toàn thời lượng không có nghĩa đã kiểm từng frame hoặc mọi chi tiết đúng.

- **Không gian/camera:** từng shot/cut, máy cố định/di chuyển, độ cao/hướng nhìn/cự ly/góc rộng tương đối, chủ thể gần/xa, che khuất, ánh sáng và vật thể nền. Không bịa tiêu cự, chiều sâu, tốc độ hoặc loài chính xác khi không đủ căn cứ.
- **Vai trò:** đặt ID ổn định R1/R2… theo chức năng trong chuyện, tách khỏi tên loài. Ghi nhận dạng/trạng thái ban đầu, hướng nhìn, vị trí và đường vào/ra. Có thể một nhân vật giữ nhiều vai trò; không ép luôn phải có kẻ săn mồi–con mồi.
- **Hành động:** từng sự kiện có timecode, actor/targets, tín hiệu trước, động tác/tốc độ/hướng/tiếp xúc, nguyên nhân và thay đổi sau; chú ý phản ứng phụ của môi trường. Không chỉ tóm tắt “đuổi rồi cắn”; ghi đủ các động tác đọc được của từng vai trò. Đoạn bị che ghi chưa thấy, không điền kết quả mong muốn.
- **Câu chuyện:** chi tiết/quan hệ quyết định, hook, tiến triển, key/hậu quả khi có; cảnh quan/quan sát không bị ép thêm cao trào. Nối phần hình/âm/lời/nhịp quan trọng với chức năng cần cho bản đích trong story/mô tả hiện có; phân biệt điều quan sát có timecode với diễn giải về động cơ/chú ý/cảm xúc/viral. Chức năng là đầu vào để chọn giữ/thay/bỏ theo chuẩn chuyển thể, không phải luật buộc sao mẫu. Không thêm field/schema hoặc báo cáo mới chỉ để ghi phần này.
- **Âm thanh:** môi trường, hành động, nhạc/giọng nếu có; timecode, độ liên tục/nhịp, texture, mức nổi bật tương đối và đồng bộ/độ trễ. Nguồn gây tiếng chỉ là giả thuyết nếu nghe không nhận dạng được; không tự gán tiếng kim loại hoặc “tiếng đớp của loài X”. Không ghi dB/LUFS nếu chưa đo. Ghi cả khoảng im lặng và phần không nghe rõ; không khẳng định vắng nhạc/voice nếu audio chưa nghe đủ.

Nếu mẫu dài hơn khả năng đọc trong một call, chia các đoạn phủ đủ toàn thời lượng và xem nối tại ranh giới để không bỏ mất hành động/âm qua ranh; không chỉ đọc 10 giây đầu rồi nhận đã phân tích toàn clip. Nếu cần chọn một câu chuyện từ video dài cho bản 10s, đọc đủ mẫu trước (hoặc người dùng chọn đoạn), ghi đoạn nguồn được dùng và phần lược bỏ. Không ép nhồi nhiều biến cố hoặc tăng tốc vô lý cho vừa 10s.

## Lưu và tái dùng

Phân tích local ở `.nature-studio/references/<ref-id>/analysis-v001.json`, bằng chứng cùng thư mục; bản dùng cho clip dẫn trong production/INPUTS và research. Chỉ giữ bản media local được cung cấp/được phép, không cần chép file video lớn vào từng production. Không publish media, URL riêng hoặc hồ sơ tham chiếu.

Hash bytes file nguồn với `python scripts/reference_video.py hash <file>`; link chỉ là locator, không là danh tính bất biến. Có file/hash hoặc remote version kiểm được mới xác nhận cache còn đúng; URL giống nhau hoặc bản metadata hash không chứng minh nội dung không đổi. Không kiểm lại được nguồn thì ghi cache unverified, không gọi fresh. Clip/analysis đổi làm brief cũ hết hạn; chuẩn Project đổi chỉ cần đọc lại chuẩn/ánh xạ, không tự phân tích lại video nguyên vẹn không đổi. Đổi target không buộc đọc lại toàn mẫu nếu hồ sơ đã có đầy đủ thông tin cần thiết.

Chạy helper check/brief theo schema. Đọc lại bằng chứng phần ảnh hưởng nếu hồ sơ mơ hồ/thiếu động tác hoặc âm; không dùng bản brief ngắn để che coverage thiếu. Mặc định chỉ giao bộ chuyển thể hoàn chỉnh khi đủ hình và âm (hoặc xác minh nguồn không có audio). Phân tích một phần chỉ giao như draft khi người dùng trực tiếp chấp nhận giới hạn đó; giới hạn phải đi cùng hồ sơ và kết quả, không tự hiểu im lặng là đồng ý.

## Preflight có thể kiểm — v1.7

Trước nhận phân tích, chạy `python scripts/media_review.py capabilities` nếu dùng runtime local, đối chiếu thêm tool thực trong phiên theo [media review](../../../../00-Standards/media-review-and-finishing.md). Phát hiện FFmpeg/WhisperX không mở native video/audio understanding; báo phần thiếu ngay, không hứa upload file sẽ giải quyết. Adapter thật cần method/ranges/evidence. Không biến chấp thuận partial thành quyền đổi cơ chế máy–chủ thể.
