# Ghi và sử dụng bộ nhớ

Version: 2.1 | Updated: 2026-10-17 | Truy xuất chọn lọc v1.8; giữ gate activation

## Phân luồng và nguồn duy nhất

- Diễn biến, lỗi, kết quả, phản hồi một lần thử → production/attempt. Chỉ thị lâu dài rõ của người dùng → nguồn quy chuẩn và decisions đúng Project; không giả làm kết luận nghiên cứu, không hỏi lại quyền đã có.
- Dữ kiện chuyên môn có nguồn → Knowledge. Khả năng/giới hạn model đã kiểm → model profile. Memory dẫn tới nguồn, không sao chép hoặc tự thay những tài liệu này bằng lesson.
- Kinh nghiệm có hành động tái sử dụng → `05-Memory/projects/<slug>/` hoặc `05-Memory/shared/`, mỗi nơi có candidates/active/retired và INDEX. Quan sát chưa có ích tái dùng ở lại production.
- Ghi cả phương pháp có ích, thất bại và đánh đổi. Không bắt buộc mỗi phiên có bài học. Nếu quy chuẩn đã nói đủ thì ghi việc bỏ sót trong production; chỉ tạo lesson khi có phương pháp/bằng chứng mới đáng lưu.

## Phạm vi

Project là phạm vi mặc định. Dùng ID ổn định tại PROJECT.md để nhận diện, slug cho đường dẫn. Tách dự án nguồn phát sinh khỏi phạm vi áp dụng.

Shared là phương pháp có ích ngoài dự án nguồn, vẫn có điều kiện nhiệm vụ/model/giao diện/format. Kỹ thuật không tự là chung; shared không mặc định áp dụng mọi dự án. Đặc tính loài, thị hiếu và format riêng không tự thành quy tắc chung. Không có ngưỡng số dự án/lần thử cố định chứng minh mọi loại kết luận.

Trước khi đề xuất shared, ghi vì sao phương pháp còn hữu ích khi đổi chủ đề, phụ thuộc nào còn giữ, căn cứ và giới hạn suy rộng. Thiếu thì giữ Project hoặc shared candidate. Một sự việc có hai lesson chỉ khi khác hành động/phạm vi, cùng dẫn về bằng chứng.

Mỗi lesson có một bản gốc, ID duy nhất toàn kho (`L-<UUID>` hoặc ID cũ đã cấp). Tìm trùng theo ý nghĩa, hành động, điều kiện trước khi cấp ID. Mở rộng/thu hẹp phạm vi giữ ID, ghi lịch sử, chuyển bản gốc và sửa liên kết hiện hành; giữ snapshot cũ. Project tham chiếu shared thay vì giữ bản sao. Nếu chưa đủ căn cứ mở rộng, không làm mất bài học Project đang hợp lệ.

## Trạng thái và quyền đã được duyệt

- candidate: quan sát/hypothesis/đề xuất đang chờ kiểm; chỉ gợi ý phép thử, không dùng như quy tắc xác nhận.
- active: đủ căn cứ trong phạm vi đã ghi; chỉ áp khi khớp điều kiện.
- retired: sai/bị thay thế/hết áp dụng; giữ lịch sử và liên kết thay thế.

`/na-dongvideo` được tự ghi tổng kết, tạo/cập nhật candidate ở cả hai cấp, bổ sung bằng chứng và gộp mục trùng có truy vết. `/na-chayvideo` được ghi quan sát/candidate nhưng không tự nâng trạng thái. Đóng phiên, lặp lời AI, im lặng hoặc một lượt render đẹp không chứng minh đã duyệt/đã hiệu quả.

Riêng `/na-dongvideo` được tự kích hoạt **bài học phương pháp có phép kiểm khách quan** khi đồng thời đạt:

