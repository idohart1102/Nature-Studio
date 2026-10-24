---
name: na-taoanh
description: Tạo hoặc sửa ảnh first frame Nature Studio khi gọi /na-taoanh, “tạo ảnh”, “tạo first frame” với ý định tạo media trong Project; QA ảnh thật sau mỗi lượt, tối đa 5 lượt rồi xin thêm. Không kích hoạt khi chỉ hỏi, trích dẫn, viết prompt hoặc sửa skill; ảnh ngoài dự án dùng luồng tạo ảnh thông thường.
---

# /na-taoanh

Version: 1.11 | Updated: 2026-10-25 | Checklist hình ảnh của hồ sơ loài v3 là tiêu chí QA; ảnh thật làm ref nhận dạng

Quy ước trong chat, không cam kết giao diện đăng ký slash command. Dùng workspace chứa skill làm gốc (đi lên ba cấp từ thư mục skill). Tổng kết/QA tiếng Việt; prompt thực thi tiếng Anh một đoạn. Skill này tạo ảnh, không tạo video. Chỉ xây/sửa skill không phải yêu cầu chạy sinh ảnh.

## Xác định đúng đầu vào

Đọc START-HERE.md, SYSTEM.md, `00-Standards/first-frame.md`, production/quality-review/memory-policy và `02-Models/model-profiles/sunburst-imagegen.md`. Khi thực thi qua image_gen, dùng skill imagegen sẵn có theo catalog để tuân thủ cơ chế tool, ảnh tham chiếu và lưu file; qua 9router thì theo mục Tuyến 9router bên dưới. Không cần công cụ ảnh khi chỉ chỉnh tài liệu.

Ưu tiên Project/mã video/attempt được nêu. Tra metadata Project và production thực, không chọn theo ngày file hoặc mã chữ đơn lẻ. “Tạo ảnh” trong ngữ cảnh rõ một video là lời gọi; câu hỏi, trích dẫn, yêu cầu viết prompt không kích hoạt. Yêu cầu ảnh ngoài Project không bị ép vào Underwater; chuyển luồng imagegen thông thường hoặc hỏi mục đích khi mơ hồ. Không mặc định mọi ảnh trong workspace là first frame.

Đọc brief/concept/FIRST FRAME PROMPT, INPUTS, feedback, ảnh và review hiện hành cùng các file Project dẫn tới. Tìm lesson active của Project và shared đúng điều kiện, ghi ID/version/cách dùng. Với Underwater đọc `03-Projects/underwater/first-frame-qa.md`. Hồ sơ loài trong ảnh lấy bằng `python scripts/species_profiles.py resolve "<tên>"` (chỉ mở đúng hồ sơ đó); mục 7 Checklist hình ảnh là tiêu chí QA bắt buộc, `entity_id` là `id` của hồ sơ khi tra ref. Ưu tiên ref `origin: photo` cho identity/anatomy; ảnh AI chỉ hỗ trợ production. Giữ lựa chọn người dùng và câu chuyện đã chốt; không sáng tác production mới hoặc đổi loài/kết cục để sửa ảnh dễ hơn. Thiếu concept quan trọng thì hoàn thiện trong phạm vi đã giao hoặc hỏi trước khi sinh. Video mới chỉ cấp ID bằng video_ids.py khi nhiệm vụ thật đòi production mới và đủ brief; revision không cấp video ID mới.

Ghi bản khóa đầu vào: t=0, chủ thể/số lượng/nhận dạng/tỷ lệ, môi trường, camera, vị trí/quan hệ/đường chuyển động cần cho video và tiêu chí bắt buộc. Tách ảnh đích sửa, reference và supporting input; mở từng ảnh local cần dùng bằng view_image trước khi sửa. Mâu thuẫn hoặc dữ kiện chưa có cơ sở phải xử lý trước khi tiêu lượt.

