# Phân luồng nguồn cho /na-chayvideo

Version: 1.1 | Updated: 2026-10-22 | Source-preserving stage routing; chưa đo chất lượng model đối chứng.

Một skill tiếp nhận, hai workflow tạo mới và sửa. Nguồn nội dung là Standards/Project/Knowledge/Models; helper chỉ chọn và trình bày nguyên văn. Không tóm tắt thay nguồn bắt buộc, cắt theo quota token hoặc mặc định nguồn cũ vẫn còn trong context.

## Nguồn có thể chỉnh độc lập

`03-Projects/<slug>/context-map.json` giữ danh sách nguồn đầy đủ theo mode, hồ sơ loài và dụng cụ. Trường `routing` trỏ tới cấu hình giai đoạn riêng, ví dụ [Underwater](../03-Projects/underwater/context-routing.json). Thêm/sửa tài liệu Knowledge không cần sửa skill; cập nhật các đường dẫn khi thêm tài liệu. Loài mới chưa có profile vẫn nghiên cứu đúng loài, không dùng loài thay thế.

Cấu hình routing schema 1 có `modes` (profile hoặc alias), `stages` và `effects`. Mỗi stage ghi `sources`, `tasks`, boolean `species`/`angling`; `task_overrides` đổi task của alias reference mà vẫn kế thừa nguồn new. Mỗi effect ghi `sources`, `tasks`, `requires`. Tasks/effects lấy từ nhiệm vụ thực; effect chỉ **thêm** phụ thuộc. Camera có thể ảnh hưởng nhận dạng/rig/t=0; đổi nguồn âm khác sửa mức mix. Không suy từ vài từ khóa rằng các phần còn lại chắc chắn giữ nguyên.

Danh sách mode ở context-map là mức bao phủ tối thiểu. Nguồn mới chưa có stage được đưa vào mọi stage (`unassigned`); không âm thầm mất nguồn khi cấu hình chậm cập nhật. Mode/stage/effect chưa được cấu hình quay về nguồn toàn nhánh. Cấu hình sai schema, alias vòng hoặc thiếu tài liệu bắt buộc là lỗi phải xử lý/đọc gốc. `reference` giữ creativity/story theo chuẩn reference, không nhận yêu cầu phải đổi chuyện của new độc lập. Khi thêm ràng buộc mới vào một nguồn ở stage muộn, người bảo trì phải xét có cần đọc nó sớm trước concept không; hash không tự hiểu yêu cầu mới.

## Tạo output ban đầu

Sau đọc START-HERE/SYSTEM và chọn Project, dùng các stage theo quyết định thực:

Brief đã đủ và nhiệm vụ là fullset thì ưu tiên `--stage all` + view một lần: giữ cùng nội dung nguồn với baseline và tránh nhiều header/tool-call. Chia stage khi việc làm rõ/chọn hướng có thể tránh đọc sâu các nguồn chưa dùng, hoặc khi nguồn đã được giữ đủ trong cùng context. Không chạy năm stage chỉ để gọi là có phân luồng.

| Stage | Đọc để làm gì |
|---|---|
| orient | Project/chính sách; xác định brief/loài/quyền chọn và phần thiếu trước nghiên cứu sâu. |
| concept | Creativity/story chung và Project, format/contract/khán giả/giới hạn model trước chọn chuyện, nghiên cứu/Knowledge loài–môi trường–tương tác, tackle khi cần; rà lịch sử và lesson đúng nhiệm vụ. |
| write | Contract, format, giọng caption/model và Knowledge liên quan; mở bổ sung theo concept thật đã chọn. |
| review | Đối chiếu nội dung, sinh học/vật lý, liên đới bốn mục và QA đúng vật được cung cấp. Chỉ thêm `video-review`/`audio-review` khi có nhiệm vụ tương ứng, không giả đã xem/nghe. |
| save | Production/ID/lưu hồ sơ, kiểm coverage, source provenance; đủ nội dung thật mới reserve. |

Stage không phải quyền hoãn ràng buộc có ảnh hưởng quyết định sớm. Project/map/links yêu cầu nguồn nào thì mở thêm nguồn đó. Không giới hạn sáng tạo vào nhãn nguồn. Không nạp cả packet lẫn từng file có cùng toàn văn. `--stage all` giữ đường đọc đầy đủ khi chưa chắc hoặc muốn đọc một lần.

Ví dụ lệnh (tên file/context do AI chọn theo nhiệm vụ thật):

```text
python scripts/chayvideo_context.py packet underwater --mode new --stage concept --species muskie --interaction angling --out .nature-studio/context/task-concept.json
python scripts/chayvideo_context.py view .nature-studio/context/task-concept.json --context-id ctx-20261022T090000-ab12 --ledger .nature-studio/context/ctx-20261022T090000-ab12.json
```

