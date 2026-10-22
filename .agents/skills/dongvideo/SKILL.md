---
name: dongvideo
description: Tổng kết phiên video Nature Studio khi gọi /dongvideo hoặc yêu cầu đóng phiên, rút bài học từ production; cập nhật bộ nhớ Project và đánh giá đóng góp bộ nhớ chung. Không kích hoạt khi chỉ hỏi, trích dẫn hoặc sửa skill; không render hay xuất bản.
---

# /dongvideo

Version: 1.4 | Updated: 2026-10-18 | Nhận XX-YYYY và hai định dạng legacy; giữ truy xuất chọn lọc

Nhận lệnh trong tin nhắn, không giả định giao diện đã đăng ký slash command. Dùng workspace chứa skill làm gốc (đi lên ba cấp từ thư mục skill). Đầu ra tiếng Việt. Đóng phiên là chốt ghi nhận hiện tại, không cấm tiếp tục sửa video.

## Đọc và xác định đúng hồ sơ

Đọc START-HERE.md, SYSTEM.md, 00-Standards/memory-policy.md, production.md, quality-review.md, 06-Evaluation/README.md và mẫu session-review/lesson. Chính sách bộ nhớ là nguồn duy nhất cho quyền đổi trạng thái; không tự nới tiêu chí.

Ưu tiên Project/production người dùng nêu. Nếu chỉ có mã, đối chiếu PROJECT.md và hồ sơ thực; không giả định prefix độc nhất khi import nhiều nguồn. Nếu không có mã, dùng ngữ cảnh khi chỉ có một production phù hợp; hỏi một câu khi còn mơ hồ, không đoán theo file mới nhất. Chủ đề chưa đủ để đóng video cụ thể. Không tạo production giả để chạy lệnh.

Đọc PROJECT.md, quyết định/format liên quan, SUMMARY, brief, concept, feedback, các attempt và review thực, gồm review/performance do /danhgia ghi nếu có. Liệt kê file trước khi kết luận thiếu lịch sử; không chốt danh sách A01–A04 cố định. Đọc phần chat đang truy cập được và dữ liệu người dùng cung cấp; lưu phản hồi cần giữ vào feedback kèm nguồn/ngày/phạm vi, không nhận đã thấy toàn bộ phiên cũ. Mở media khi cần/được phép bằng công cụ phù hợp; không xem/nghe được thì ghi giới hạn, không suy pass từ tên file hay prompt.

## Tổng kết và học ở hai cấp

Theo [truy xuất bộ nhớ](../../../00-Standards/memory-retrieval.md): query Project + shared với `--candidates` khi tìm trùng, không giới hạn task nếu cần so toàn namespace; phân trang descriptor rồi mở bài gốc liên quan. Khi tạo/sửa lesson, bổ sung `retrieval` summary/topics/entities/interactions sau đọc nguồn, giữ ID/status/evidence/quyền chia sẻ; query lại để catalog phản ánh thay đổi. Candidate không thành luật, unknown không bị bỏ qua; không nạp toàn bộ INDEX/body để bắt đầu.

- Xác định dữ liệu mới so với SESSION-REVIEW.md; so nội dung/hash/phiên bản, không chỉ ngày. Cùng dữ liệu và không có thay đổi thì báo không có cập nhật, không thêm entry/lesson lặp.
- Tách kết quả thực, phương pháp có ích, lỗi, đánh đổi, giả thuyết nguyên nhân và việc chưa kiểm. Không chỉ gom lỗi; render đẹp hoặc lời AI lặp lại không là bằng chứng độc lập.
- Đọc descriptor phân trang và lesson gốc liên quan của Project và shared theo lõi truy xuất; INDEX dùng điều hướng/kiểm chỉ mục khi cần. Tìm trùng theo hành động/điều kiện/cơ chế trước khi tạo ID. Chỉ đọc bộ nhớ Project khác khi được giao đánh giá chuyển giao.
- Luôn đánh giá riêng bài học Project và đóng góp shared. Đổi chủ đề phương pháp còn có ích không? Phụ thuộc model/giao diện/format nào? Hành động/bằng chứng gì? Kỹ thuật không tự là chung, đặc tính loài không thành quy tắc toàn kho. Không có đóng góp mới thì ghi lý do ngắn, không ép tạo lesson.
- Định tuyến dữ kiện → Knowledge, giới hạn model → Models, chỉ thị lâu dài → quy chuẩn/decisions theo quyền rõ đã có, quan sát cục bộ → production. Không tự sửa các nguồn từ suy đoán. Lesson chỉ ghi phương pháp mới và dẫn nguồn, không nhân bản quy chuẩn.
- Tự ghi/cập nhật candidate ở Project hoặc shared; giữ ID khi bổ sung bằng chứng/chuyển phạm vi. Một sự việc có hai lesson chỉ khi khác hành động/phạm vi. Nếu active mất căn cứ, ghi mâu thuẫn và đưa về candidate theo policy; giữ lịch sử, sửa chỉ mục/liên kết.

