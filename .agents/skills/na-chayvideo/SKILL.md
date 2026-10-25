---
name: na-chayvideo
description: Tạo hoặc sửa bộ nội dung video Nature Studio khi gọi /na-chayvideo hoặc yêu cầu làm video qua đặc trưng dự án. Tự nhận dự án, nghiên cứu đúng loài/tình huống, rà trùng; ý tưởng Việt, prompt Anh, caption Mỹ kèm hashtag. Không tự render/đăng; không kích hoạt từ câu hỏi kiến thức, trích dẫn hoặc sửa skill.
---

# /na-chayvideo

Version: 2.15 | Updated: 2026-10-25 | Mồi câu tra theo mã thư viện mồi; bài học là cổng QA (kể cả Chờ duyệt), QA tối đa 5 vòng reviewer độc lập, khám phá có chủ đích

Gốc workspace chứa START-HERE.md, đi lên ba cấp từ thư mục skill; không ghi cứng ổ đĩa. Đọc START-HERE.md và SYSTEM.md trước công việc; trong cùng phiên không cần nạp lại nguồn nguyên vẹn đã đọc. Yêu cầu hiện hành của người dùng ưu tiên trong phạm vi được giao.

## Định tuyến

1. Chọn chế độ: **new** cho concept mới; **revision** cho sửa/tiếp tục clip đã có; **caption** khi chỉ sửa caption. Giữ loài/câu chuyện đã chốt khi revision; caption không chạy lại brainstorm, timeline hay cấp mã. Thay đổi liên quan sinh thái/rig/model phải mở lại nguồn tương ứng.

   Yêu cầu học cách quay/hành động/kịch bản từ video mẫu, kể cả đổi đối tượng, dùng [na-clonevideo](../na-clonevideo/SKILL.md) và nhánh **reference**. Không chạy đồng thời cả new và clone. Nhánh [reference](references/reference.md) dùng cùng lõi/output/Project, không ép đổi câu chuyện để đạt độ mới.
2. Chạy `python scripts/chayvideo_context.py projects`. Catalog đọc metadata hiện hành mọi PROJECT.md; mở bản gốc khi metadata thiếu/mơ hồ. Ưu tiên tên/ID được chỉ định, rồi tổ hợp chủ đề/loài/môi trường/thị trường/format/ngữ cảnh. Không chọn chỉ bởi “cá/Mỹ/Omni”, không ép vào dự án duy nhất khi không phù hợp. Chỉ hỏi khi thật sự chưa phân biệt được.
3. Đọc [workflow](references/workflow.md) và đúng một nhánh: [tạo mới](references/new.md), [revision](references/revision.md), [caption](references/caption.md). Dùng `preflight` → `view --ledger` → coverage theo lệnh trong lõi chung; không nạp JSON rồi đọc lại từng file. Thiếu cấu hình hoặc ảnh hưởng chưa rõ thì mở nguồn toàn nhánh. [Hướng dẫn cấu hình](../../../00-Standards/context-routing.md) chỉ cần khi thêm nguồn/bảo trì hoặc dùng tuỳ chọn chưa rõ.

## Bất biến

- Bộ nhớ theo [lõi truy xuất](../../../00-Standards/memory-retrieval.md): descriptor Project + shared theo nhiệm vụ/hint trước, mở gốc phù hợp sau; không nạp toàn bộ INDEX/active. Unknown/legacy và trang còn lại phải được xét, candidate không là luật.

