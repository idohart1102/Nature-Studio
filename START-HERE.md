# Nature Studio — bắt đầu tại đây

Kho sản xuất nội dung thiên nhiên, lưu trên máy; khởi tạo 15/10/2026 (Asia/Saigon).

Phiên bản toàn hệ thống: **Nature Studio v2.2.1**, nguồn máy đọc là [VERSION](VERSION); xem [CHANGELOG.md](CHANGELOG.md). Khi người dùng đưa link GitHub và yêu cầu so sánh/cập nhật, đọc [UPDATE.md](UPDATE.md) trước khi ghi: cần cả bản đích và trạng thái local, giữ dữ liệu riêng và không đoán bản mới từ tên file.

## Lệnh tạo bộ nội dung

Để chuyển thể video mẫu, gửi `/clonevideo` kèm file/link và thay đổi mong muốn. [Skill clonevideo](.agents/skills/clonevideo/SKILL.md) phân tích cách quay, vai trò/hành động từng chủ thể, câu chuyện và âm thanh; đổi loài/nhân vật/bối cảnh qua mapping đúng tự nhiên rồi xuất cùng bốn mục. Dùng [lõi chung](00-Standards/video-prompt-workflow.md) và [chuẩn chuyển thể](00-Standards/reference-video-adaptation.md), không ép sáng tạo một chuyện khác mẫu. Cần công cụ truy cập hình/âm thật; chỉ xem frame/transcript không là phân tích toàn clip. Không tự tạo media hoặc công bố nội dung. Việc xây skill không chạy phân tích/render thật.

Gửi `/chayvideo` kèm tên dự án, loài hoặc brief nếu có. AI đọc [skill chayvideo](.agents/skills/chayvideo/SKILL.md), tra nguồn hiện hành và lịch sử thực trước khi chọn ý tưởng; trả bốn mục: Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh; CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag. Có thể chỉ nêu đặc trưng dự án trong yêu cầu tạo nội dung, skill tự tra dự án phù hợp; chỉ hỏi khi mơ hồ hoặc không có dự án khớp. Mỗi prompt là một đoạn văn. Khi thiếu lựa chọn bắt buộc, skill hỏi đúng phần còn thiếu. Lệnh chỉ tạo văn bản và hồ sơ local, không tự render/đăng.

Đây là quy ước nhận lệnh trong chat qua [AGENTS.md](AGENTS.md), không phải cam kết giao diện có menu slash riêng. Updated: 2026-10-16.

## Cách dùng với bất kỳ AI nào

Giao file này cùng yêu cầu và quyền đọc thư mục repo; đường dẫn workspace không cố định, thư mục có thể mang tên khác, ví dụ `C:\Nature Studio`. Nếu AI không truy cập được file local, gửi repo hiện hành hoặc gói ZIP tạo bằng `scripts/package_workspace.py`, không dùng hướng dẫn độc lập v1.9 trong 07-Releases/standalone-guides/ vì đó chỉ là lưu trữ lịch sử. Không giả định AI nhớ lịch sử chat.

1. Đọc [SYSTEM.md](SYSTEM.md); xác định nhiệm vụ: nghiên cứu, ý tưởng, viết prompt, tạo media, review hay cập nhật hệ thống.
2. Tra [danh mục dự án](03-Projects/INDEX.md), xác định dự án; đọc PROJECT.md của đúng dự án. Dự án đã cấu hình: [Underwater](03-Projects/underwater/PROJECT.md). Thiếu dự án và không suy được từ yêu cầu thì hỏi một câu ngắn.
3. Đọc quy chuẩn dự án liên quan nhiệm vụ rồi lấy hướng dẫn từ [Standards](00-Standards/INDEX.md). /chayvideo theo nhánh new/revision/caption của skill: tạo bộ đầy đủ đọc format/giọng/output-contract; chỉ sửa caption không buộc nạp lại format/model/kiến thức không liên quan. Khi tạo ý tưởng mới, bắt buộc đọc [hướng dẫn sáng tạo chung](00-Standards/creativity.md) và tài liệu sáng tạo mà PROJECT.md dẫn tới; Underwater có [Sáng tạo mở](03-Projects/underwater/creative-direction.md). Khi sửa clip, giữ trọng tâm đã chốt.
4. Tra [Knowledge](01-Knowledge/INDEX.md) theo loài, môi trường, tương tác/dụng cụ; tra [Models](02-Models/INDEX.md) khi cần thông tin model/giao diện.
5. Tra [Memory](00-Standards/memory-retrieval.md): query descriptor Project + shared theo nhiệm vụ/hint, phân trang và xét unknown/legacy, mở bài gốc phù hợp rồi chỉ áp active đúng điều kiện; không nạp toàn bộ INDEX/active. Ghi ID/version/cách dùng vào INPUTS; không tự áp lesson Project khác. Tạo mới rà idea-ledger và hồ sơ thực để tránh lặp; chỉ mục/fingerprint có hash hỗ trợ tra cứu, hồ sơ chưa được bao phủ hoặc hết hạn vẫn phải đọc gốc. Revision/caption giữ chuyện đã chốt, đọc lịch sử liên quan.
6. Khi sản xuất, tạo hồ sơ bằng mẫu trong 00-Standards/templates/. Ghi phiên bản tài liệu/đầu vào đã dùng; mỗi lần thử là một thư mục mới. Không tạo/render nếu yêu cầu chỉ viết prompt.
7. Review sản phẩm thực tế khi có; ghi phản hồi, chỉ đưa kết luận đủ cơ sở vào bộ nhớ theo memory-policy.md. Khi chỉ có prompt thì chỉ kiểm được prompt.

