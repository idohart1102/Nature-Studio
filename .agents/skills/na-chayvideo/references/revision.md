# Sửa/tiếp tục clip

Version: 1.3 | Updated: 2026-10-22 | Ghi feedback mỗi lượt, base từ resolve --out

Đọc packet revision và production cụ thể: brief/concept, SUMMARY, attempt được chọn, INPUTS/feedback và media/handoff khi được cung cấp. Trước khi trả lời mỗi lượt sửa, thêm mục feedback.md của production theo mục Phiên làm việc trong SKILL; chat sau chỉ biết những gì đã ghi vào file. Không mặc định attempt số lớn nhất là được chọn. Thiếu ngữ cảnh clip cần xác định thì hỏi đúng phần thiếu; chưa rõ không viết chuyện thay thế.

Theo [lõi chung](../../../../00-Standards/video-prompt-workflow.md), dùng stage write/review/save và effects thực, không đi lại concept-new. Render/audio review phải có task tương ứng, không coi mode revision là đã truy xuất mọi lesson review. View giữ nguyên văn; coverage giữ đủ tập nguồn nền và phần được effects bổ sung. Ảnh hưởng chưa rõ hoặc config thiếu quay về nguồn đầy đủ; không tự cắt Knowledge chỉ từ chữ “sửa nhỏ”.

Dùng `resolve --out` rồi `save --from-resolve` (base_attempt/base_sha256) theo [lõi chung](../../../../00-Standards/video-prompt-workflow.md#tiếp-tục-đúng-bộ-đầu-vào) để giữ nguồn từng trường. Đối chiếu frame_state khi sửa chuyện/prompt; thiếu xác nhận t=0 thì unverified. Nếu tiếp tục dùng ảnh đã QA, kiểm handoff theo first-frame.md; sửa văn bản không tự ghi lại handoff hoặc sinh ảnh.

Giữ loài/ý định/key/kết cục đã chốt ngoài phần người dùng yêu cầu đổi. Không chạy brainstorm hoặc rà toàn bộ lịch sử để buộc mới; nếu yêu cầu thực sự là concept mới thì chuyển new. Mở thêm Knowledge/nguồn ngoài chỉ phần thay đổi và liên đới; sửa rig có thể ảnh hưởng mồi/móc/dây/lực/ảnh đầu/âm/caption, phải kiểm cả chuỗi. Sửa prompt ảnh không có nghĩa được tạo ảnh.

Yêu cầu thay đổi rõ thì sửa đúng phần được giao, không bắt chẩn đoán lỗi hoặc có render mới được sửa. Khi xử lý lỗi, dựa trên vật thực sự đã kiểm để xét nơi cần sửa: brief/concept, bố cục/trạng thái đầu, bộ đầu vào/media được chọn, cách diễn đạt prompt hoặc kết quả/model/settings. Ghi gọn quan sát → nguyên nhân nghi ngờ → phần sửa và phần cần kiểm lại trong INPUTS/review/revision hiện có; chưa rõ thì giữ là giả thuyết, không suy một lần render lỗi thành model không có khả năng. Nếu chỉ có phản hồi người dùng thì ghi nguồn phản hồi, không nhận AI đã quan sát media. Với chuyện/prompt đã đổi, đối chiếu phần liên quan theo bước G của Story Development; caption-only giữ nhánh nhẹ, không mở lại chuyện/QA ảnh khi không liên quan.

Giữ quy chuẩn hiện hành trừ ngoại lệ người dùng chốt cho clip; phát hiện mâu thuẫn thực tế thì nêu/correct gần ý định. Kiểm chéo các mục bị ảnh hưởng. Trả đúng phần được giao, lưu attempt mới với before/after hoặc tham chiếu phần giữ nguyên; không ghi đè lịch sử/quota ảnh. Cập nhật SUMMARY/concept/ledger khi cơ chế hoặc trạng thái thật thay đổi; fingerprint cũ hết hạn khi có thêm nguồn, không tự giữ kết luận cũ.

Khi đã có render, đọc [media review](../../../../00-Standards/media-review-and-finishing.md): đo thực và kiểm provenance; chỉ lỗi mức mix thì xét finishing có quyền, không mặc định render lại hình. Lấy CURRENT-STATE/SUMMARY và evidence actual inputs, không nhầm text mới nhất với render được chọn hoặc tạm duyệt với QA đạt.

Giữ ngắn danh sách vật thể/điểm nối/trạng thái và dấu hiệu cần thấy trong INPUTS/revision; tách quan sát, nguyên nhân nghi ngờ, phần giữ/sửa. Đổi cơ chế thì rà lại câu cũ thay vì nối thêm cấm. Kiểm lấy đúng mồi, attachment, lực, che khuất và ending riêng theo brief, không buộc mọi loài giãy mạnh. Asset planned theo lõi chung; đổi ảnh/metadata thì kiểm receipt, không tự kế thừa QA. Ngoại lệ beat cần binding thật, không suy từ số động tác.

Caption theo contract/giọng Project hiện hành: Underwater mặc định ba bản, thứ tự caption EN + hashtag → lược dịch caption VI → hook EN 1–9 từ → lược dịch hook VI. Tiếng Anh được viết trước, tự đọc kiểm giọng người câu cá Mỹ rồi dịch ý; không coi helper là kiểm native. Chỉ sửa phần được giao, bundle cũ phải được rà lại khi chuyện đổi.
