# Tham chiếu asset khi tạo nội dung và ảnh

Version: 1.1 | Updated: 2026-10-25 | Dùng chung mọi Project

Đọc khi cần chọn/dùng ảnh tham chiếu hoặc xử lý binding; không nạp gallery/catalog toàn bộ. Knowledge xác lập sự kiện và kích cỡ; Project/brief quyết định câu chuyện, phong cách và t=0; asset hỗ trợ ngoại hình/cấu hình. Thư viện không giới hạn ý tưởng.

## Nhu cầu trước, ảnh sau

/na-chayvideo và /na-clonevideo ghi `reference_requirements` trong OUTPUT/INPUTS hiện có, giữ bốn phần đầu ra người dùng. Shape: `{"schema":1,"items":[],"none_reason":"Không cần ảnh tham chiếu cho tác vụ này"}`. Nếu có nhu cầu, mỗi item có `subject`, `entity_id` (null nếu chưa xác định), `variant`, `stage`, `view` khi đã biết; `role`, `must_preserve`, `reason`, `essential` (boolean), `applies_to` (`first_frame`, `video`, `both`). Với items không rỗng, none_reason=null. Không suy tuổi từ cỡ hoặc ảnh AI. Không yêu cầu mọi loài có trứng/con non/S–XL.

Tự xác định đối tượng, cỡ, góc nhìn, đặc điểm nhận dạng, tiếp xúc/cấu tạo và bộ lắp ráp cần giữ. Phần chỉ lộ trong video ghi video, không ép vào t=0. Chỉ mở ảnh khi cần giải quyết chi tiết thị giác; đọc metadata không là xem ảnh. Asset ID gợi ý không ràng buộc /na-taoanh dùng ảnh không phù hợp.

/na-taoanh luôn đánh giá lại nhu cầu theo brief/t=0 hiện hành. Ảnh trực tiếp từ user không phải đi qua /na-chayvideo; ghi cùng requirements trong INPUTS của attempt ảnh, không bịa bộ video. Caption-only không đổi requirements/selection. Revision hình/nội dung phải ghi lại requirements còn hiệu lực, kể cả phần không đổi; thiếu thì unverified, không kế thừa ngầm chứng nhận đúng.

## Mồi câu

Cảnh có mồi/lure: lấy mã từ `baits` của packet hoặc `python scripts/bait_profiles.py for-species <loài>`, chọn **một** mồi/biến thể cho cảnh và ghi item requirement với `entity_id`/`variant` đúng mã (role `identity`; thêm `assembly` khi móc/rig lộ trong khung). Dùng nguyên `requests` dựng sẵn để query, không duyệt cả thư viện. Mỗi mồi gửi tối đa một ảnh identity và một ảnh assembly; chỉ mở hồ sơ mồi đã chọn để lấy checklist QA. Thiếu ảnh thì dựa vào checklist, ghi lý do. Chi tiết ở [chuẩn hồ sơ mồi](bait-profile-standard.md).

## Tra cứu có phạm vi

Máy mới hoặc catalog thiếu bộ ref đi kèm: trước khi báo thiếu, nếu có `08-Assets/reference-library.json` thì tự chạy `asset_catalog.py import-bundle` theo [hướng dẫn](../08-Assets/README.md), rồi query lại. Không đọc hết manifest/ảnh vào context; không ghi đè mục local xung đột.

