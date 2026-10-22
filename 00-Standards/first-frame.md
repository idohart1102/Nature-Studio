# Tạo ảnh first frame và QA

Version: 1.3 | Updated: 2026-10-18 | Màu tự nhiên, hạn chế ám vàng toàn cảnh

Thực thi theo [.agents/skills/na-taoanh/SKILL.md](../.agents/skills/na-taoanh/SKILL.md). Đây là phương pháp chung; tiêu chí hình ảnh lấy từ Project, không mặc định cá/nước/9:16 cho mọi dự án.

## Các tiêu chí bắt buộc

| Tiêu chí | Kiểm trên ảnh/file thực |
|---|---|
| Khớp brief | Chủ thể, số lượng, nhận dạng, tỷ lệ và lựa chọn đã khóa; không thêm/bớt vật để làm dễ |
| Đúng t=0 | Trạng thái trước biến cố theo concept; không vẽ sẵn kết quả dành cho phần sau |
| Cấu tạo/kết nối | Hình thể/giải phẫu hoặc cấu trúc vật, tiếp xúc/đường nối phù hợp; không nhân đôi/dính/biến dạng |
| Không gian | Vị trí tương đối, tỷ lệ, che khuất, phối cảnh hợp lý; đủ không gian cho diễn biến đã chọn |
| Môi trường/phong cách | Chất liệu, ánh sáng, màu, quang học và camera đúng Project, không chỉ ảnh đẹp |
| Màu tự nhiên/cân bằng trắng | Không ám vàng/cam mạnh toàn cảnh ngoài brief; giữ màu chuẩn đối tượng, phân biệt với ảnh hưởng thật của nguồn sáng/môi trường |
| Khả năng làm đầu vào video | Bố cục hỗ trợ câu chuyện; không khóa chủ thể vào trạng thái không thể tiếp nối. Đây là đánh giá bố cục, không là test chuyển động |
| File đầu ra | Mở được và đã xem ảnh; đo pixel/tỷ lệ/thông tin alpha khi liên quan; không suy từ prompt |
| Ràng buộc Project | Mọi tiêu chí bổ sung Project xác định là bắt buộc đã được kiểm |

Trước sinh ghi danh sách áp dụng, điều kiện/ngoại lệ. Không đặt toàn bộ tiêu chí khó thành not_applicable sau khi thấy ảnh lỗi. Nếu chi tiết nhận dạng bắt buộc bị che/mờ không kiểm được, ghi not_checked và sửa bố cục hoặc báo giới hạn.

Mỗi mục pass/fail/not_checked/not_applicable kèm bằng chứng. `qa_pass` chỉ khi mọi mục bắt buộc pass, không lỗi chặn và không mục bắt buộc chưa kiểm. Lỗi nhỏ chỉ không chặn nếu không ảnh hưởng brief/khả năng dùng và được nêu rõ. Không dùng tổng điểm/giới hạn 5 lượt để hạ chuẩn. Yêu cầu không kiểm được do tool/model phải ghi riêng.

## Màu tự nhiên và cân bằng trắng

Mặc định khi tạo/sửa ảnh: màu chân thực theo đối tượng, nguồn sáng và môi trường; hạn chế lớp ám vàng/cam mạnh phủ cả ảnh. Không tự thêm golden-hour lighting, amber wash hoặc sepia grading chỉ để làm đẹp. Màu vàng/vàng đồng tự nhiên của loài, vật liệu hay chi tiết phải giữ đúng, nhưng không lan thành màu phủ trên nền, nước và các vật khác. Không ép mọi đối tượng trung tính hoặc khử màu thật; không sửa bằng lớp ám xanh/tím đối nghịch.

Khi brief chủ đích yêu cầu ánh sáng/tông ấm phù hợp thực tế, giữ yêu cầu đó và kiểm độ hợp lý; không viện màu vàng riêng của đối tượng để biện minh ám vàng toàn cảnh. Ở môi trường dưới nước, giữ màu nước và suy giảm màu hợp bối cảnh, không bắt nước thành trắng/xám để đạt cân bằng trắng.