1. Có bằng chứng gốc đã truy cập, hành động cụ thể, phạm vi hẹp, ngoại lệ; ghi mức chắc chắn và điều không được suy ra.
2. Có ca kiểm phù hợp với kết luận, kết quả thực tế pass và hồ sơ ở `06-Evaluation/results/`. Không tự tạo expected rồi gọi là actual. Kiểm prompt không chứng minh render; kiểm schema/liên kết không chứng minh quyết định AI đúng.
3. Đã kiểm ca liên quan và ngoại lệ/hồi quy có thể bị ảnh hưởng, lưu kết quả/đánh đổi. Không còn mâu thuẫn chưa xử lý.
4. Không thay sở thích, định hướng, brief, format, Standards hoặc chính sách. Không dùng quyền này cho kết luận sáng tạo, phản ứng khán giả, hiệu quả model/retention hay nhân quả chưa tách biến.
5. Ghi activation automatic, ngày, lý do, liên kết chính sách này và hồ sơ kiểm. Shared có thêm căn cứ dùng ngoài Project nguồn.

Thiếu bất kỳ điều kiện nào thì candidate; báo phần cần kiểm, không dừng cả phiên để hỏi. Kết luận rộng/đánh giá sáng tạo trình duyệt theo đợt. Người dùng có thể cho phép kích hoạt cụ thể nhưng vẫn ghi giới hạn bằng chứng; sự đồng ý không chứng minh dữ kiện tự nhiên/hiệu quả nhân quả. Yêu cầu đổi quy chuẩn được xử lý như quyết định riêng.

Khi bằng chứng mới mâu thuẫn, ghi phạm vi/bằng chứng, ngừng dùng phần kết luận bị ảnh hưởng; đưa active về candidate nếu không còn đủ cơ sở. Không xóa quan sát cũ. Đổi trạng thái/hợp nhất giữ ngày, lý do, ID thay thế. Lời AI lặp lại không phải bằng chứng độc lập, view không thay QA.

## Truy xuất và kiểm vòng sau

Theo [truy xuất chọn lọc](memory-retrieval.md), query metadata Project hiện hành + shared theo nhiệm vụ và hint chủ đề/đối tượng/tương tác; không nạp toàn bộ INDEX hoặc toàn văn mọi active. Đọc descriptor theo trang rồi mở bản gốc có thể áp dụng. Conditions mâu thuẫn rõ mới loại; thông tin chưa biết/legacy cần xét, nhãn chỉ xếp liên quan. Không cắt top-k để chứng nhận coverage. Danh sách conditions rỗng không thêm hạn chế ở chiều đó, không chứng minh áp dụng mọi nơi; vẫn đọc điều kiện/ngoại lệ. Không tự áp bộ nhớ Project khác; chỉ tra khi được giao đánh giá chuyển giao.

Quy chuẩn hiện hành ưu tiên hơn memory; gặp mâu thuẫn nêu vấn đề, không âm thầm ghi đè. INPUTS ghi ID + version + đường dẫn + cách dùng; candidate đã thử ghi riêng. Lần `/na-dongvideo` sau kiểm lesson nào thật sự được dùng, kết quả/giới hạn; đã dùng không chứng minh có ích hoặc quan hệ nhân quả.

INDEX là bản đồ. Nếu thiếu/cũ, tìm file thực và sửa chỉ mục. Dùng [mẫu lesson](templates/lesson.md), metadata JSON trong frontmatter cũng là YAML hợp lệ, đọc bằng stdlib Python. Chạy `python scripts/validate_memory.py`: chỉ kiểm cấu trúc/liên kết, không xác nhận nội dung hay hiệu quả.

Không ghi chuỗi suy luận nội bộ; chỉ lưu kết luận, hành động, căn cứ kiểm tra được. Không tự publish/push, tiêu tiền, render hoặc sửa release đã đóng từ lệnh tổng kết.

## Chia sẻ lesson khi cập nhật hệ thống — v1.4

Theo [publication.md](publication.md), /na-dongvideo tạo lesson mặc định private, reviewed=false. Khi publish đã được giao, rà bài học cải thiện ở cả Project/shared để đưa bản làm sạch lên hệ thống; không tự upload production làm bằng chứng. Public/reviewed độc lập candidate/active/retired, giữ phạm vi và sự thật. Lesson chưa thể chia sẻ ở lại local, nêu rõ thay vì loại hết bộ nhớ hoặc tự active. Chỉ mục public chỉ liệt kê mục đã xuất.
