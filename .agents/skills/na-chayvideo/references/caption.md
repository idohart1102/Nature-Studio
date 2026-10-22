# Chỉ sửa caption

Đọc packet caption/stage write qua view (Project, giọng viết, memory policy và descriptor bài học rồi mở gốc phù hợp) cùng nội dung clip đã chốt: concept/attempt/video được cung cấp. Theo [lõi chung](../../../../00-Standards/video-prompt-workflow.md), không nạp JSON/hash inventory hoặc toàn bộ Memory INDEX. Chỉ mở phần nguồn đủ xác định hành động/kết cục/dụng cụ và caption trước. Không đọc toàn bộ lịch sử concept, habitat, model, Story Development hoặc tái phát triển chuyện chỉ để sửa một câu. Có nghi vấn thuật ngữ/cơ chế thì mở đúng nguồn bổ sung. So caption gần đây để tránh lặp cách mở khi cần. Coverage không thay tự kiểm giọng/đúng cảnh.

Underwater: nguyên bản, ngắn/trực tiếp, chọn một chi tiết đáng xem, giọng người câu cá Mỹ. Linh hoạt hỏi/nhận xét/phản ứng/chỉ dẫn, thường 1–8 từ nhưng không quota. Không nhồi slang/jargon hoặc khẳng định mắc/bắt/nuốt khi hình chưa chứng minh. Phần câu caption và 3–5 hashtag khác nhau liên quan viết **cùng một đoạn**; hook_text riêng không có hashtag. Không AI/công nghệ tạo nội dung, không #Underwater bất kể hoa/thường. Prompt/concept chỉ là dự kiến; render được cung cấp thì bám điều đã quan sát thật. Giữ mức không chắc chắn khi bị che.

Trả CAPTION theo hợp đồng Project. Underwater mặc định ba bản Chuẩn/Hài hước/Tò mò, mỗi bản: caption EN + hashtag → lược dịch caption VI → hook text EN 1–9 từ → lược dịch hook VI. Viết tiếng Anh Mỹ tự nhiên trước rồi dịch ý sau; không giả giọng bằng slang/jargon hoặc dịch thành ngữ Việt. Caption/hook bổ trợ nhau, ba bản khác cách tiếp cận và đều khớp cảnh; không hứa payoff ngoài clip. Hook text riêng không tự vẽ lên media.

JSON/lưu dùng caption_variants/selected caption theo [template](../../../../00-Standards/templates/caption-variants.json) và lõi chung. Mặc định làm đủ ba; nếu chỉ được giao sửa một bản, trả đúng bản đó và giữ các bản khác còn phù hợp qua base đã resolve. Không cập nhật lược dịch/hook/caption rời làm lệch nhau. Kiểm cú pháp bằng helper rồi tự QA giọng/đúng cảnh; không cấp ID, viết lại prompt hoặc sửa lịch sử. Hồ sơ cũ chỉ có caption vẫn đọc được, không tự backfill ba bản.

Khi lưu bằng helper, resolve đúng bản gốc rồi truyền base_attempt/base_sha256 theo lõi chung. Caption-only không được kèm thay đổi idea/prompt/frame_state; tự kế thừa phần giữ nguyên, không mở lại QA ảnh nếu không có nhiệm vụ dùng ảnh.


Nếu Project yêu cầu tag địa điểm, lấy setting đã khóa từ INPUTS/frame_state; Underwater dùng đúng một tag địa điểm chung cho ba bản, trong tổng 3–5 tag. Legacy thiếu setting không tự đoán: theo nhánh xử lý tại audience-and-caption.md. Đổi vùng ảnh hưởng cảnh phải là revision được giao, không sửa prompt/frame_state trong caption-only.
