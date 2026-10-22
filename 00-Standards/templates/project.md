# Dự án
ID: <project-id>
Slug: <project-slug>
Aliases / đặc trưng nhận diện:
Status: draft
Version: 0.5
Updated: <date>
Prefix sản xuất: local-generated, chưa cấp trong repo; init bằng scripts/video_ids.py sau khi tạo Project local.
Legacy prefixes nếu có:
Mục tiêu / chủ đề / khán giả / thị trường:
Nguồn quy chuẩn hiện hành: format.md; audience-and-caption.md; output-contract.md
Context sources: context-map.json là tập nguồn đầy đủ theo mode; có thể trỏ routing tới cấu hình stage/effect riêng theo 00-Standards/context-routing.md. Không có config thì đọc full branch; nguồn mới chưa phân stage vẫn phải đọc. Không sao chép nguồn/điều kiện Underwater cho Project khác.
Yêu cầu lấy đầu vào:
Giới hạn sáng tạo / tính chân thực:
Nguồn nghiên cứu / thẻ truy xuất:
Ghi chú: không mặc định kế thừa quy tắc dự án khác.

Memory namespace: 05-Memory/projects/<project-slug>/INDEX.md (stable ID ở trên).
Memory retrieval: theo 00-Standards/memory-retrieval.md; query descriptor Project + shared theo nhiệm vụ/hint rồi mở bài gốc liên quan, không đưa toàn bộ INDEX/active vào context-map common. Unknown/legacy cần xét; candidate không là luật.
Khi khởi tạo Project, tạo INDEX và candidates/active/retired trong namespace, dẫn cả shared/INDEX.md từ PROJECT.md và đăng ký namespace ở 05-Memory/INDEX.md. Không kế thừa bài học Project khác mặc định. Model/format/loài là điều kiện nếu liên quan, không mặc định dự án nào cũng có cá.

First-frame QA guide: 00-Standards/first-frame.md + tài liệu riêng Project nếu có; không kế thừa tiêu chí cá/nước/9:16 cho mọi Project. /na-taoanh chỉ chạy khi có yêu cầu tạo ảnh thực.

Profile loài chọn điểm thật đáng xem và cỡ có căn cứ, không là danh sách tình huống đóng. Khi cần ref, dùng catalog chung theo entity/stage/role ở [knowledge-routing](../knowledge-routing.md); metadata/planned ref không chứng minh ảnh hoặc render đã đạt. Không tải cả thư viện hoặc gán luật Underwater cho Project khác.
