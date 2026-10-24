---
name: na-taoanh
description: Tạo hoặc sửa ảnh first frame Nature Studio khi gọi /na-taoanh, “tạo ảnh”, “tạo first frame” với ý định tạo media trong Project; QA ảnh thật sau mỗi lượt, tối đa 5 lượt rồi xin thêm. Không kích hoạt khi chỉ hỏi, trích dẫn, viết prompt hoặc sửa skill; ảnh ngoài dự án dùng luồng tạo ảnh thông thường.
---

# /na-taoanh

Version: 1.8 | Updated: 2026-10-22 | Lệnh handoff tự tính hash; feedback mỗi lượt sửa

Quy ước trong chat, không cam kết giao diện đăng ký slash command. Dùng workspace chứa skill làm gốc (đi lên ba cấp từ thư mục skill). Tổng kết/QA tiếng Việt; prompt thực thi tiếng Anh một đoạn. Skill này tạo ảnh, không tạo video. Chỉ xây/sửa skill không phải yêu cầu chạy sinh ảnh.

## Xác định đúng đầu vào

Đọc START-HERE.md, SYSTEM.md, `00-Standards/first-frame.md`, production/quality-review/memory-policy và `02-Models/model-profiles/sunburst-imagegen.md`. Khi thực thi, dùng skill imagegen sẵn có theo catalog để tuân thủ cơ chế tool, ảnh tham chiếu và lưu file; không cần skill đó khi chỉ chỉnh tài liệu.

Ưu tiên Project/mã video/attempt được nêu. Tra metadata Project và production thực, không chọn theo ngày file hoặc mã chữ đơn lẻ. “Tạo ảnh” trong ngữ cảnh rõ một video là lời gọi; câu hỏi, trích dẫn, yêu cầu viết prompt không kích hoạt. Yêu cầu ảnh ngoài Project không bị ép vào Underwater; chuyển luồng imagegen thông thường hoặc hỏi mục đích khi mơ hồ. Không mặc định mọi ảnh trong workspace là first frame.

Đọc brief/concept/FIRST FRAME PROMPT, INPUTS, feedback, ảnh và review hiện hành cùng các file Project dẫn tới. Tìm lesson active của Project và shared đúng điều kiện, ghi ID/version/cách dùng. Với Underwater đọc `03-Projects/underwater/first-frame-qa.md`. Hồ sơ loài trong ảnh lấy bằng `python scripts/species_profiles.py resolve "<tên>"` (chỉ mở đúng hồ sơ đó); mục 7 Checklist hình ảnh là tiêu chí QA bắt buộc, `entity_id` là `id` của hồ sơ khi tra ref. Ưu tiên ref `origin: photo` cho identity/anatomy; ảnh AI chỉ hỗ trợ production. Giữ lựa chọn người dùng và câu chuyện đã chốt; không sáng tác production mới hoặc đổi loài/kết cục để sửa ảnh dễ hơn. Thiếu concept quan trọng thì hoàn thiện trong phạm vi đã giao hoặc hỏi trước khi sinh. Video mới chỉ cấp ID bằng video_ids.py khi nhiệm vụ thật đòi production mới và đủ brief; revision không cấp video ID mới.

Ghi bản khóa đầu vào: t=0, chủ thể/số lượng/nhận dạng/tỷ lệ, môi trường, camera, vị trí/quan hệ/đường chuyển động cần cho video và tiêu chí bắt buộc. Tách ảnh đích sửa, reference và supporting input; mở từng ảnh local cần dùng bằng view_image trước khi sửa. Mâu thuẫn hoặc dữ kiện chưa có cơ sở phải xử lý trước khi tiêu lượt.