Packet schema3 giữ toàn văn và manifest local; context-map.json là dependency (mức phủ tối thiểu), không còn là nguồn in ra. `view` verify trước rồi in nguyên văn, không JSON-escape body hoặc in hash dài. Mặc định mỗi batch nhắm 18.000 ký tự body và chỉ chia giữa các nguồn, không cắt một nguồn; nguồn lớn đứng riêng. Với tool cắt output sớm, thêm `--page-large`: nguồn dài hơn `--max-chars` được chia trang theo heading, trang ghép lại đúng nguyên văn, và nguồn chỉ tính đã đọc khi đủ mọi trang trong cùng context. Còn `NEXT SOURCES.count` thì đọc tiếp cùng packet, dùng receipt batch trước với seen/retained và ghi receipt mới. Chỉ xong khi count=0 và coverage đạt. Có thể chỉnh `--max-chars` theo output budget của tool; `--all-sources` chỉ khi bảo đảm tool nhận đủ. Memory descriptor chỉ rút khỏi lần in lặp của cùng packet khi được xác nhận còn trong context; task mới vẫn hiện descriptor mới. Nếu output bị truncated, không tái dùng receipt đó; dùng `--source <path>` và công cụ đọc từng phần để đọc đủ, hoặc fallback đọc gốc và ghi chưa được helper kiểm. `--receipt` chỉ ghi dưới context/audit local, không ghi đè receipt hoặc file nguồn.

## Sửa output

Resolve bản đầu vào được chọn theo [lõi chung](video-prompt-workflow.md); giữ chuyện và phần đã chốt. Chọn `--mode revision --stage write`, thêm effect thực như `--effect camera`, `rig`, `species`, `environment`, `story`, `audio-level`, `audio-source`. Cấu hình hiện tại giữ toàn bộ nhóm nguồn nền của revision-write; không tự bật đường cắt bớt Knowledge chỉ vì người dùng nói “chỉ sửa”. Caption-only dùng mode caption/stage write và nguồn clip đủ chứng minh nội dung. Không dùng stage concept để brainstorm lại clip revision.

Khi thực sự đánh giá render và âm, thêm `--effect video-review --effect audio-review` hoặc lặp `--task` chính xác; tasks được hợp với task stage, không thay thế nhiệm vụ viết bằng một bộ lọc hẹp. Query độc lập theo memory-retrieval vẫn hỗ trợ hint, candidates và phân trang; candidate không thành luật. Phần chưa rõ quay lại full branch và các nguồn bổ sung tương ứng.

## Không đọc lặp và không mất ngữ cảnh

Mỗi chat/epoch có một ledger: `chayvideo_context.py context-id` (hoặc `preflight`) cấp context_id duy nhất theo thời điểm và đường dẫn `.nature-studio/context/<context_id>.json`. `view --ledger <ledger> --context-id <context_id>` tự đọc và ghi lại ledger; lần gọi tiếp theo trong cùng chat thêm `--retained`. Chỉ dùng `--retained` khi AI xác nhận mọi nguồn trong ledger đã được đọc đủ, không truncated và toàn văn còn trong ngữ cảnh hiện tại. Ledger ghi các nguồn/trang đã hiển thị và hash, không chứng minh AI đã hiểu. Ledger phải mang đúng tên context_id; ledger đã tồn tại mà thiếu `--retained` bị từ chối. Sau compaction, mở chat khác, mất ngữ cảnh hoặc chưa chắc: lấy context_id mới và đọc lại nguồn cần dùng. `--seen/--receipt` (một file mỗi lượt) vẫn được hỗ trợ.

```text
python scripts/chayvideo_context.py packet underwater --mode new --stage write --species muskie --interaction angling --out .nature-studio/context/task-write.json
python scripts/chayvideo_context.py view .nature-studio/context/task-write.json --context-id ctx-20261022T090000-ab12 --ledger .nature-studio/context/ctx-20261022T090000-ab12.json --retained
```

Không tự nhận có thể xóa token đã nằm trong lịch sử của host. Stage giúp tải đúng lúc; tổng bộ nguồn tạo fullset vẫn phải đủ như baseline. Reuse chỉ tiết kiệm lần đưa lại cùng văn bản. Source/map/config, helper builder/router, skill/workflow, taxonomy và memory inventory thay đổi làm packet cần kiểm lại; cập nhật tài liệu có thể yêu cầu dựng lại cả plan.

## Kiểm trước lưu/giao

Với workflow hiện tại, cần đủ toàn bộ tập nguồn nền của mode qua các stage hoặc packet all, cộng nguồn do effects yêu cầu. Chạy coverage trên các packet đã đọc và receipt còn giữ, ví dụ:

```text
python scripts/chayvideo_context.py coverage .nature-studio/context/task-concept.json .nature-studio/context/task-write.json .nature-studio/context/task-review.json .nature-studio/context/task-save.json --ledger .nature-studio/context/ctx-20261022T090000-ab12.json --context-id ctx-20261022T090000-ab12 --retained
```

Với receipt kiểu cũ chưa bao gồm các nguồn trước, truyền nhiều `--receipt`. `complete=false` phải mở nguồn còn thiếu hoặc dựng lại packet stale; thiếu Python/receipt thì đọc gốc theo workflow và ghi chưa được helper kiểm. Complete chỉ là khai báo bao phủ nguồn file, không chứng nhận độ mới câu chuyện, semantic coverage, áp lesson đúng hoặc QA media. History/lesson/research và liên đới bốn mục vẫn phải kiểm theo quy chuẩn. Ghi paths/version/hash/cách dùng thực vào INPUTS, không in toàn bộ manifest vào output người dùng.

Chưa bật tự loại các đoạn Knowledge theo điểm số hay tóm tắt bằng LLM. Muốn giảm tiếp bằng section routing phải có bản đồ phụ thuộc/ngoại lệ và đối chứng đầu ra trước; không lấy số token làm lý do hạ chất lượng.