Mặc định prompt và QA theo [màu tự nhiên/cân bằng trắng](../../../00-Standards/first-frame.md#màu-tự-nhiên-và-cân-bằng-trắng): hạn chế ám vàng/cam mạnh toàn ảnh, giữ màu chuẩn của đối tượng; đối tượng vàng không là lý do phủ vàng cả cảnh. Không tự thêm golden-hour/amber/sepia grade, không khử vàng bằng ám xanh hoặc làm mất màu thật. Chỉ dùng tông ấm có chủ đích khi brief yêu cầu và nguồn sáng/bối cảnh phù hợp; QA màu trên output thật, sửa có mục tiêu trong budget hiện hành.

## Công cụ và ưu tiên Sunburst

Tra bài học theo [lõi truy xuất](../../../00-Standards/memory-retrieval.md) với task `image-generation` và `image-review`, hint từ brief; luôn kèm `--candidates` theo [memory-policy v2.2](../../../00-Standards/memory-policy.md#kênh-duyệt-sheet-và-bài-học-làm-cổng-qa--v22-2026-10-25); đọc descriptor rồi mở gốc phù hợp, không nạp toàn bộ INDEX. Ràng buộc Đã duyệt thành tiêu chí QA ảnh bắt buộc đạt; Ràng buộc Chờ duyệt bắt buộc xét (áp dụng hoặc ghi lý do); candidate vẫn không là kết luận đã xác nhận. Ghi bài đã áp dụng trong INPUTS/review. Giữ nguồn/quota/handoff như phần dưới.

Khi dùng bộ nội dung đã có, resolve đúng attempt và đối chiếu frame_state theo lõi chung. Tái dùng ảnh đã QA phải theo [kiểm liên kết ảnh](../../../00-Standards/first-frame.md#kiểm-liên-kết-ảnh-trước-tái-dùng). matched chỉ là liên kết hồ sơ khớp; vẫn xem/đo ảnh như skill yêu cầu. Khi ghi handoff mới dùng schema 3 theo phần asset bên dưới, phân biệt attempt ảnh với source_attempt nội dung; giữ review/handoff trước, không tự nâng hồ sơ cũ hoặc sinh lại chỉ vì cần kiểm lại.

Model ưu tiên: **GPT Image 2.5 Sunburst**. Thứ tự tuyến (người dùng đã cho phép, không hỏi lại):

1. **Built-in `image_gen`** (Codex) khi môi trường có tool này. Nếu schema có selector và hỗ trợ Sunburst thì chọn Sunburst; nếu không, dùng model mặc định của image_gen và tiếp tục.
2. **9router Sunburst** khi không dùng được image_gen: môi trường không có tool (ví dụ Claude Code) hoặc tool báo lỗi không khả dụng/không được phép. Gọi qua `scripts/image_9router.py`, model `cx/gpt-image-2.5-sunburst`. Lỗi nội dung/ảnh xấu của image_gen không phải lý do đổi tuyến giữa cycle; ảnh xấu thì sửa prompt.

Không dùng CLI/API khác, không tự chỉ định Flare để thay thế. Tên Sunburst trong prompt không chọn backend; không bịa model/seed/quality ẩn. Một cycle giữ một tuyến; đổi tuyến giữa chừng phải ghi lý do trong attempt và vẫn dùng chung bộ đếm.

Người dùng đã cho phép dùng model mặc định nếu không tìm được Sunburst. Danh tính model không phải tiêu chí QA hoặc cổng chặn sinh ảnh. Không công bố model không làm ảnh fail và không cần xin quyền riêng cho backend unknown.

Ghi requested_model=Sunburst, selection_mode=sunburst nếu chọn được, tool_default nếu dùng mặc định image_gen, hoặc 9router_sunburst; actual_model lấy từ công bố thực, nếu không có thì unknown và model_verified=false. C2PA của ảnh 9router chỉ ghi `gpt-image` chung nên không chứng minh Sunburst. Không nhận đã dùng Sunburst khi chưa có căn cứ. Không cần khóa API cho built-in. Cả hai tuyến đều lỗi/không có thì báo trạng thái và dừng; không retry vô hạn.

### Tuyến 9router

Kiểm trước, không tốn lượt: `python scripts/image_9router.py check` (gateway `http://localhost:20128/v1`, khóa trong `NINEROUTER_API_KEY` hoặc `.nature-studio/9router.key`, đều là dữ liệu local, không đưa vào prompt/hồ sơ/repo). `ready=false` thì báo người dùng mở 9router hoặc cấp khóa; không tự tạo/đổi khóa trong 9router.

Sau `reserve`, mỗi lượt gọi đúng một lệnh: `python scripts/image_9router.py generate --prompt-file <Axx>/prompt.txt --out <Axx>/<file>.png [--image <ảnh 1> --image <ảnh 2> ...] --size 1024x1536`. Thứ tự `--image` là thứ tự image1, image2... mà prompt nhắc tới; có ảnh thì backend chạy edit, không có thì generate. Script không ghi đè, lưu `<file>.9router.json` (khối `tool` tên `9router_image` với prompt và `referenced_image_paths` theo thứ tự, hash input/output, kích thước thực, latency, outcome); khi ghi actual-input theo quy trình asset, chép khối `tool` này, `asset_catalog.py` chấp nhận cả `image_gen` và `9router_image`. Khóa không được ghi. Mã thoát khác 0 vẫn là lượt đã gửi: `finish` theo outcome trong record (`unknown` khi timeout vì backend có thể vẫn chạy, tra trước khi gọi lại).

Đặc tính đã đo 2026-10-25 (11 call, 10 thành công, 1 lỗi cố ý sai model): generate ~30 giây, edit có ảnh tham chiếu 2,5–5 phút; edit cục bộ giữ cảnh tốt. **`size` không được tôn trọng**: khổ ảnh theo câu chữ prompt. Prompt ghi `tall vertical 9:16 aspect ratio frame` cho ra 941x1672 (2/2 lần, lệch 9:16 ~0,05%, trong dung sai first-frame.md); chỉ ghi `vertical`/`portrait` cho ra 1024x1536 (2:3); không ghi khổ có thể ra 1536x1024. Vì vậy prompt luôn ghi rõ tỷ lệ đích, vẫn đo file thật; sai khổ là fail và tính lượt. Không đặt `--quality low/medium` để tiết kiệm. Gọi sai model có thể làm 9router khóa model đó trên tài khoản 30 phút; chỉ dùng model mặc định của script.

## Vòng sinh/sửa và QA

1. Khởi tạo/đọc cycle ở production bằng `python scripts/image_budget.py init --production 04-Productions/<slug>/<video-id>`. Cùng vòng sửa đang dở tiếp tục bộ đếm cũ; không reset bằng đổi chat, mã attempt hoặc gọi lại lệnh. Chỉ `new-cycle` khi người dùng giao ảnh/brief mới rõ ràng và có hồ sơ yêu cầu.
2. Nếu đang ở cycle đã đạt, đầu vào không đổi và không được yêu cầu revision, trả lại ảnh đã đạt, không tiêu thêm lượt. Nếu muốn sửa sau khi đạt, xác định quyền/phạm vi vòng mới, không tự mở vòng để vượt hạn mức.
3. Trước **mỗi** lần gửi image_gen/9router (tạo mới, edit hoặc tạo lại), tạo attempt mới theo production.md, lưu prompt/ảnh nguồn/INPUTS/settings và gọi `image_budget.py reserve --production ...`. Lưu call_id/cycle_id vào attempt. Được phép sinh chỉ khi reserve thành công. Tool call đã gửi tính một lượt kể cả lỗi/cancel/không có ảnh; pending không rõ có chạy phải giữ lượt, tra kết quả trước khi gọi lại. Một call là một ảnh đích; không yêu cầu nhiều variants để lách quota. Tool tự trả nhiều ảnh thì kiểm từng ảnh và ghi đúng, không gọi thêm ngoài budget.
4. Dùng công cụ ảnh thực của tuyến đã chọn, một lần gọi theo prompt có mục tiêu. Sửa cục bộ trên ảnh tốt nhất có căn cứ; lỗi nền tảng thì tạo lại từ prompt đã sửa. Không mặc định bản mới nhất là tốt nhất. Với image_gen dùng đúng cơ chế referenced_image_paths/num_last_images_to_include theo schema hiện hành, không đưa cả hai; với 9router truyền ảnh bằng `--image` theo thứ tự.
5. Copy output thực vào attempt local, giữ output gốc và hash; không ghi đè bản cũ. Mở ảnh output bằng view_image, kiểm toàn ảnh và chi tiết quan trọng. Không chấm ảnh từ prompt, thumbnail nhỏ hoặc tên file. Đo kích thước/tỷ lệ file, không coi “đã yêu cầu 9:16” là đã đúng. Công cụ đo/crop phục vụ quan sát; sửa pixel phải dùng công cụ ảnh của tuyến trừ khi người dùng chỉ định khác.
6. Chấm từng tiêu chí theo first-frame.md và Project: pass/fail/not_checked/not_applicable, quan sát cụ thể, severity, hướng sửa, kiểm hồi quy các phần đã đúng. Không lấy điểm đẹp tổng hợp bù lỗi giải phẫu/quan hệ/t=0. Kiểm bố cục hỗ trợ video, không đoán từ ảnh rằng chuyển động/audio sẽ đúng.
7. Nếu lỗi chặn hoặc tiêu chí bắt buộc chưa kiểm đủ: chưa đạt/chưa kiểm đủ. Chọn một nhóm lỗi ưu tiên và sửa có mục tiêu, ghi đánh đổi; kiểm lại toàn ảnh ở lượt sau. Lỗi lặp thì đổi chiến lược sửa hoặc ảnh nguồn mà giữ ý định; không hạ chuẩn, thêm che khuất/độ đục để giấu lỗi. Nếu đầu vào bất khả thi cần người dùng quyết định thì dừng sớm và báo, không phải dùng hết 5.
8. Nếu mọi tiêu chí bắt buộc pass, không còn lỗi chặn và ảnh đã được nhìn/đo thật: dừng ngay, ghi `qa_pass`, không cố dùng hết lượt. Ghi handoff bằng `python scripts/chayvideo_output.py handoff <source_attempt> --project <slug> --production <ID> --image-attempt <Axx> --image <Axx/file.png> --review <Axx/review.md> --qa-status qa_pass --width <px> --height <px> [--qa-source 03-Projects/<slug>/first-frame-qa.md] [--asset-inputs <file>] [--call-id <id> --cycle-id <id>] [--actual-model <tên công bố>] --promote`: helper tự tính mọi hash, ghi `<Axx>/FIRST-FRAME-HANDOFF.json`, chạy check-frame và chỉ chép sang FIRST-FRAME.json khi matched; không bao giờ ghi đè handoff cũ. user_approved=false trừ khi có phản hồi duyệt rõ. Ảnh sửa mới chưa đạt không tự thay con trỏ ảnh cũ đã đạt. Cập nhật prompt để khớp ảnh đã chốt; thay đổi ý định concept phải có quyền, không âm thầm đổi video prompt trái brief.

## Hạn mức và xin thêm lượt

Cycle mặc định tổng **5 lượt**, bao gồm lượt đầu và mọi edit/regenerate. Đọc/view/QA/sửa prompt văn bản không tính lượt. Budget helper chỉ quản lý sổ, không tự chặn tool; agent phải reserve trước mọi call. Không coi số Axx là bộ đếm ảnh. Mỗi video/ảnh đích có cycle riêng; nếu xử lý nhiều ảnh, chỉ thực hiện các đích được giao, không tự nhân batch.

Hết 5 chưa đạt: **không gọi lượt thứ 6**. Hiển thị bản tốt nhất nhưng gắn rõ chưa đạt/chưa kiểm đủ, báo số đã dùng, lỗi còn, thay đổi dự kiến và đề xuất số lượt bổ sung cụ thể. Hỏi: “Đã dùng 5/5 lượt, ảnh còn [...]. Tôi đề xuất thêm N lượt để [...]. Bạn có đồng ý không?”. Chờ câu trả lời thật; timeout/im lặng không là đồng ý. Chỉ sau đó lưu nguồn chấp thuận, gọi `grant --extra N --approval-file <file-relative-to-production>` và tiếp tục **cycle cũ**, dùng số tăng liên tục. Không tự tăng hạn mức hoặc mở cycle mới để lách quota. Nếu lần bổ sung hết vẫn fail thì lại dừng và xin số lượt mới.

## Hồ sơ và bàn giao

Theo mẫu `00-Standards/templates/first-frame-review.md`, giữ mỗi attempt INPUTS, prompt thực thi, settings, ảnh output thực, QA và mã quota. Log vào production `.image-qa.sqlite3`; đây là dữ liệu local. FIRST-FRAME.json ghi attempt/path/hash, qa_status, requested_model/actual_model/model_verified, user approval độc lập. Khi sinh/sửa không cần tự đổi user selection; AI QA pass không phải người dùng duyệt.

Trả ảnh inline + đường dẫn tuyệt đối, QA status/ảnh đạt ở attempt nào, số lượt dùng/còn, model thực xác nhận được và hạn chế quan trọng. Nếu chưa đạt thì chỉ rõ, không đặt tên “final/approved” để gây hiểu nhầm. Không tự tạo video, chi tiền ngoài tuyến đã được giao, đăng bài, commit hoặc push. /na-dongvideo tổng kết và xét bài học hai cấp; mọi runtime/ảnh/feedback/registry giữ local, bài học theo memory-policy/publication. Không tự active từ vòng sửa ảnh.

Sau call, ghi `image_budget.py finish --production ... --call-id <id> --outcome success|error|cancelled|unknown`; thao tác này không hoàn lượt. Handoff ghi bằng lệnh `handoff` ở bước 8 (trường theo 00-Standards/templates/first-frame-handoff.json); không lưu template rỗng như ảnh đạt. Mỗi lượt sửa ảnh theo yêu cầu người dùng ghi feedback.md như mục Phiên làm việc của /na-chayvideo; vòng ảnh nên chạy trong chat riêng, nối bằng mã video và attempt. Quota helper chỉ xác nhận file chấp thuận tồn tại, agent phải kiểm đó là lời đồng ý thật cho số lượt/phạm vi tương ứng.

Trước tạo/sửa, tự đánh giá ảnh cần asset gì từ brief/t=0: identity, anatomy, assembly và nguồn scale khi liên quan; kế thừa reference_requirements từ /na-chayvideo rồi kiểm lại, brief ảnh trực tiếp tự lập nhu cầu. Khi cần ref, theo [quy trình asset chung](../../../00-Standards/first-frame-asset-references.md): lọc đúng Project/entity/variant/stage/view/role, mở ảnh đã chọn, pin/verify receipt, chỉ gửi ảnh cần và ghi input thực có thứ tự/hash/mục đích. Không mang nền trắng/chữ kích thước từ thư viện vào cảnh; không coi nhãn AI là số đo. Handoff mới schema3 kiểm actual input, schema2 cũ không tự nâng. Thiếu ref hỗ trợ có thể dùng Knowledge; thiếu ref thiết yếu xử lý trước call. Không tạo ảnh chỉ từ việc mở profile/cập nhật catalog; không đọc cả thư viện.

Máy mới hoặc catalog thiếu bộ ref đi kèm: nếu có `08-Assets/reference-library.json`, chạy `python scripts/asset_catalog.py import-bundle 08-Assets/reference-library.json` trước khi báo thiếu, rồi query đúng Project. Không nạp cả manifest vào context hoặc tự ghi đè ID xung đột.


Khi concept có địa điểm thực, đọc setting đã khóa trong INPUTS/frame_state.environment và hồ sơ vùng được dẫn theo [chuẩn địa điểm](../../../00-Standards/location-context.md). Kiểm sinh cảnh đúng vùng/mùa/giai đoạn và nhất quán với prompt video; không tự chọn vùng mới. Chỉ query ref môi trường khi cần, không gọi ảnh thư viện cá là bằng chứng sinh cảnh.

## Ảnh mẫu và bài học — v1.10

Ảnh mẫu thư viện là mặc định từ **lượt đầu**, không chờ ảnh lỗi mới gửi: với mỗi mục `reference_requirements` của ảnh t=0, query `asset_catalog.py` đúng entity/role/variant/view, mở ảnh ứng viên và đánh giá phù hợp (đúng loài/biến thể/cỡ/góc nhìn/vai trò, không mang nền trắng hay tỷ lệ sai vào cảnh). Phù hợp thì gửi theo thứ tự image1..n với vai trò ghi rõ trong prompt ("use image2 only as identity reference for ..."); không phù hợp hoặc thư viện thiếu thì **không bắt buộc** gửi, ghi lý do và dựa vào Knowledge. Môi trường chưa có ảnh mẫu sinh cảnh thì đi bằng hồ sơ vùng/habitat. Có ảnh mẫu thì 9router chạy chế độ edit (2,5–5 phút/lượt); tính lượt như mọi call.

QA ảnh dùng bảng tiêu chí của first-frame.md + Project + bài học task `image-generation`/`image-review` (ví dụ lỗi hình học dụng cụ đã ghi nhận). Lỗi lặp sau 2 lượt sửa cục bộ thì đổi chiến lược (sinh lại, đổi bố cục/cự ly, thêm ảnh mẫu đúng hơn) thay vì sửa lặp cùng cách. Khi chạy trong /na-combo: ảnh đạt/chưa đạt được `combo.py media` upload, kiểm checksum rồi xóa local; hồ sơ văn bản giữ nguyên.
