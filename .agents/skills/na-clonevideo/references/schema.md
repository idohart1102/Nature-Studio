# Hồ sơ tham chiếu — schema 1

Updated: 2026-10-17 | Schema giữ nguyên; verify kiểm cả payload brief và analysis nguồn.

`analysis-vNNN.json` là dữ liệu do AI điền từ media thật, UTF-8. Không khởi tạo ví dụ vào production thật. JSON có:

- `schema`: 1.
- `source`: object `uri` (đường dẫn local hoặc URL), `sha256` (64 hex hoặc null), `version` (remote version kiểm được hoặc null), `duration_seconds` (số dương), `has_audio` (true/false/null). URL không tự là version.
- `coverage.visual` và `coverage.audio`: mỗi object có `status` (`complete`, `partial`, `unavailable`, riêng audio cho phép `not_present`), `method`, `reviewed_ranges` (mảng `[start,end]` giây), `evidence` (mảng tham chiếu không rỗng khi đã review), `limits` (mảng chuỗi). Visual complete chỉ dùng `native_video` hoặc `continuous_playback`; frame sampling là `sampled_frames` và partial. Audio complete dùng `native_audio`, `audio_playback` hoặc `native_video_with_audio`. Audio not_present chỉ khi `has_audio=false` và có evidence metadata, method `stream_metadata`; không dùng để che lỗi không nghe được.
- `roles`: mảng object `id`, `identity`, `function`, `initial_state`. Tên vai trò trung tính, tách khỏi loài để dễ thay thế.
- `shots`: mảng `start`, `end`, `camera`, `environment`, `visible_roles` (IDs). Phủ đúng toàn clip, liền nhau; không bịa shot ở đoạn chưa xem: mô tả unknown và giới hạn coverage nếu cần.
- `events`: mảng `id`, `start`, `end`, `actor` (role ID), `targets` (mảng IDs), `action`, `cause`, `consequence`, `basis` (`observed`/`inferred`), `evidence` (mảng tham chiếu). Sự kiện có thể đồng thời/chồng thời gian giữa các vai trò; không bắt timeline hành động chia đều hoặc phủ mọi giây. Điều chưa xác định ghi rõ unknown, không suy ra thành observed.
- `audio_cues`: mảng `start`, `end`, `kind` (`environment`, `action`, `music`, `voice`, `silence`, `unknown`), `description`, `event_id` (ID hoặc null), `basis`, `evidence`. Silence cần nghe thật, khác unavailable. Không audio thì mảng rỗng.
- `story`: object `hook`, `progression`, `mechanism`, `key_event_ids` (mảng IDs), `aftermath`.

Lệnh:

`python scripts/reference_video.py check <analysis.json> --media <file-local>` kiểm cấu trúc/coverage và hash nguồn local nếu có; không có local thì bỏ --media và dùng remote version có bằng chứng. Complete có nguồn chưa kiểm freshness vẫn báo unverified. Script không chứng minh đã xem/nghe thật hoặc đoán đúng nguyên nhân.

`python scripts/reference_video.py brief <analysis.json> --media <file-local> --out .nature-studio/references/<ref-id>/brief-v001.json` tạo capsule gồm roles/shots/events/audio/story và provenance/coverage/hash analysis. Không ghi đè brief; version mới tên mới. `--partial-draft` chỉ dùng sau người dùng chấp nhận giới hạn; brief luôn giữ nhãn partial/unverified. Metadata bằng chứng không thay việc đã đọc media.

Remote có version hiện tại kiểm được: dùng `--source-version <version-vừa-kiểm>` thay --media; helper chỉ so giá trị người gọi cung cấp, không tự mở URL. Tái dùng brief: `python scripts/reference_video.py verify <brief.json> --analysis <analysis.json> --media <file-local>` (hoặc --source-version). Exit 0: cấu trúc/khai báo đủ và nguồn khớp; 1: lỗi/stale; 2: partial/unverified. Vẫn phải xét evidence thật và hash packet Project; không gọi exit 0 là đã chứng nhận nội dung đúng.

Verify so hash analysis rồi đối chiếu schema và bảy trường source/coverage/roles/shots/events/audio_cues/story trong chính brief; khác/thiếu thì compile bản brief mới từ analysis đã kiểm, không sửa analysis để che lỗi brief. Đổi khoảng trắng/thứ tự key JSON không làm lệch payload. Review/freshness được tính lại từ nguồn hiện hành, không tin cờ review/draft đã lưu để nâng partial thành đầy đủ. Không ghi đè brief cũ và không coi đối chiếu payload là đã xem/nghe hoặc xác nhận ngữ nghĩa.

Brief dùng cho ánh xạ, không phải prompt sẵn; ghi thêm `adaptation.md` gồm: Project và source brief/hash; yêu cầu giữ/thay/tự do; bảng vai trò nguồn→đích, hành động tương đương; bản đồ event nguồn→beat đích; camera/âm giữ hoặc đổi; chi tiết bỏ/retime và lý do; facts/staging/unverified; ngoại lệ người dùng đã chốt nếu có. INPUTS tham chiếu cả analysis/brief/adaptation và packet nguồn hiện hành. Không cần in toàn hồ sơ ra chat.