Không đọc toàn bộ kho mỗi lượt. Nếu không tìm thấy thông tin, tìm theo tiêu đề/thẻ/nội dung; thiếu chỉ mục không có nghĩa tài liệu không tồn tại. Không bắt người dùng tự điền mọi trường mẫu mới bắt đầu.

## Trạng thái khởi tạo

- Underwater có quy chuẩn kế thừa v1.9, đã phân tách theo phạm vi.
- Nguồn v1.9 được giữ nguyên ở bản phát hành nhập ban đầu; không kế thừa v1.8.
- Chưa nhập video/render cũ, chưa đo lại audio, chưa xác nhận hiệu quả retention hay viral.
- Chưa có model test mới, bài học active hoặc ca đánh giá đã chạy đạt.

## Cập nhật cấu trúc 2026-10-16

Workspace tổ chức theo Project. Dự án hiện hành: [Underwater](03-Projects/underwater/PROJECT.md), tên cũ Under Fish US / Under Fishing US. Quy chuẩn đã chuyển sang 03-Projects/underwater; hồ sơ sản xuất sang 04-Productions/underwater; mẫu dự án là 00-Standards/templates/project.md. Không có dự án mới được tạo từ lần đổi tên này.

Tên repo cố định là Nature-Studio; nâng VERSION không đổi URL. [REPOSITORY.json](REPOSITORY.json) ghi danh tính nguồn; UPDATE.md hướng dẫn đối chiếu bản đang dùng và bản mới.

## Tổng kết và học sau phiên — v1.1

Gửi `/dongvideo UF-0001` hoặc yêu cầu đóng phiên video cụ thể. Đọc [skill dongvideo](.agents/skills/dongvideo/SKILL.md): tổng kết dữ liệu thực, luôn xét bài học Project và shared; tự lưu candidate, chỉ tự kích hoạt phương pháp đã kiểm khách quan theo [policy](00-Standards/memory-policy.md). Kết luận rộng còn chờ kiểm/duyệt được gom trong báo cáo tiếng Việt. Đóng phiên không tự duyệt video hoặc đẩy GitHub. Gọi lại với cùng dữ liệu không tạo mục trùng.

Nâng từ v1.0: đọc phần migration trong [UPDATE.md](UPDATE.md); bảo toàn production/lesson/chỉnh sửa riêng trước khi chuyển cấu trúc. Chạy `python scripts/validate_memory.py` sau cập nhật.

## Mã video — Nature Studio v1.2

Video mới dùng **XX-YYYY**, hai chữ A–Z riêng từng Project local, bốn chữ số từ **0001**. [Quy tắc và công cụ](00-Standards/video-identifiers.md): init tạo prefix, reserve cấp mã an toàn và UUID. Không cấp mã từ câu hỏi hoặc revision. Registry `.nature-studio/` không lên Git, phải được giữ khi backup/di chuyển/cập nhật; không nằm trong gói mẫu. UF-0001, mã ba chữ/năm số và các attempt lịch sử giữ nguyên. Prefix UF dành riêng cho legacy; namespace mới được chuyển khi init/reserve thật, giữ UUID Project. Xem UPDATE.md khi nâng từ v1.1.

## Story Development — 2026-10-16

Khi tạo concept mới, đọc [phương pháp phát triển câu chuyện](00-Standards/story-development.md) sau creativity và kết hợp phần Project chỉ định. Tài liệu nghiên cứu ngoại bộ và giới hạn được liên kết trong đó. Không dùng phương pháp để thay số mục đầu ra hoặc tự triển khai media.

## Xuất bản hệ thống và bộ nhớ — v1.4

Đọc [publication.md](00-Standards/publication.md) trước khi commit/push hoặc cập nhật GitHub bằng API. Production/attempt/media/ledger/registry giữ local; không đưa vào cây repo hoặc gói hệ thống. Bài học cải thiện ở Project/shared vẫn đi cùng cập nhật sau khi làm sạch và đánh dấu public/reviewed; không tự active. Chạy `python scripts/validate_publication.py` trên cây index trước publish; CI kiểm lại. Không xóa dữ liệu local theo các deletion runtime từ upstream. Commit cũ vẫn có thể chứa dữ liệu đã từng công khai; lần cập nhật này không rewrite lịch sử.

## /taoanh — ảnh first frame có QA

Gửi `/taoanh <mã video>` hoặc “tạo ảnh”/“tạo first frame” trong ngữ cảnh Project rõ. [Skill](.agents/skills/taoanh/SKILL.md) đọc concept và quy chuẩn, tạo/sửa qua image_gen, xem ảnh thực và QA sau mỗi lượt. Dừng ngay khi đạt hoặc tối đa 5 call; chưa đạt thì báo và xin thêm lượt, không reset qua chat. Ảnh đạt khác với bạn duyệt và khác với video đạt. Ưu tiên Sunburst nếu chọn được; nếu không, dùng model mặc định image_gen và tiếp tục không hỏi lại. QA kiểm chất lượng ảnh, không bắt buộc xác minh model; không giả đã chọn Sunburst. Lệnh chỉ xây/sửa skill không chạy tạo ảnh.

## /danhgia — chấm video render và số liệu

Gửi `/danhgia <mã video>` kèm file render, hoặc kèm số liệu sau đăng. [Skill](.agents/skills/danhgia/SKILL.md) kiểm kỹ thuật bằng `media_review.py`, xem frame 3 giây đầu và quanh key, nghe âm khi có khả năng, rồi ghi review, CURRENT-STATE và performance. Lỗi được chuyển cho /chayvideo hoặc /taoanh sửa; skill không tự sửa hay render.
