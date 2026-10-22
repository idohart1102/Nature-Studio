# Nature Studio — điểm vào cho AI

Từ v2.2.1 mọi skill có tiền tố `na-`: `/na-chayvideo`, `/na-clonevideo`, `/na-dongvideo`, `/na-taoanh`, `/na-danhgia`. Tên cũ không tiền tố (`/chayvideo`, `/taoanh`...) vẫn được hiểu là lệnh mới tương ứng. Tên script trong `scripts/` giữ nguyên.

## /na-clonevideo — chuyển thể từ mẫu

Khi người dùng gọi `/na-clonevideo` hoặc yêu cầu học cách quay/hành động/kịch bản/âm từ video mẫu để thay loài, nhân vật hoặc bối cảnh, đọc [.agents/skills/na-clonevideo/SKILL.md](.agents/skills/na-clonevideo/SKILL.md). Không kích hoạt từ thảo luận hoặc xây/sửa skill. Phân tích hình và âm thực có coverage/timecode; thiếu quyền/công cụ thì báo và xin phần thiếu, không giả đã xem/nghe toàn bộ. Chuyển thể theo vai trò/nhân quả, kiểm lại đặc tính đối tượng đích. Nhánh reference dùng [lõi prompt](00-Standards/video-prompt-workflow.md) và Project hiện hành chung với na-chayvideo; không ép đổi chuyện để đạt độ mới. Không tự render/đăng/push. Analysis/brief/evidence giữ local; registry/quota/history được bảo toàn.

Đọc START-HERE.md và SYSTEM.md trước khi thực hiện công việc trong kho.

Bộ nhớ theo [truy xuất chọn lọc](00-Standards/memory-retrieval.md): query mô tả ngắn Project + shared theo nhiệm vụ/ngữ cảnh, phân trang và xét unknown/legacy rồi mở bản gốc phù hợp; không nạp toàn bộ INDEX/active, không áp candidate như luật.

Phiên bản toàn hệ thống đọc từ VERSION, thay đổi ở CHANGELOG.md. Khi nhận link GitHub để hiểu hệ thống hoặc yêu cầu cập nhật, đọc README.md và thực hiện UPDATE.md; đối chiếu commit/hash và thay đổi local trước khi ghi. Không coi link nguồn là bằng chứng đã biết bản đang dùng của người dùng.

Trước khi phát triển concept mới, đọc [hướng dẫn sáng tạo chung](00-Standards/creativity.md) và hướng dẫn riêng được PROJECT.md chỉ định. Ví dụ không giới hạn không gian câu chuyện; rà lịch sử và kiểm độ mới ở hành vi/nhân quả. Revision giữ ý định đã chốt.

Khi người dùng gửi `/na-chayvideo` hoặc yêu cầu tạo bộ nội dung qua đặc trưng dự án (loài, chủ đề, môi trường, thị trường, format), đọc và thực hiện [.agents/skills/na-chayvideo/SKILL.md](.agents/skills/na-chayvideo/SKILL.md). Đây là quy ước nhận lệnh trong nội dung tin nhắn; không giả định đã đăng ký một slash command của giao diện. Không kích hoạt sản xuất khi người dùng chỉ trích dẫn, giải thích hoặc sửa chính lệnh/skill này.

Skill đọc quy chuẩn và lịch sử đúng dự án trước khi tạo ý tưởng. Mặc định của skill: Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag; mỗi prompt là một đoạn văn. Tự tra metadata các dự án để chọn dự án khớp rõ; chỉ hỏi khi mơ hồ hoặc chưa có dự án phù hợp. Không kích hoạt sản xuất từ câu hỏi kiến thức đơn thuần. Không khởi chạy tạo media chỉ từ lệnh này.

Version: 2.1 | Updated: 2026-10-18 | Reason: profile thực dụng, planned asset catalog và kiểm–lưu/QA có binding; giữ ID, lịch sử và bộ nhớ Project/shared.

