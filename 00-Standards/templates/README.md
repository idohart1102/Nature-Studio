# Mẫu hồ sơ

Đây là mẫu, không phải dữ liệu thực hoặc việc yêu cầu người dùng điền toàn bộ. AI tự điền phần có căn cứ; dùng unknown / not checked / not applicable đúng nghĩa khi thiếu. Không giả tạo kết quả.

- [Dự án mới](project.md)
- [Brief](brief.md), [Nghiên cứu](research.md), [Ý tưởng](concept.md)
- [Đầu vào attempt](attempt-inputs.md), [Thiết lập](settings.md), [Review](review.md)
- [Phản hồi](feedback.md), [Hiệu quả đăng](performance.md), [Tóm tắt video](episode-summary.md)
- [Bài học](lesson.md), [Ca đánh giá](evaluation-case.md), [Nguồn](source.md), [Manifest phát hành](release-manifest.md)

Tạo thư mục production/attempt thực khi có nhiệm vụ; A01 chứa prompt ảnh, prompt video, caption và media thật nếu có. Chưa nhập các clip cũ trong chat vào kho; không tự coi đây là video đầu tiên đã hoàn thành.

- [Tổng kết phiên](session-review.md) cho /na-dongvideo. [Lesson](lesson.md) dùng JSON frontmatter portable; không copy mẫu chưa điền vào Memory.

- [QA first frame](first-frame-review.md), [handoff JSON](first-frame-handoff.json): chỉ điền dữ liệu thực; không coi template là kết quả đạt.

## Profile và asset

[species-profile.md](species-profile.md) dùng cho cá hoặc nhóm khác, giữ sáu phần dễ dùng; [asset-record.json](asset-record.json) là metadata nhập vào catalog local. Đây là template, không là file/ảnh đã tồn tại hoặc QA. Không tạo hồ sơ rỗng hàng loạt.

## Binding ngoại lệ beat

Chỉ dùng khi đã đối chiếu yêu cầu trực tiếp của người dùng; helper xác minh file/hash/phạm vi, không chứng minh tác giả/chấp thuận. Quyền không giới hạn “cụm hành động” không tự là quyền bỏ số beat. Trong production lưu nguyên yêu cầu được phép giữ và JSON grant dưới đây, dùng giá trị thật (không tạo từ template để giả authority):

```json
{
  "schema": 1,
  "rule": "beat_count",
  "project": "underwater",
  "production": "VIDEO-ID-THAT-ALREADY-EXISTS",
  "mode": "revision",
  "beat_count": 9,
  "confirmed_user_request": true,
  "authorization": {"path": "requests/user-change.md", "sha256": "MEASURED"},
  "video_prompt_sha256": "SHA256-OF-EXACT-UTF8-PROMPT",
  "target_attempt": "A02",
  "base_attempt": "A01",
  "base_sha256": "MEASURED-BASE-OUTPUT-SHA256"
}
```

9 chỉ minh họa. target_attempt phải là attempt tiếp theo đúng layout (A02 hoặc attempts/A02), chưa tồn tại khi save; check bản đã lưu vẫn cho kiểm lại binding. New/reference mới không có base; revision luôn có base thật. Data output chứa `contract_exception: {"path":"requests/beat-grant.json","sha256":"MEASURED"}` và checks.key_onset thật. File grant/request nằm trong production và được kiểm hash. Dùng cùng lệnh check/save với `--project` và `--production`; JSON tự khai không đủ quyền. Ngoại lệ chỉ đổi count, không miễn timeline/key/duration/aspect/one-shot. Không sửa lịch sử để giả đã có grant. Nếu target/prompt/base/yêu cầu đổi thì rà lại phạm vi, không tự gia hạn grant.

- `asset-inputs.json`: khai báo input thực theo attempt; điền hash/arguments thật, không dùng template rỗng như bằng chứng. Handoff mới schema3; legacy giữ nguyên.

- `caption-variants.json`: template minh họa, không phải sản phẩm/footage đã QA; caption canonical + bundle schema1, selected style; mỗi bản caption EN, caption_vi, hook_text, hook_vi. Định dạng/patch/legacy theo lõi workflow.