- Mặc định một bộ bốn mục: **Ý TƯỞNG** tiếng Việt; **FIRST FRAME PROMPT**, **VIDEO PROMPT** tiếng Anh; **CAPTION** theo hợp đồng Project. Underwater trả Chuẩn/Hài hước/Tò mò; mỗi bản đúng thứ tự caption EN + hashtag → lược dịch caption VI → hook text EN 1–9 từ → lược dịch hook VI. Viết trực tiếp giọng người câu cá Mỹ, rồi lược dịch; loại văn dịch/slang hoặc câu đùa gượng. Mỗi prompt và từng caption là một đoạn riêng. JSON giữ `caption` chuỗi, thêm `caption_variants`/`caption_variant` theo template; không nhét cả ba bản vào một chuỗi caption. Sửa đúng phần được giao; chi tiết giọng/hashtag theo nguồn Project, không áp luật Underwater lên Project khác.
- Tạo mới phải đọc creativity/story-development chung + Project; nghiên cứu đúng loài/vùng/tình huống. Ví dụ không là danh mục đóng. Độ mới xét hành vi/nhân quả, không đổi tên loài/màu/địa danh rồi lặp chuyện.
- Packet/index tạo lại được, không cao hơn nguồn gốc. Không cắt yêu cầu để đạt ngân sách token; thiếu/stale/coverage chưa đủ thì đọc thêm. Không bịa nguồn hoặc đã xem/nghe/đo/QA.
- Áp bài học theo [memory-policy v2.2](../../../00-Standards/memory-policy.md#kênh-duyệt-sheet-và-bài-học-làm-cổng-qa--v22-2026-10-25): query kèm `--candidates`; Ràng buộc Đã duyệt bắt buộc đạt, Ràng buộc Chờ duyệt bắt buộc xét, Định hướng sáng tạo chỉ tham khảo. Ghi ID/version/path/applied hoặc lý do không áp dụng; không tự active candidate ngoài gate. Bảo toàn registry/media/quota ảnh/FIRST-FRAME.json/lịch sử; không tự /na-dongvideo hoặc /na-taoanh.
- Chỉ văn bản và hồ sơ local. Media/chi tiền/đăng/push cần yêu cầu tương ứng; sửa skill không là sản xuất. Thiếu brief không reserve mã/lưu ý tưởng giả.

## Phiên làm việc

Mỗi video đi theo pha, mỗi pha một chat: tạo bộ → ảnh (/na-taoanh) → loạt sửa. Mỗi lượt sửa ghi ngay một mục feedback.md theo [mẫu](../../../00-Standards/templates/feedback.md): lời người dùng nguyên văn, cách hiểu, phạm vi, phần đã chốt, phương án đã loại kèm lý do, việc còn mở. Sau khoảng 5 lượt sửa trong cùng chat, hoặc khi việc chuyển sang sửa hệ thống, đề nghị mở chat mới và in sẵn câu nối, ví dụ `/na-chayvideo sửa <ID> <attempt>: <việc còn mở>`. Chat mới đọc feedback.md, SUMMARY và CURRENT-STATE (nếu có), chạy resolve, rồi đọc lại nguồn theo lõi chung; không dựa vào trí nhớ chat cũ.

Tự xác định nhu cầu asset từ brief, lưu reference_requirements trong OUTPUT/INPUTS theo [lõi chung](../../../00-Standards/video-prompt-workflow.md): đối tượng/biến thể, đặc điểm cần giữ, role và first_frame/video/both. Có thể ghi không cần với lý do. Query metadata đúng Project khi cần, chỉ mở ảnh để giải quyết chi tiết thị giác; ID gợi ý là planned, không giả đã truyền ảnh. /na-taoanh sẽ kiểm lại và chọn input thật. Revision ghi nhu cầu còn hiệu lực, caption-only giữ binding không tra asset. Thư viện không giới hạn ý tưởng; không đổi chuyện vì thiếu ảnh, không nạp cả catalog hoặc thêm mục vào bốn phần trả lời mặc định. Cảnh có mồi: chọn một mã/biến thể từ `baits` của packet theo [chuẩn hồ sơ mồi](../../../00-Standards/bait-profile-standard.md), ghi vào requirement và prompt đúng mồi đó; chỉ mở hồ sơ mồi đã chọn.

Máy mới hoặc catalog thiếu bộ ref đi kèm: nếu có `08-Assets/reference-library.json`, chạy `python scripts/asset_catalog.py import-bundle 08-Assets/reference-library.json` trước khi báo thiếu, rồi query đúng Project. Không nạp cả manifest vào context hoặc tự ghi đè ID xung đột.


Khi Project cần địa điểm thực, dùng [chuẩn địa điểm](../../../00-Standards/location-context.md): profile loài → descriptor đúng loài → hồ sơ vùng chọn; khóa setting trong INPUTS và frame_state.environment. Underwater yêu cầu một hashtag địa điểm trong tổng 3–5 tag mỗi caption khi setting đã xác nhận; caption-only/legacy thiếu setting xử lý theo nguồn Project, không đoán vùng.

## QA và bài học — v2.14

Trước khi viết: chạy `python scripts/memory_retrieval.py query <slug> --mode <mode> --entity ... --interaction ... --candidates --out .nature-studio/memory/<ctx>-query.json`, đọc hết trang/unknown, mở gốc bài có thể áp dụng; nếu có sheet combo (`.nature-studio/combo/config.json`) thì chạy `python scripts/combo.py pull` và `apply-user` trước để trạng thái người dùng vừa duyệt có hiệu lực. Dựng bảng tiêu chí theo [quality-review v1.2](../../../00-Standards/quality-review.md#qa-nhiều-vòng-có-bài-học--v12-2026-10-25): tiêu chí gốc + độ mới + độ hay + từng bài học kèm cách kiểm.

Sau khi viết và helper `check` đạt: QA tối đa **5 vòng** bằng reviewer độc lập (Agent tool, context mới tách khỏi người viết, có thể giữ cùng reviewer qua các vòng của một bộ theo quality-review v1.3; chỉ đưa bảng tiêu chí, JSON đầu ra và đường dẫn nguồn, không đưa lập luận). Reviewer trả pass/fail từng tiêu chí, lỗi cụ thể, hướng sửa; sửa đúng lỗi, chạy lại helper rồi gửi vòng sau. Dừng sớm khi mọi tiêu chí bắt buộc pass. Hết 5 vòng chưa đạt: giữ bản tốt nhất, ghi "CHƯA ĐẠT" và lỗi còn lại trong review.md/sheet, không hạ chuẩn hay đổi chuyện đã khóa để lách. Không có Agent tool thì tự QA và ghi giới hạn self-review.

Khám phá theo [creativity.md](../../../00-Standards/creativity.md#khám-phá-có-chủ-đích--2026-10-25): xét `03-Projects/<slug>/idea-bank.md` trước khi phát triển tiền đề; lượt ≥3 bộ có ≥30% suất Khám phá + 1 suất Thử nghiệm; ghi tiền đề tốt chưa dùng vào idea-bank. Hướng chủ đề do người dùng giao từng lượt; không mặc định câu cá bằng mồi hay săn mồi tự nhiên.