## Kiểm chứng và kích hoạt

Chỉ tự kích hoạt procedural lesson khi **mọi** điều kiện automatic trong memory-policy.md đạt; ghi ca kiểm thực tại 06-Evaluation/results và activation. Không dùng kiểm schema làm bằng chứng hiệu quả video/quyết định AI. Không tự render/mua lượt/chạy thử có phí để đạt gate; thiếu công cụ/dữ liệu thì candidate. Nguồn tài liệu hỗ trợ bằng chứng, không thay kết quả kiểm cần cho kết luận đó.

Kết luận sáng tạo, thị hiếu, hiệu quả model/khán giả hoặc nhân quả chưa tách biến giữ candidate, gom mục cần kiểm/duyệt theo đợt; không ngắt phiên hỏi từng lesson. User-authorized dẫn tới phản hồi/quyết định đã lưu, giữ giới hạn sự thật; phê duyệt thiết kế hệ thống không phải duyệt tất cả lesson tương lai.

Kiểm lesson đã dùng qua INPUTS ID/version và kết quả attempt mới: đã dùng không chứng minh có ích. Chỉ có prompt thì kết luận giới hạn prompt. Không tạo review/performance/QA giả để chốt.

## Ghi và bàn giao

Tạo/cập nhật SESSION-REVIEW.md theo mẫu, entry mới khi có bằng chứng mới, giữ entry cũ. Cập nhật feedback/SUMMARY/idea-ledger chỉ ở phần có thay đổi thực, không đổi selected/approved/published nếu thiếu căn cứ. Không ghi đè attempt/prompt/media. Lesson metadata dùng JSON frontmatter theo mẫu, đường dẫn portable; đồng bộ INDEX Project, shared và root.

Chạy `python scripts/validate_memory.py`, kiểm diff/link/ID, quyền đổi trạng thái và phạm vi. Validator không thay đánh giá nội dung. Không ghi suy luận nội bộ. Nếu ghi dở/lỗi, báo phần chưa xong, không nhận đã đóng đủ.

Trả ngắn bằng tiếng Việt: production/phạm vi tổng kết; kết quả; bộ nhớ Project; đóng góp shared (hoặc không có); active mới kèm căn cứ/candidate chờ; file thay đổi và việc tiếp theo. Không nhận video đã duyệt vì đã tổng kết. Không tự commit/push/publish hay tạo media từ lệnh này.

Nhận mã XX-YYYY và mã legacy XXX-YYYYY hoặc UF-0001. Đọc IDENTITY.json khi có để đối chiếu Project/video UUID; không cấp lại mã khi tổng kết, không yêu cầu đổi mã cũ và không đoán Project chỉ từ prefix.

## Phân biệt ghi nhớ local và chia sẻ

Đọc 00-Standards/publication.md. Lesson mới mặc định publication.visibility=private, reviewed=false. Trong báo cáo, tách bài học có thể đóng góp bản cập nhật hệ thống khỏi nguồn production riêng; không tự gửi lên GitHub hoặc coi nhãn public là active. Khi được giao publish, rà/làm sạch bài học theo policy, giữ bằng chứng riêng local và chỉ xuất căn cứ được chia sẻ. Không lược bỏ hết lessons khỏi bản cập nhật chỉ vì không xuất production.

Khi có asset/ref, ghi ID/revision/hash và phần thật đã dùng/QA trong hồ sơ; metadata/hash không chứng minh actual inputs. Bản public/private cùng ID/version có thể khác nội dung: đối chiếu nguồn/hash trước merge, không ghi đè hoặc tự active từ bản kể một phiên.