Mặc định prompt và QA theo [màu tự nhiên/cân bằng trắng](../../../00-Standards/first-frame.md#màu-tự-nhiên-và-cân-bằng-trắng): hạn chế ám vàng/cam mạnh toàn ảnh, giữ màu chuẩn của đối tượng; đối tượng vàng không là lý do phủ vàng cả cảnh. Không tự thêm golden-hour/amber/sepia grade, không khử vàng bằng ám xanh hoặc làm mất màu thật. Chỉ dùng tông ấm có chủ đích khi brief yêu cầu và nguồn sáng/bối cảnh phù hợp; QA màu trên output thật, sửa có mục tiêu trong budget hiện hành.

## Công cụ và ưu tiên Sunburst

Tra bài học theo [lõi truy xuất](../../../00-Standards/memory-retrieval.md) với task `image-generation` và `image-review`, hint từ brief; đọc descriptor rồi mở active phù hợp, không nạp toàn bộ INDEX. Khi debug/thử mới dùng thêm `--candidates` riêng; không coi candidate là luật. Giữ nguồn/quota/handoff như phần dưới.

Khi dùng bộ nội dung đã có, resolve đúng attempt và đối chiếu frame_state theo lõi chung. Tái dùng ảnh đã QA phải theo [kiểm liên kết ảnh](../../../00-Standards/first-frame.md#kiểm-liên-kết-ảnh-trước-tái-dùng). matched chỉ là liên kết hồ sơ khớp; vẫn xem/đo ảnh như skill yêu cầu. Khi ghi handoff mới dùng schema 3 theo phần asset bên dưới, phân biệt attempt ảnh với source_attempt nội dung; giữ review/handoff trước, không tự nâng hồ sơ cũ hoặc sinh lại chỉ vì cần kiểm lại.

Chỉ dùng built-in `image_gen` theo yêu cầu người dùng, không tự dùng CLI/API. Model ưu tiên: **GPT Image 2.5 Sunburst**. Nếu schema thực có selector và hỗ trợ Sunburst thì chọn Sunburst; nếu không tìm được hoặc không có selector, dùng model mặc định của image_gen và tiếp tục, không hỏi lại. Không tự chỉ định Flare để thay thế. Tên Sunburst trong prompt không chọn backend; không bịa model/seed/quality ẩn.

Người dùng đã cho phép dùng model mặc định nếu không tìm được Sunburst. Danh tính model không phải tiêu chí QA hoặc cổng chặn sinh ảnh. Không công bố model không làm ảnh fail và không cần xin quyền riêng cho backend unknown.

Ghi requested_model=Sunburst, selection_mode=sunburst nếu chọn được hoặc tool_default nếu dùng mặc định; actual_model lấy từ công bố thực, nếu không có thì unknown và model_verified=false. Không nhận đã dùng Sunburst khi chưa có căn cứ. Không cần khóa API cho built-in. Tool lỗi/không có thì báo trạng thái; không tự chuyển đường khác, không retry vô hạn.

## Vòng sinh/sửa và QA

1. Khởi tạo/đọc cycle ở production bằng `python scripts/image_budget.py init --production 04-Productions/<slug>/<video-id>`. Cùng vòng sửa đang dở tiếp tục bộ đếm cũ; không reset bằng đổi chat, mã attempt hoặc gọi lại lệnh. Chỉ `new-cycle` khi người dùng giao ảnh/brief mới rõ ràng và có hồ sơ yêu cầu.
2. Nếu đang ở cycle đã đạt, đầu vào không đổi và không được yêu cầu revision, trả lại ảnh đã đạt, không tiêu thêm lượt. Nếu muốn sửa sau khi đạt, xác định quyền/phạm vi vòng mới, không tự mở vòng để vượt hạn mức.
3. Trước **mỗi** lần gửi image_gen (tạo mới, edit hoặc tạo lại), tạo attempt mới theo production.md, lưu prompt/ảnh nguồn/INPUTS/settings và gọi `image_budget.py reserve --production ...`. Lưu call_id/cycle_id vào attempt. Được phép sinh chỉ khi reserve thành công. Tool call đã gửi tính một lượt kể cả lỗi/cancel/không có ảnh; pending không rõ có chạy phải giữ lượt, tra kết quả trước khi gọi lại. Một call là một ảnh đích; không yêu cầu nhiều variants để lách quota. Tool tự trả nhiều ảnh thì kiểm từng ảnh và ghi đúng, không gọi thêm ngoài budget.
4. Dùng image_gen thực, một lần gọi theo prompt có mục tiêu. Sửa cục bộ trên ảnh tốt nhất có căn cứ; lỗi nền tảng thì tạo lại từ prompt đã sửa. Không mặc định bản mới nhất là tốt nhất. Dùng đúng cơ chế referenced_image_paths/num_last_images_to_include theo schema hiện hành, không đưa cả hai.
5. Copy output thực vào attempt local, giữ output gốc và hash; không ghi đè bản cũ. Mở ảnh output bằng view_image, kiểm toàn ảnh và chi tiết quan trọng. Không chấm ảnh từ prompt, thumbnail nhỏ hoặc tên file. Đo kích thước/tỷ lệ file, không coi “đã yêu cầu 9:16” là đã đúng. Công cụ đo/crop phục vụ quan sát; sửa pixel phải dùng image_gen trừ khi người dùng chỉ định khác.
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
