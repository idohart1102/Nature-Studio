# Truy xuất bài học theo ngữ cảnh

Version: 1.0 | Updated: 2026-10-17 | Nature Studio v1.8

Nguồn quyền/trạng thái vẫn là [memory-policy](memory-policy.md). Engine `scripts/memory_retrieval.py` dùng thư viện chuẩn Python; không gọi model, không tự học trọng số hoặc nâng trạng thái lesson. Một ID có một bản gốc. Nhãn đa trị giúp tìm, không tạo thư mục chủ đề hay bản sao lesson.

## Chọn trước, đọc sâu sau

1. Xác định Project và **giai đoạn công việc thật**. `mode new/revision/caption/reference` dùng cho bộ đầu ra; khi chỉ sửa một phần, truyền `--task` chính xác thay vì mở rộng cả mode. Hint từ brief gồm topic/entity/interaction; không buộc người dùng tự gắn tag. Dùng tên chuẩn/alias từ [taxonomy](memory-taxonomy.json); nhãn mới vẫn hợp lệ. Không giả model/interface yêu cầu là backend đã xác minh; thiếu thì bỏ điều kiện đó để trả unknown cần xét.
2. Query chỉ xét Project hiện hành + shared. `conditions` quyết định mâu thuẫn rõ; topic/entity/interaction chỉ xếp mức liên quan. Có ba trạng thái điều kiện: match, unknown, excluded. Điều kiện rỗng không thêm hạn chế, không chứng minh áp dụng toàn cục. Task lạ không bị loại bằng so chuỗi không hiểu. Không tự áp lesson Project khác.
3. Đọc mô tả ngắn trong kết quả, rồi **mở nguyên văn bản gốc** của bài có thể áp dụng; kiểm điều kiện/ngoại lệ/mâu thuẫn trước dùng. Summary không thay nguồn. Ghi ID/version/hash/path/cách dùng vào INPUTS; candidate thử riêng, không coi là luật. Ghi lesson đã xem khác lesson thật sự dùng.
4. Active/candidate/retired nằm trong ba nhóm tách biệt. Mặc định chỉ active; thêm `--candidates` khi nghiên cứu/thử/sửa lỗi hoặc `/na-dongvideo` kiểm trùng. `/na-dongvideo` không truyền task khi cần so ý nghĩa toàn namespace, rồi xét điều kiện gốc. Retired chỉ `--retired` để truy nguyên. Không tự biến approval video thành active lesson.

Ví dụ query cho review video (lệnh dùng đúng dữ liệu nhiệm vụ, không bốc mẫu làm quy chuẩn):

```text
python scripts/memory_retrieval.py query underwater --task video-review --topic tackle-continuity --entity muskie --interaction angling --text "dây câu phát sinh khi cá giãy" --candidates --out .nature-studio/memory/review-query.json
python scripts/memory_retrieval.py read underwater .nature-studio/memory/review-query.json --id L-ID-thuc-trong-ket-qua
```

Thay ID minh họa bằng ID thật được query trả về, không tự tạo lesson cho ví dụ. Query dùng `--model`, `--interface`, `--format` lặp lại khi có dữ liệu chính xác; không nhập giả để ép match. `read` xác minh bản gốc, status, hash, namespace fingerprint và điều kiện; không tự cấp quyền áp candidate.

## Không cắt top-k rồi coi là đủ

Kết quả phân trang mặc định12 dòng, tối đa100 dòng/lần; đây là kích thước batch, không là giới hạn tổng bài liên quan. `remaining`/`next_cursor` báo phần chưa xem; gọi lại cùng query và `--cursor` để đọc tiếp. Không đổi tham số giữa các trang. Dòng `deferred` là xếp thấp, không phải loại bỏ; `needs_review` gồm bài cũ thiếu nhãn hoặc điều kiện chưa rõ. Không bỏ qua unknown chỉ vì hết batch.

