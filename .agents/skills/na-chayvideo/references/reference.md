# Nhánh reference — dùng chung cho /na-clonevideo

Đây là chế độ tạo bộ từ tham chiếu, không phải revision của video đã tồn tại và không chạy lại toàn bộ skill new. Có analysis/brief có coverage và mapping theo [chuẩn chuyển thể](../../../../00-Standards/reference-video-adaptation.md) trước khi viết; chỉ có link/tóm tắt thì quay bước phân tích, không bịa dữ liệu.

Đọc packet `--mode reference --stage all` qua view, hoặc các stage phù hợp theo lõi chung, cùng Knowledge/model/source bổ sung cho **đối tượng đích**. Map và stage profile reference kế thừa new, task concept vẫn là adaptation/research; thay nguồn chung không làm mất nguồn reference. Điều này không chuyển yêu cầu “phải độc đáo so với mẫu” sang clone. Giữ nguồn, ghi reuse/adaptation; rà lịch sử liên quan/feedback và lần chuyển thể trước, không bắt khác chuyện để qua kiểm trùng. Đọc creativity/Story Development với phạm vi reference như chuẩn chuyển thể quy định.

Khóa trạng thái t=0, vai trò/mapping, lực/đường đi, key/aftermath và âm theo đúng đích. Viết qua output-contract và model profile hiện hành, kiểm chéo với source event IDs; format/caption/lesson/QA/lưu hồ sơ đều dùng [lõi chung](../../../../00-Standards/video-prompt-workflow.md) và cùng scripts/chayvideo_output.py. Dùng `--mode reference` để kiểm/lưu fullset. Khi chỉ sửa caption hoặc một phần của bản chuyển thể đã có, chuyển nhánh caption/revision; không phân tích lại nguyên mẫu khi không cần.

Đủ nội dung mới thì reserve mã đúng Project, lưu analysis/brief paths+hash và adaptation vào research/concept/INPUTS, ghi ledger là chuyển thể có chủ đích. Chỉ phân tích không reserve. Không khẳng định đã render, nghe audio đích hoặc QA media từ việc viết prompt.

Trước viết, khóa translation/rotation/chuyển động chủ thể riêng trong adaptation.md theo chuẩn chuyển thể; partial acceptance không cho phép thay cơ chế. Mapping hiện hành phải khớp revision đã chọn, không lấy nhầm lịch sử.