Khi người dùng gọi `/na-dongvideo` hoặc yêu cầu tổng kết/đóng phiên video và rút bài học, đọc [.agents/skills/na-dongvideo/SKILL.md](.agents/skills/na-dongvideo/SKILL.md). Không kích hoạt từ trích dẫn, câu hỏi hay sửa skill. Lệnh tổng kết tiếng Việt, luôn xét Project và shared, không tự render/push hay duyệt video. Bộ nhớ theo [memory-policy](00-Standards/memory-policy.md): /na-chayvideo chỉ áp active đúng điều kiện; /na-dongvideo có quyền tự kích hoạt phương pháp khách quan khi đạt đủ gate đã duyệt, không tự thay chính sách sáng tạo.

Video mới: đọc [video-identifiers.md](00-Standards/video-identifiers.md); dùng scripts/video_ids.py cấp mã XX-YYYY: prefix hai chữ A–Z trên local và bốn số từ 0001; UF dành riêng cho legacy. Không gán prefix repo cố định; giữ nguyên video legacy khi sửa/tổng kết. Registry .nature-studio/ là dữ liệu local cần bảo toàn khi nâng cấp.

## Xuất bản hệ thống và bộ nhớ — v1.4

Đọc [publication.md](00-Standards/publication.md) trước khi commit/push hoặc cập nhật GitHub bằng API. Production/attempt/media/ledger/registry giữ local; không đưa vào cây repo hoặc gói hệ thống. Bài học cải thiện ở Project/shared vẫn đi cùng cập nhật sau khi làm sạch và đánh dấu public/reviewed; không tự active. Chạy `python scripts/validate_publication.py` trên cây index trước publish; CI kiểm lại. Không xóa dữ liệu local theo các deletion runtime từ upstream. Commit cũ vẫn có thể chứa dữ liệu đã từng công khai; lần cập nhật này không rewrite lịch sử.

## /na-taoanh — tạo ảnh và QA

Khi người dùng gọi `/na-taoanh`, “tạo ảnh”, “tạo first frame” với ý định tạo/sửa ảnh trong Project, đọc [.agents/skills/na-taoanh/SKILL.md](.agents/skills/na-taoanh/SKILL.md). Không kích hoạt từ câu hỏi, trích dẫn, yêu cầu chỉ viết prompt hoặc sửa skill. Ảnh ngoài Project dùng luồng tạo ảnh thông thường, không ép vào Underwater. First frame QA theo [first-frame.md](00-Standards/first-frame.md) và Project. Tối đa 5 lượt sinh/sửa/call đã gửi, lưu budget local, hết lượt chưa đạt thì dừng và xin thêm số lượt cụ thể. image_gen là tuyến thực thi; ưu tiên Sunburst nếu chọn được, nếu không thì dùng model mặc định và tiếp tục không hỏi lại. Danh tính model không phải tiêu chí QA; không nhận đã dùng Sunburst khi chưa có căn cứ hoặc tự chuyển CLI/API. Không sinh ảnh chỉ vì yêu cầu xây skill.

Profile loài và planned asset theo 00-Standards/knowledge-routing.md khi nhiệm vụ cần. Chỉ query descriptor và mở ref liên quan; không nạp cả catalog. Metadata/hash không tự là visual QA, actual model input hoặc bằng chứng viral.

## /na-danhgia — đánh giá video và hiệu quả sau đăng

Khi người dùng gọi `/na-danhgia` hoặc yêu cầu “đánh giá video”, “QA video”, “chấm video” kèm file hoặc mã video, đọc [.agents/skills/na-danhgia/SKILL.md](.agents/skills/na-danhgia/SKILL.md). Không kích hoạt từ câu hỏi, đánh giá prompt hoặc sửa skill. Chấm từ hình/âm/số đo thật theo chuẩn Project, ghi review và CURRENT-STATE; thiếu khả năng xem/nghe thì ghi not_checked. Không sửa prompt, tạo media, đăng, đổi approval hay ghi Memory master.
