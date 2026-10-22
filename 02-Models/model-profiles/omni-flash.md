# Omni Flash

ID: MODEL-OMNI-FLASH
Status: unverified-interface
Updated: 2026-10-16
Requested by user: Omni Flash
Provider/model ID theo tài liệu Google đã mở 2026-10-16: Google / gemini-omni-1.1-flash. Giao diện thực tế của người dùng vẫn chưa kiểm; không tự đổi model hoặc suy setting của wrapper từ API.

## Viết prompt — /chayvideo v1.1

Nguồn: [Google Omni Flash](https://ai.google.dev/gemini-api/docs/omni.md), truy cập 2026-10-16; hồ sơ [SRC-GOOGLE-OMNI-20261016](../../01-Knowledge/sources/google-omni-2026-10-16.md). Đây là kiểm tài liệu, chưa test render.

- Nêu rõ một shot liên tục, không cắt; mô tả âm thanh và chuyển động cụ thể.
- Chỉ định ảnh mở đầu bằng lời; dùng `<FIRST_FRAME>` khi giao diện hỗ trợ và thực sự gắn ảnh.
- Có thể dùng timecode; không có cú pháp thời gian bắt buộc. Loại trừ ngắn đặt trong prompt chính.

Cách tổ chức của studio (không phải schema Google): FIRST FRAME PROMPT tiếng Anh, một đoạn chỉ t=0; VIDEO PROMPT tiếng Anh, một đoạn gồm ảnh mở đầu → thời lượng/tỷ lệ/camera → cảnh nhất quán → beat/chuyển động/nhân quả → Sound design → loại trừ. Áp nhịp riêng từng dự án. Với Underwater, giữ 5–10 beat đủ 10s, beat đầu ≤3.0s và key >5.0s. Kiểm thông số giao diện trước thực thi; không hứa prompt khóa chính xác mọi frame.

## Yêu cầu sản xuất Underwater

Video 10s, 9:16; dùng ảnh mở đầu và audio theo prompt nếu công cụ hỗ trợ. Đây là yêu cầu đầu ra, chưa phải kết quả test model. Không tự đổi model.

## Kiểm trước khi thực thi

- Xác minh trường first/start frame hay chỉ reference; tag trong text không tự đính kèm ảnh.
- Kiểm thời lượng, tỷ lệ, khả năng audio và setting thực tế của giao diện đang dùng; nếu không hỗ trợ thì nêu giới hạn, không hứa đã khóa frame.
- Timecode là yêu cầu cần kiểm trên render, không bảo đảm frame chính xác. Lưu setting/ảnh input/output thật từng attempt.
- Các URL trong v1.9 là nguồn kế thừa; chỉ trang Google ghi ở trên đã được mở lại ngày 2026-10-16. Không suy khả năng giao diện từ tên gần giống hoặc từ việc đã đọc tài liệu API.

## Lịch sử kiểm thực tế

Chưa có test nào được nhập vào hệ thống này.