Trước call, đưa yêu cầu ngắn phù hợp vào prompt thực thi, ví dụ: “Natural, true-to-life colors under the specified lighting; avoid a strong overall yellow/orange cast, while preserving the subject's authentic yellow or golden coloration.” Không dùng ví dụ để ghi đè brief ánh sáng đã chốt.

QA toàn ảnh và chi tiết: đối chiếu màu đối tượng với Knowledge/ref đúng phạm vi, kiểm nền và vùng trung tính nếu có; không tự thêm vật chuẩn màu vào cảnh. Ghi rõ màu vàng là của đối tượng, nguồn sáng/môi trường hay lớp màu không có căn cứ. Ám vàng mạnh làm sai màu toàn cảnh/nhận dạng ngoài brief là lỗi chặn cần sửa; chưa phân biệt được thì not_checked và ghi giới hạn. Không dùng tỷ lệ pixel vàng hoặc giá trị RGB trung bình làm bằng chứng duy nhất. Sửa màu có mục tiêu, giữ bố cục/anatomy/t=0, kiểm lại phần đã đúng và tính lượt như mọi edit hiện hành. Không sửa QA hay ảnh lịch sử hàng loạt từ quy tắc mới.

## Hạn mức và danh tính

Tối đa 5 yêu cầu sinh/edit/regenerate mỗi cycle; lỗi tool cũng tính nếu đã gửi. Script `scripts/image_budget.py` lưu quota atomically trong production, không gọi API. Bắt buộc reserve trước call, ghi call_id vào attempt, không reset qua phiên chat. Xin thêm số lượt cụ thể sau khi hết; nguồn chấp thuận được lưu local trước grant. Script ghi nhận nguồn nhưng không tự chứng minh đó là lời đồng ý: agent phải kiểm quyền thật.

Mỗi lượt là một attempt Axx riêng, dùng đúng mã video hiện có. Chốt FIRST-FRAME.json trỏ chính xác file/hash/review đạt; user approval độc lập. Không ghi đè output/review/ảnh nguồn. Không viết lại lịch sử input video đã render khi thay ảnh mở đầu; attempt video sau phải dùng đúng ảnh mới đã chọn và ghi provenance.

## Lựa chọn model

Sunburst là ưu tiên, image_gen là tuyến thực thi. Chọn Sunburst nếu công cụ hỗ trợ; nếu không tìm được hoặc không có selector thì dùng model mặc định và tiếp tục không hỏi lại. Danh tính model không thuộc tiêu chí QA và không chặn sinh/duyệt chất lượng ảnh. Ghi actual_model=unknown nếu tool không công bố, không nhận đã dùng Sunburst. Không tự chuyển API/CLI. Xem [model profile](../02-Models/model-profiles/sunburst-imagegen.md).

## Kiểm liên kết ảnh trước tái dùng

Khi tiếp tục dùng ảnh cho video/ảnh revision: `python scripts/chayvideo_output.py check-frame A03 --project <slug> --production <ID>`; A03 là **attempt nguồn nội dung được xác định**, không mặc định mới nhất. Dùng attempts/A03 nếu layout tương ứng; `--handoff <path>` chọn handoff khác, đường dẫn tương đối production. Lệnh chỉ đọc, không sửa ảnh/review/handoff/selection/quota. Caption-only không dùng ảnh thì không chạy.

| Kết quả | Xử lý |
|---|---|
| matched (exit 0) | File/hash/review và opening inputs khớp hồ sơ QA; không chứng minh ảnh đúng hoặc người dùng duyệt |
| needs_review (exit 2) | Opening/first-frame prompt/tiêu chí đổi hoặc chưa qa_pass; đối chiếu ảnh thật, không tự sinh lại |
| unverified (exit 2) | Thiếu frame_state/binding hoặc hồ sơ legacy; đọc nguồn/ảnh để xác định |
| invalid (exit 2), lỗi đọc/resolve (exit 1) | Sai nguồn, thiếu file/hash không khớp; xử lý trước dùng |