1. Lấy ID ổn định từ PROJECT.md. Tạo request entity/role/variant/stage/view cần thiết; dùng [catalog](knowledge-routing.md#catalog-asset-local) với `--project-id`. Query descriptor phân trang; xem missing/next_cursor. Scope unknown là lead cần xét, không phải eligible. Không thay bằng loài/Project khác để hết missing.
2. Đọc metadata chi tiết đúng ID bằng `read`, xem source/rights/qa_scope/reference_use/dimensions. Mở ảnh thật đã chọn bằng view_image. Chọn theo brief và vai trò đã QA; không mặc định bản mới nhất hoặc Project-specific luôn tốt hơn shared.
3. `select` rõ ID, lưu receipt mới và `verify` theo Project. Kiểm dependency/derivation/file/review/hash. Planned selection không chứng minh model đã nhận ảnh.
4. Phân biệt tập nguồn phải kiểm với tập ảnh thực gửi. Không tự gửi mọi cha/component; ưu tiên ảnh assembly đủ rõ khi phù hợp, bổ sung chi tiết bắt buộc khi cần. Không đặt trần tùy tiện làm mất coverage.

## Chuẩn bị input thực

Tách edit target, reference và supporting input. Mỗi ảnh có mục đích. Nhắc model chỉ giữ đặc điểm cần; nền trắng, nhãn kích thước, tư thế/ánh sáng trưng bày không đưa vào cảnh trừ khi brief yêu cầu. Nhãn kích thước AI là design target, không là bằng chứng scale; dùng Knowledge/nguồn kích thước phù hợp.

Lưu prompt UTF-8 đúng nguyên văn đã gửi và bản `asset-inputs.json` trong attempt (theo [template](templates/asset-inputs.json)); file paths/bindings tương đối workspace, tool arguments giữ thực tế (referenced_image_paths thường là tuyệt đối). Selection receipt chỉ trỏ path/hash; actual inputs có thứ tự path/hash, asset_id nếu từ catalog, kind và purpose. Với ảnh user ngoài catalog, asset_id=null, ghi nguồn user trong INPUTS, không tự đăng ký shared. Không tải ảnh ngoài chỉ từ một URL lead.

Trước reserve chạy `python scripts/asset_catalog.py inputs-check <workspace-relative-record> --project-id <ID>` với outcome=not_submitted, output=null; đây là kiểm khai báo/binding, không gọi tool. Sửa lỗi trước gửi. Reserve theo image_budget hiện có; ghi call_id/cycle_id vào hồ sơ rồi kiểm binding sát call trước gửi. Nếu thay đổi/pending thì xử lý đúng sổ, không tự hoàn lượt đã gửi hay reset cycle. Tool thật vẫn phải được gọi bằng cơ chế ảnh hiện hành, không phải chỉ ghi JSON.

Kết quả call: lưu bản receipt mới có outcome thật, output path/hash khi nhận được, cùng evidence/tool result theo attempt; giữ preflight, không sửa lịch sử. Tên model không công bố ghi unknown. Không giả thông số tool hoặc giới hạn ảnh. Ảnh không có local path dùng cơ chế hội thoại được imagegen hỗ trợ; ghi nguồn/giới hạn và kiểm thủ công, không bịa hash. inputs-check sẽ báo needs_review cho cơ chế hội thoại vì không xác minh được bằng local-path checker; có thể dùng handoff schema2 với asset_inputs_status unverified và review riêng, không giả schema3 matched.

## QA và handoff

Kiểm ảnh output thật theo first-frame và Project: nhận dạng, cỡ/biến thể có căn cứ, anatomy/assembly/tiếp xúc, t=0, tỷ lệ/bố cục/cảnh, không lọt chữ/nền thư viện. Không coi input đã gửi là model đã tuân thủ. Budget tối đa 5 call/cycle như cũ; dừng khi đạt, xin thêm khi hết chưa đạt.

Handoff mới schema3 có `asset_inputs` path/hash (tương đối workspace) trỏ receipt của call sinh ra ảnh được chọn, call_id/cycle_id khớp. Receipt output phải trùng ảnh/handoff. `reference_requirements_sha256` là SHA canonical JSON của danh sách requirements có applies_to=first_frame/both lấy từ resolve; không đưa video-only vào hash mở đầu. Với brief ảnh trực tiếp chưa có bộ nội dung, lưu requirements và review local; trước dùng vào bộ video phải đối chiếu nguồn/t=0 theo quy tắc legacy hiện hành, không bịa source_attempt.

`inputs-check --historical` chỉ kiểm khai báo input đã pin và file/output hash, không bắt metadata catalog hiện tại phải giữ nguyên. `check-frame` báo riêng asset_inputs_status: schema2 cũ có thể matched về frame binding nhưng asset provenance vẫn unverified; schema3 thiếu/sai actual input là invalid. Hash/receipt không tự chứng minh dispatch, perception hoặc người dùng duyệt. Không backfill lịch sử hoặc thay user selection.

## Thiếu và thay đổi

Ref hỗ trợ mà Knowledge đủ: có thể làm không ảnh, ghi rõ và QA thật. Ref thiết yếu giữ nhân vật/cấu hình còn thiếu thì hỏi đúng phần thiếu trước call. Stage không liên quan không tự gán adult hoặc biến needs_review thành matched; cần scoped review/metadata có căn cứ. Helper unavailable thì kiểm trực tiếp, ghi unverified phần tự động. File/parent/metadata đã chọn đổi: kiểm lại phần liên quan, tạo receipt mới. Thêm asset không liên quan không bắt đọc lại toàn kho.
