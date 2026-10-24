# Kiểm chất lượng — v1.1

## Phân tầng kết luận

- Prompt-only: kiểm hợp đồng, tính nhất quán, cơ sở và khả năng thực hiện; chưa xác nhận hình/âm đạt.
- Image-reviewed: kiểm ảnh thật; chưa suy ra video giữ được cấu tạo/chuyển động.
- Video-reviewed: kiểm file thật, frame quanh key, chuyển động, kết nối, thời lượng và audio nếu thực sự nghe được.
- Published-measured: chỉ ghi hiệu quả từ dữ liệu đăng thực tế, có thời điểm đo và nguồn.

## Cách ghi review

Mỗi phát hiện: ID → timecode/frame → điều quan sát được → tiêu chí bị ảnh hưởng → mức độ → nguyên nhân nghi ngờ → sửa đề xuất → kết quả kiểm lại. Dùng pass / fail / not checked / not applicable cho từng tiêu chí. Kết luận chưa được kiểm khác với không đạt.

Ưu tiên: đúng loài/môi trường → nhất quán vật thể và nhân quả → câu chuyện/nhịp → hình/âm → caption theo dự án. Tiêu chí cụ thể ở format/output-contract, không áp cứng cùng trọng số cho mọi chủ đề.

## Hai bảng đánh giá riêng

1. Sản xuất: đúng dữ kiện, giải phẫu, vật lý, bố cục, timeline, audio, hợp đồng, số lượt sửa và lỗi lặp.
2. Hiệu quả nội dung: impressions/reach/view theo định nghĩa nền tảng, thời gian xem, retention, xem lại/tương tác nếu có; lưu tuổi bài và ngày đo. Thiếu chỉ số thì để unavailable, không điền 0.

Không suy nhân quả từ một clip hoặc một biến thể nhiều thay đổi; không chấm đạt chỉ vì prompt chứa từ khóa. Review có thể bị sửa khi có bằng chứng mới.

## Review câu chuyện — 2026-10-16

Dùng checklist tại [story-development.md](story-development.md). Tách tính đọc được của hook, tiến triển và giá trị key/hậu quả khỏi sở thích người review; phân biệt tự kiểm của AI, kiểm hiểu với người thật và analytics. Ghi unknown/not checked cho phần chưa quan sát. Không coi tổng điểm story là xác suất viral hoặc tự kết luận xem lại đồng nghĩa thích.

## Gate first frame

Theo [first-frame.md](first-frame.md) và hướng dẫn Project. Xem ảnh output thật, kiểm chi tiết và đo pixel/tỷ lệ; mọi tiêu chí bắt buộc pass, không lỗi chặn hoặc not_checked bắt buộc mới qa_pass. Model verification, image QA và user approval là ba trạng thái riêng. Không dùng giới hạn 5 lượt để hạ chuẩn. Chỉ kiểm ảnh không chứng minh timeline/chuyển động/audio của video.

## Kiểm file và trạng thái — v1.7

Khi có render, theo [media-review-and-finishing.md](media-review-and-finishing.md): đo duration thực, mức âm đầu–giữa–cuối; kiểm giải phẫu lúc reveal/ending, không lấy QA t=0 thay phần chưa thấy. Tách text hiện hành/render thực/QA từng miền/tạm duyệt/final; không suy actual settings từ prompt. Metrics không thay nghe hoặc xem liên tục.

## Skill đánh giá — v2.2.1

Mức video-reviewed và published-measured chạy qua [/na-danhgia](../.agents/skills/na-danhgia/SKILL.md): chấm độc lập với người viết prompt, ghi review/CURRENT-STATE/performance, không tự sửa hoặc render.

## QA nhiều vòng có bài học — v1.2, 2026-10-25

Bộ nội dung /na-chayvideo, chạy riêng hoặc trong /na-combo (UF-D026): QA tối đa **5 vòng**, dừng sớm khi đạt. Mỗi vòng do một agent reviewer độc lập chấm: context mới, chỉ nhận bảng tiêu chí, đầu ra và đường dẫn nguồn cần đối chiếu, không nhận lập luận của người viết. Reviewer chấm từng tiêu chí pass/fail/not_checked kèm lỗi cụ thể và hướng sửa; người viết sửa đúng lỗi rồi gửi vòng sau, reviewer kiểm cả hồi quy.

Bảng tiêu chí = tiêu chí gốc (output-contract, format, story, caption, sinh học/dụng cụ, địa điểm) + độ mới + độ hay theo creativity.md + mọi bài học theo memory-policy v2.2 (Ràng buộc Đã duyệt bắt buộc đạt; Ràng buộc Chờ duyệt bắt buộc xét). Hết 5 vòng chưa đạt: giữ bản tốt nhất, ghi "CHƯA ĐẠT" và lỗi còn lại, không hạ chuẩn. review.md ghi số vòng, kết quả từng vòng và bài học đã áp dụng. Môi trường không có công cụ agent thì ghi rõ giới hạn self-review. Ảnh first frame giữ hạn mức 5 lượt của /na-taoanh với cùng bảng bài học cho task ảnh.