Đọc cả errors/needs_review/unverified vì có thể nhiều vấn đề. Nếu ảnh vẫn phù hợp sau đối chiếu thì QA lại bằng quan sát, không cần sinh lại. Giữ QA cũ, lưu review/handoff mới trước cập nhật FIRST-FRAME.json theo quyền đã có; không tự đổi lựa chọn người dùng.

Handoff schema 2 theo template:

- project_id là ID ổn định trong PROJECT.md. attempt_id vẫn là attempt **sinh/sửa ảnh**; source_attempt là attempt **nguồn bộ nội dung** đã resolve, source_attempt_sha256 lấy từ attempt_sha256. Hai attempt có thể khác nhau.
- image_path/review_path tương đối production, dùng `/`; sha256/review_sha256 là hash bytes ảnh/review. Đo pixel/QA thật như trước; helper không giải mã ảnh hoặc chấm tiêu chí.
- frame_inputs/frame_inputs_sha256 lấy từ `resolve <attempt> --project <slug> --production <ID> --frame-inputs` **sau đối chiếu QA ảnh thật**: gồm frame_state và first-frame prompt, không gồm caption/chuyển động sau t=0. Snapshot chỉ in thêm khi có cờ này để giảm đọc trùng; không sửa snapshot để che ảnh lệch brief.
- qa_sources là đường dẫn tương đối workspace → SHA256 của tiêu chí thực sự dùng: first-frame.md, quality-review.md, PROJECT.md và tiêu chí ảnh riêng do Project chỉ định nếu có. Nguồn đổi cần kiểm phần liên quan; hash không chứng minh đánh giá đúng.

Frame_state theo [lõi chung](video-prompt-workflow.md#tiếp-tục-đúng-bộ-đầu-vào). Ảnh trực tiếp từ brief chưa có bộ bốn trường vẫn được tạo/QA theo yêu cầu; không bịa video prompt/caption để dùng resolver. Khi đó binding unverified; trước dùng cho bộ video thật mới đối chiếu và bổ sung qua review mới. Handoff cũ giữ nguyên, kiểm tay khi cần, không backfill hoặc sửa qa_status hàng loạt. Thiếu helper thì kiểm nguồn/ảnh trực tiếp và ghi giới hạn, không giả matched.

## Tỷ lệ đầu vào và export — v1.7

Tách ba kết luận: QA nội dung ảnh, phù hợp làm đầu vào video, và file export chính xác. Với tỷ lệ đích, sai số tương đối `abs((width/height)/(target_width/target_height)-1) <= 0.001` (0.1%) được chấp nhận riêng cho tỷ lệ đầu vào do làm tròn pixel, nếu giao diện nhận được và brief không yêu cầu exact input. Ví dụ 941×1672 lệch khoảng 0.0532% so với 9:16; luôn ghi pixel thật, không gọi exact 9:16. Không dùng lượt sinh chỉ để sửa sai số này khi nội dung và input đã đạt. Ghi từng kết luận trong review/handoff; không đổi qa_pass lịch sử hoặc tự duyệt export. Export có yêu cầu tỷ lệ/kích thước chính xác vẫn phải kiểm riêng. Không crop/stretch âm thầm; xử lý pixel theo quyền người dùng và tuyến công cụ hiện hành, giữ ảnh gốc/hash và kiểm lại bố cục.

Bộ phận ngoài khung ở t=0 không bị ép xuất hiện nếu brief đã chốt; ảnh chỉ QA phần thấy được, phần sẽ lộ ở video có checkpoint reveal/ending riêng theo [media review](media-review-and-finishing.md).

## Asset inputs — v2.1.1

Khi tạo/sửa, đánh giá nhu cầu và dùng [quy trình tham chiếu](first-frame-asset-references.md) khi cần ref. Handoff mới schema3 mở rộng schema2 với asset_inputs (path/hash tương đối workspace), call_id và reference_requirements_sha256. Helper kiểm input/output/call/Project/attempt bindings; không chứng minh tool dispatch hoặc perception. Schema2 cũ giữ kết luận frame binding riêng, trả asset_inputs_status=unverified nếu không có bằng chứng, không tự backfill. Tiêu chí ảnh/QA và budget không đổi.