AI cần xét các active/unknown chưa có quyết định trong phạm vi nhiệm vụ; muốn hoãn phải có lý do dựa trên descriptor/điều kiện, không chỉ điểm số. Khi query rộng/rỗng, lỗi chưa giải thích được hoặc taxonomy chưa phủ, dùng `--broad` và phân trang mô tả ngắn toàn active không mâu thuẫn điều kiện. `discovery_complete` chỉ nghĩa đã duyệt hết trang và không lỗi cấu trúc; **không chứng nhận semantic coverage**. Nếu nhiều bài thật sự liên quan, phải đọc đủ; không đánh đổi tính đúng để giảm token.

`errors` có đường dẫn/mô tả lỗi parse, scope/status, ID trùng hoặc dữ liệu chưa đầy đủ. Khi có lỗi, dừng kết luận coverage; mở đúng nguồn và xử lý trước khi áp lesson, không giả không có bài. Bài không có object `retrieval` vẫn có summary từ action và cờ legacy; không tự cắt action làm mất ngoại lệ. Quy chuẩn Project/Standards bắt buộc vẫn đọc theo nhiệm vụ, không phụ thuộc retrieval rank.

## Packet và freshness

Packet schema2 trả `memory` là một trang descriptor, không nhúng toàn bộ INDEX hoặc mọi active. Dùng query độc lập nếu cần thêm hint/task/page; nạp nguồn đã chọn bằng:

```text
python scripts/chayvideo_context.py packet underwater --mode revision --species muskie --interaction angling --memory-selection .nature-studio/memory/revision-query.json --lesson-id L-ID-thuc --out .nature-studio/context/revision.json
```

Query dùng cho packet phải có cùng mode; task có thể thu hẹp phần đang sửa. `--lesson-id` lặp lại chỉ nhận ID đã xuất ở trang selection, còn khớp hash/fingerprint. Không cần nhồi mọi lesson đã mở vào packet nếu INPUTS đã ghi nguồn; vẫn phải kiểm freshness trước áp/lưu. Verify schema1 cũ còn hỗ trợ discovery cũ; khi tiếp tục nhiệm vụ nên dựng schema2, không sửa INPUTS lịch sử.

Catalog tự dựng tại `.nature-studio/memory/<slug>/catalog.json`, giữ inventory/hash và metadata đầy đủ **chỉ local**. Mỗi query/verify đọc nguồn local để phát hiện thêm/sửa/xóa/chuyển status; không chỉ kiểm bài đã chọn hoặc dựa INDEX. Đây là tiết kiệm nội dung AI phải đọc, không cam kết giảm mọi I/O filesystem. Cursor gắn query, page size, taxonomy và fingerprint; nguồn đổi phải query lại. Cache mất được dựng lại, không cần xóa lesson. Không in catalog nguyên bộ vào chat.

## Lưu và xuất bản

`retrieval` tùy chọn: `schema:1`, `summary` có hành động/giới hạn cần thiết, `topics`, `entities`, `interactions` là danh sách nhãn. Không nhân đôi scope/tasks/model làm nguồn quyền thứ hai. `/na-dongvideo` đọc nguồn và bổ sung nhãn khi tạo/sửa lesson, kiểm trùng; không nâng candidate để tiện truy xuất. Lesson legacy tiếp tục dùng qua fallback, JSON retrieval có mặt nhưng lỗi phải sửa/báo lỗi.

Theo [publication](publication.md), metadata mới cũng cần làm sạch nếu công khai. Catalog/query/selection log không xuất; public INDEX được dựng trong staging từ các lesson `public/reviewed=true` thực được xuất, không từ catalog runtime. Giữ ID/version/status và bằng chứng hợp phạm vi; không làm mất private originals khi nâng cấp. Không xuất JSON catalog ở `05-Memory`; guard chặn để tránh lộ descriptor riêng. Bản đầu không thêm public JSON index vì Markdown INDEX và source metadata đã đủ rebuild.
