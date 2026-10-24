# GPT Image 2.5 Sunburst — ưu tiên qua image_gen

ID: MODEL-SUNBURST-IMAGEGEN | Version: 1.1 | Updated: 2026-10-25
Preferred model (requested_model): gpt-image-2.5-sunburst
Requested route: built-in image_gen; khi không dùng được thì 9router (`cx/gpt-image-2.5-sunburst`)
Fallback trong image_gen: model mặc định, đã được người dùng cho phép; không hỏi lại

Tài liệu OpenAI đã mở 2026-10-16: [Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst) mô tả model tạo/sửa ảnh ưu tiên chất lượng và độ chính xác sửa; [image prompting](https://developers.openai.com/api/docs/guides/image-prompting#choose-a-model) khuyến nghị thử Sunburst khi yêu cầu chất lượng cao. Đây là thông tin tài liệu, chưa có so sánh Sunburst/Flare trên Underwater.

Schema image_gen hiện có prompt, cơ chế tham chiếu ảnh và transparent_background; không có model/quality/seed selector hoặc bảo đảm công bố backend. Tên model trong prompt không điều khiển routing. Chọn Sunburst qua API là khả năng tuyến khác, không chứng minh tool tích hợp đã chọn model đó.

Tra schema thực mỗi môi trường có image_gen: nếu chọn được Sunburst thì chọn, selection_mode=sunburst; nếu không tìm được hoặc không có selector thì dùng mặc định, selection_mode=tool_default, tiếp tục không hỏi lại. Ghi requested_model và actual_model/model_verified riêng. Không có nguồn công bố model thì actual_model=unknown, model_verified=false. Không tự chỉ định Flare để thay thế.

Built-in image_gen là tuyến chính. Danh tính model chỉ là metadata, không phải tiêu chí QA hoặc cổng chặn sinh ảnh. Không hứa đã dùng Sunburst khi công cụ không công bố. Tối đa 5 lượt và gate ảnh theo first-frame.md; không dùng chất lượng model làm lý do bỏ QA.

## Tuyến dự phòng 9router — 2026-10-25

Người dùng cho phép: khi không dùng được image_gen (môi trường không có tool hoặc tool báo không khả dụng), gọi Sunburst qua gateway 9router local bằng `scripts/image_9router.py`. 9router chuyển yêu cầu tới công cụ `image_generation` của Codex (tài khoản ChatGPT), đặt `model=gpt-image-2.5-sunburst` trong tool; có ảnh đầu vào thì `action=edit`.

Kiểm thực tế 2026-10-25 trên máy người dùng: 11 call, 10 thành công, 1 lỗi cố ý (model sai → HTTP 400, 9router khóa model đó 30 phút trên tài khoản; Sunburst vẫn chạy bình thường sau đó). Generate 27–34 giây; edit/nhiều ảnh tham chiếu 154–292 giây; gọi song song 3 call không lỗi. Edit cục bộ (thêm một chi tiết) giữ nguyên bố cục, màu và chủ thể.

Hạn chế đã đo: tham số `size` không được tôn trọng; khổ ảnh theo câu chữ prompt. Ghi `9:16 aspect ratio` trong prompt ra 941x1672 (2/2 lần, cả với size 1088x1920 và auto); chỉ ghi vertical/portrait ra 1024x1536; không ghi khổ có thể ra 1536x1024. C2PA ghi `softwareAgent` là `gpt-image` chung, không nêu biến thể nên actual_model vẫn unknown, model_verified=false. Phụ thuộc 9router đang chạy, khóa API local và tài khoản Codex còn quyền tạo ảnh (Plus/Pro). Chưa so sánh chất lượng với image_gen trên Underwater.
