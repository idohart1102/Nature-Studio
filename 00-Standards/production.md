# Quy trình sản xuất — v1.6

Updated: 2026-10-17 | Mã XX-YYYY từ Nature Studio v2.0.0.

Clonevideo — 2026-10-17: chuyển thể theo reference-video-adaptation.md, dùng video-prompt-workflow.md và helper chung. Phân tích mẫu không cấp ID; bộ nội dung chuyển thể mới đủ brief thì cấp mới, revision dùng ID cũ. Research/INPUTS ghi nguồn/coverage/hash analysis/brief/mapping và những thay đổi so với mẫu; ledger ghi reuse có chủ đích. Không ép chuyện khác mẫu để đạt novelty; các gate thực tế và Project vẫn giữ. Hồ sơ tham chiếu ở .nature-studio/references hoặc production local, không publish.

Plan 01 — 2026-10-17: /na-chayvideo được lấy nguồn theo task packet và tra lịch sử bằng chỉ mục có hash. Tạo mới đọc creativity/Story Development; revision giữ chuyện; caption-only chỉ nguồn liên quan. Không bắt đọc lại nguồn nguyên vẹn đã có trong phiên. Index không thay nguồn gốc: đọc hồ sơ chưa có fingerprint/hết hạn và trường hợp gần nhất; không dùng tìm từ khóa để chứng nhận mới. Helper chỉ kiểm cú pháp/lưu attempt, không thay tự kiểm nội dung hoặc hồ sơ/ledger.

## Trước sản xuất

- Đọc brief, đúng dự án và output-contract; phân biệt tạo mới với sửa sản phẩm cũ.
- Tra kiến thức, giới hạn model và bài học active liên quan; kiểm idea-ledger. Không bắt buộc phải có bài học cũ mới làm.
- Tạo vài hướng trong quá trình phát triển, chọn hướng phù hợp yêu cầu; giữ ý tưởng đã chốt khi chỉ sửa cục bộ. Tránh lặp cơ chế/key/kết cục chỉ bằng thay tên loài hoặc màu mồi.
- Khóa trạng thái đầu, chuỗi lực, diễn biến và hậu quả; áp nhịp riêng của dự án. Không thay chân thực bằng tính gây sốc.

## Hồ sơ và ID

- Video mới theo [quy tắc mã](video-identifiers.md): XX-YYYY, hai chữ riêng Project local và bốn số từ 0001. Dùng scripts/video_ids.py init/reserve, registry local và IDENTITY.json; không tự thêm hậu tố thời gian hoặc đoán mã. Revision dùng mã cũ và attempt mới; giữ nguyên ID legacy.
- Mỗi production có brief/research/concept/feedback/performance/SUMMARY theo template; mỗi attempt A01, A02... giữ inputs, prompt, settings, review và media thực sự có.
- INPUTS ghi đường dẫn và phiên bản, ảnh input chính xác và hash nếu công cụ có; ghi model/giao diện/thông số thực sự dùng. Không đoán seed hoặc setting ẩn.
- Viết prompt không đồng nghĩa sinh ảnh/video. Chỉ lưu file media khi thật sự có; không tạo file rỗng giả render. Không tạo clip hoặc lượt trả phí ngoài phạm vi giao việc.

## Sau lần thử

- Review đúng vật đã truy cập; phân biệt lỗi ở brief, dữ kiện, ảnh đầu, prompt, model, setting hoặc hậu kỳ. Không kết luận nguyên nhân duy nhất nếu chưa tách biến.
- Khi so sánh, giữ điều kiện khác ổn định khi khả thi; ghi chính xác thay đổi và đánh đổi.
- Cập nhật SUMMARY và idea-ledger bằng thông tin cần tra nhanh, liên kết bài học thay vì sao chép.
- Chỉ cập nhật quy chuẩn/bộ nhớ theo memory-policy; số view không thay thế QA kỹ thuật.

Cập nhật 2026-10-16: đơn vị quản lý là Project; đọc Slug trong PROJECT.md để ghi `04-Productions/<slug>/`. Không suy thư mục từ ID ổn định sau đổi tên. Production ID cũ tiếp tục dùng cho lịch sử/revision; video mới theo chuẩn XX-YYYY từ v2.0.0 và prefix local (thay chuẩn XXX-yyyyy ban đầu), không đổi mã vì đổi tên dự án.

## Tổng kết phiên và vòng học — v1.2, 2026-10-16

/na-dongvideo dùng SESSION-REVIEW.md theo mẫu để tổng kết phần dữ liệu đã truy cập; luôn đánh giá riêng Project và shared. Không tự đóng từ /na-chayvideo, không nhầm đóng phiên với selected/QA pass. INPUTS ghi ID/version/cách áp dụng lesson để lần sau đối chiếu kết quả. Thẩm quyền đổi trạng thái chỉ theo memory-policy, không biến giả thuyết thành quy chuẩn.

## Story Development — 2026-10-16

Trước khi chọn concept mới, thực hiện [story-development.md](story-development.md) cùng creativity và phần áp dụng Project nếu có. Ghi story card vào concept hiện có; không đổi số mục đầu ra. Sau render kiểm hình/âm thật, sau đăng mới kiểm giả thuyết khán giả. Không tự tạo production hoặc cấp mã khi chỉ sửa phương pháp hệ thống.

## Riêng tư khi cập nhật hệ thống

Production, attempt, SESSION-REVIEW và idea-ledger giữ local theo publication.md. Repo chỉ phân phối mẫu ledger. /na-chayvideo vẫn rà lịch sử local và ghi đầy đủ; tách bài học tái sử dụng sang Memory, không dùng việc đồng bộ hệ thống để tự upload toàn bộ lịch sử.

## Sinh ảnh theo /na-taoanh

Khi được giao tạo ảnh thật, theo first-frame.md và skill na-taoanh; không khởi chạy từ /na-chayvideo. Một video giữ ID qua các attempt, quota ảnh theo cycle riêng. Mỗi call ghi prompt/settings/input/output/hash/QA, dùng image_budget.py reserve trước gửi; call lỗi cũng tính. FIRST-FRAME.json chỉ trỏ ảnh QA pass, không sửa provenance các attempt video cũ. Dữ liệu vòng ảnh và quota giữ local, tách lesson theo policy.

## Kiểm–lưu và asset — v2.1.0

Attempt mới giữ checks/contract version và binding ngoại lệ khi có; check/save dùng cùng gate. Planned asset_selection nằm ngoài frame_state bốn key; resolve mới nhất không tự là actual input của render. CURRENT-STATE schema2 gắn QA vào reviewed_render/coverage và approval vào selected_render, giữ legacy unverified. Không cấp ID thử khi nâng hệ thống, tạo catalog hay làm ảnh thư viện độc lập. Xem lõi workflow và templates khi cần ngoại lệ.
