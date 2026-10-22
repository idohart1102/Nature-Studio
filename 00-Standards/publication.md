# Cập nhật hệ thống công khai, giữ lịch sử sản xuất ở local

Version: 1.1 | Updated: 2026-10-17 | Quy trình xuất hệ thống, workspace VERSION độc lập

## Phân định

GitHub/gói phân phối: framework, skills, quy chuẩn, templates, kiến thức được phép chia sẻ và bài học cải thiện đã rà để công khai. Không đưa hồ sơ video, brief/concept/prompt/caption/feedback riêng, attempts, media, session-review, performance, ledger hoặc registry local vào cập nhật hệ thống. Project giữ quy chuẩn công khai, không có nghĩa mọi dữ liệu Project đều công khai.

Local vẫn giữ đầy đủ `04-Productions/<slug>/`, `03-Projects/<slug>/idea-ledger.md`, registry và bằng chứng. Repo mới chỉ có mẫu ledger, AI tạo ledger local khi cần; thiếu ledger không chứng minh chưa có lịch sử, vẫn rà file production thật.

Từ v2.1.2, asset tham chiếu được người dùng cho xuất bản có thể đi cùng repo trong `08-Assets/`: chỉ ảnh đã chọn, manifest public/reviewed và review làm sạch. Đây là ngoại lệ có chủ đích cho asset thư viện, không mở quyền đưa media production/ảnh lỗi/database runtime lên GitHub. Mặc định asset mới vẫn private; phạm vi shared/projects độc lập với quyền công bố. Guard kiểm manifest/binding; người xuất vẫn phải rà quyền sử dụng và nội dung. Máy khác nhập bằng `asset_catalog.py import-bundle`; không ghi đè dữ liệu local xung đột.

## Bài học đi cùng cải tiến

Không tự loại hết Memory khỏi cập nhật. /na-dongvideo vẫn ghi bài học Project và shared ở local. Mặc định lesson có `publication.visibility=private`, `reviewed=false`; trạng thái chia sẻ độc lập với candidate/active/retired. Bài học public có thể là candidate, không tự active vì được chia sẻ.

Trước khi gửi hệ thống lên GitHub, rà từng bài học mới/thay đổi. Bài học có ích để tái sử dụng được làm sạch: bỏ mã video/UUID/đường dẫn máy, feedback người dùng nguyên văn, prompt/concept riêng và thông tin tài khoản; giữ hành động, Project hoặc shared scope, điều kiện/ngoại lệ, mức chắc chắn và trạng thái thực. Không suy rộng scope để bỏ dấu dự án. Giữ private bằng chứng gốc; bản diễn giải công khai phải có căn cứ công khai kèm theo, ví dụ ghi chép kiểm phương pháp đã làm sạch tại 06-Evaluation/public-evidence/, không chép raw footage/lịch sử vào đó.

Nếu có thể làm sạch ngay trong bản gốc mà không mất căn cứ, giữ ID và ghi lịch sử chỉnh sửa, đặt visibility public/reviewed true. Nếu cần giữ nguyên bản lesson riêng, tạo bản xuất từ nguồn trong staging/worktree tạm, giữ ID + mapping hash riêng; không tạo hai nguồn runtime mâu thuẫn. Giữ bằng chứng gốc local, bản public dẫn tới ghi chép kiểm được phép chia sẻ. Thiếu cơ sở để công khai thì để private và báo mục chưa đưa lên, không bịa validation hoặc đổi active để lách kiểm. Việc user đồng ý cơ chế này cho phép rà/làm sạch bài học trong lần publish đã được giao, không cấp quyền tự push từ /na-dongvideo.

Chỉ mục public chỉ liệt kê lesson đã xuất, dựng lại counts/links; không công khai ID hay tóm tắt lesson private. Với bản xuất thiếu bằng chứng cần để xác nhận, giữ giới hạn và candidate; không coi link local bị mất là đã giữ truy nguyên. Người cập nhật từ repo merge lesson theo ID/version/scope, không xóa hoặc ghi đè lesson riêng.

## Bắt buộc trước khi publish

1. So Git status/remote và giữ bản khôi phục tracked + untracked; không dùng add -A/push để gộp mọi việc local.
2. Bỏ tracked runtime bằng `git rm --cached` đúng file sau khi backup; không xóa file trên đĩa. Ignore chỉ không đủ cho file đã tracked. Ledger local không commit; dùng template để khởi tạo.
3. Mặc định lesson mới bị ignore theo tên L-*.md; sau khi làm sạch và có metadata public, stage đúng file bằng `git add -f -- <lesson>`, đồng bộ index công khai.
4. Chạy memory validator phù hợp workspace, rồi `python scripts/validate_publication.py` trên **toàn bộ cây index**, không chỉ diff. Phải pass trước mọi Git push hoặc GitHub create_tree/update_ref/API. Nếu dùng export worktree, chạy tại worktree xuất.
5. So diff/schema, xác minh file thực, rà bằng tay nội dung lesson/indices/knowledge để không nhúng history vào nơi khác. Validator chặn đường dẫn/metadata/liên kết, không hiểu hết nội dung riêng tư.
6. Sau publish, fetch và đối chiếu tree/hash; xác nhận production/ledger/registry local nguyên vẹn. CI `Public tree guard` kiểm lại cả push và PR. CI phát hiện sau push không thay kiểm trước publish; chưa cấu hình branch protection hoặc pre-push hook tự chạy trên mọi máy.

Packager mặc định tạo gói hệ thống công khai, bỏ production/ledger/private lesson/browser UI/registry và kiểm tập file xuất. Đây không phải backup cá nhân đầy đủ. Backup local phải có dữ liệu runtime và registry, lưu ngoài repo công khai.

Manifest cài đặt local trong `07-Releases/manifests/` có thành phần tên `installation` (ví dụ `*-installation-*.json`), kể cả bản lồng trong snapshot, không được xuất. Packager và public-tree guard dùng cùng quy tắc đường dẫn; giữ nguyên file gốc để khôi phục, không sửa/xóa release đã đóng. Manifest hệ thống khác vẫn được kiểm theo quy trình hiện hành. Quy tắc này không thay việc rà nội dung riêng tư ở các file có tên khác.

## Dữ liệu đã từng lên GitHub

v1.4 xóa runtime khỏi cây main hiện hành bằng commit thông thường, giữ bản local. Dữ liệu ở commit cũ vẫn có thể truy cập; ignore/CI không xóa lịch sử Git. Muốn xóa toàn bộ lịch sử cần quy trình rewrite/force-push phối hợp với người dùng, không tự thực hiện trong cập nhật hệ thống thường lệ.

## Chỉ mục truy xuất — v1.8

Catalog/query/selection của memory_retrieval.py giữ tại .nature-studio, không đưa lên GitHub/gói phân phối; guard chặn JSON bên trong05-Memory kể cả snapshot. Metadata retrieval của lesson công khai phải được rà/làm sạch như action. Dựng INDEX Markdown của tập xuất từ đúng bài public/reviewed đã chọn, không chép index/catalog local có tóm tắt private. Không có public JSON catalog trong bản đầu; nhận source lesson đủ để rebuild local. Việc đọc/lọc không nâng status hoặc publication.
