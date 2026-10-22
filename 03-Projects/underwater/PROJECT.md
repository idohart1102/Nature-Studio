# Underwater

ID: under-fishing-us
Slug: underwater
Version: 2.6 | Updated: 2026-10-22 | Nguồn theo giai đoạn; giữ UF-D021; hook 3 giây đầu UF-D025
Aliases: Under Fish US; Under Fishing US; Under Fishing
Routing: Video/prompt tương tác cá–mồi dưới nước, khán giả câu cá Mỹ; săn mồi tự nhiên hoặc bait/lure/rig/jig; mọi loài cá được câu phù hợp tại Mỹ, không giới hạn Redfish/red drum/Sciaenops ocellatus, Muskie/muskellunge/Esox masquinongy, Walleye/Sander vitreus. Camera chìm cầm tay chuyển động nhẹ tự nhiên, dọc 10s và key sau 5s là dấu hiệu kết hợp. Một từ cá/Mỹ/Omni hoặc nhắc benchmark Underfishing riêng không đủ phân biệt dự án.
Model: omni-flash

UF-D020 — 2026-10-17: /na-clonevideo dùng [chuẩn chuyển thể](../../00-Standards/reference-video-adaptation.md) và lõi prompt chung. Reference giữ cơ chế mẫu có chủ đích, ánh xạ đúng loài/bối cảnh mới; ngưỡng độ mới dành cho concept độc lập không ép thay câu chuyện của bản chuyển thể. Quy chuẩn kỹ thuật/QA/âm/caption hiện hành vẫn áp dụng, khác biệt camera/nhịp so với mẫu phải ghi rõ.

UF-D021 — 2026-10-17: người dùng thay mặc định camera cố định bằng camera chuyển động nhẹ, tự nhiên như người cầm điện thoại quay. Áp dụng [camera cầm tay](format.md#camera-cầm-tay-tự-nhiên--uf-d021) cho bộ mới và revision được giao; tham chiếu học quan hệ máy–chủ thể, không đổi thành cá tự quay. Không sửa media/attempt lịch sử hoặc tự render.

UF-D025 — 2026-10-22: 3 giây đầu phải giữ người xem theo [Hook 3 giây đầu](format.md#hook-3-giây-đầu--uf-d025); 5–10 beat, beat đầu ≤3.0s, `checks.hook_signal` ≤3.0s; key vẫn onset >5.0s. Không chia mô tả thành giai đoạn cố định.

## Nguồn hiện hành

- [Format](format.md), [hợp đồng đầu ra](output-contract.md), [khán giả/caption](audience-and-caption.md).
- Tạo concept mới phải đọc [Sáng tạo mở](creative-direction.md), [Story Development](story-development.md) cùng hai hướng dẫn chung tương ứng ở 00-Standards. Revision giữ ý định.
- [context-map.json](context-map.json) chọn nguồn theo nhiệm vụ; workflow skill quy định cách đọc và fallback, không coi packet là nguồn quyền mới. [decisions.md](decisions.md) giữ lịch sử; đọc khi truy nguyên/mâu thuẫn, không nạp mọi quyết định mỗi lượt. Baseline v1.9 chỉnh từ v1.7, không dùng v1.8; bản nhập giữ nguyên ở 07-Releases/standalone-guides.
- [context-routing.json](context-routing.json) chia nguồn theo giai đoạn và phụ thuộc; sửa/thêm Knowledge qua map/cấu hình, không sửa skill. Fullset đủ brief ưu tiên all + view; đầu vào chưa rõ có thể orient/concept trước. Nguồn chưa phân loại không được bỏ; coverage không thay QA nội dung.
- Knowledge: môi trường/quang học, đúng loài/tương tác và dụng cụ khi có câu cá. Thiếu loài trong kho thì tự nghiên cứu hồ sơ đúng loài, không thay tên trong hồ sơ Muskie. Research 20 Reel được khuyến nghị để hiểu/phát triển chứ không giới hạn sáng tạo.

## Chọn loài

Đã có loài/quyền chọn thì không hỏi lại. Thiếu thì hỏi một câu: **Redfish / Muskie / Walleye / Loài cá được câu bất kỳ ở Mỹ**, cho nhập loài khác. Dùng lựa chọn click nếu công cụ hỗ trợ (có thể gộp trong giới hạn số lựa chọn của công cụ), nếu không thì lựa chọn chữ; không giả nút Markdown. Chờ đáp án thật, lựa chọn sẵn không là xác nhận. “Bất kỳ” cho phép tự nghiên cứu/chọn loài và vùng phù hợp. Không hỏi chọn cá khi chỉ sửa skill.

## Runtime và bộ nhớ

Production: `04-Productions/underwater/`; idea-ledger.md local tại thư mục Project. Thiếu ledger không có nghĩa không có lịch sử. Mã mới qua scripts/video_ids.py reserve underwater theo video-identifiers.md; prefix riêng local, không ghi cứng. Giữ UF legacy khi revision.

Theo [truy xuất chọn lọc](../../00-Standards/memory-retrieval.md), query Memory Project/shared theo nhiệm vụ/hint, mở active gốc phù hợp; xét unknown/legacy và các trang còn lại, không nạp toàn bộ INDEX theo memory-policy. Ghi ID/version/đường dẫn/cách dùng vào INPUTS; candidates chỉ thử riêng, không tự active. /na-dongvideo đóng phiên theo skill riêng; không tự đóng từ /na-chayvideo.

Tạo ảnh thật qua /na-taoanh theo [first-frame-qa.md](first-frame-qa.md) và gate chung; tối đa 5 call/cycle, quota/handoff/hash local được bảo toàn. Không tự sinh media từ việc viết prompt. Danh tính model ảnh không chặn QA, không giả chọn Sunburst. Production/ledger/registry/media riêng không publish; lesson đi theo publication policy.

Profile loài chọn điểm thật đáng xem và cỡ có căn cứ, không là danh sách tình huống đóng. Khi cần ref, dùng catalog chung theo entity/stage/role ở [knowledge-routing](../../00-Standards/knowledge-routing.md); metadata/planned ref không chứng minh ảnh hoặc render đã đạt. Không tải cả thư viện hoặc gán luật Underwater cho Project khác.

Asset v2.1.1: dùng ID Project hiện hành khi query/select; nguồn chung theo [quy trình](../../00-Standards/first-frame-asset-references.md). Không áp quy tắc Underwater cho Project khác; ref t=0/video tách riêng, ảnh nền trắng chỉ là bản thư viện.

## Địa điểm và sinh cảnh — UF-D023

Áp dụng [chuẩn chung](../../00-Standards/location-context.md). Bộ nội dung mới/reference chọn vùng Mỹ có phân bố xác nhận và sinh cảnh phù hợp, theo descriptor của profile loài; mức ưa chuộng câu cá chỉ ưu tiên phụ. Khóa một setting cho ảnh/video/caption, không giới hạn năm vùng mỗi loài. Caption mỗi bản có đúng một hashtag địa điểm trong tổng 3–5 tag; không đoán vùng từ ngoại hình nền. Revision giữ lựa chọn cũ nếu chưa được giao đổi; legacy chưa có địa điểm không tự backfill.
