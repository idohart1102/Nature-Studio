# Lõi viết prompt và lưu hồ sơ video — v1.5

Updated: 2026-10-22 | Một lõi cho na-chayvideo/na-clonevideo; nguồn nguyên văn theo giai đoạn.

## Context đúng nhiệm vụ

Chọn Project từ metadata hiện hành. Nguồn do context-map và routing Project chọn; giữ toàn văn, không tóm tắt/cắt theo quota. Lệnh dùng dữ liệu thật, đường dẫn local tương đối:

```text
python scripts/chayvideo_context.py preflight <slug> --mode new|revision|caption|reference --species <tên> --interaction natural|angling|unspecified
python scripts/chayvideo_context.py view <packet> --context-id <context_id> --ledger <ledger> --max-chars <batch> --page-large
```

`preflight` dựng packet `--stage all`, cập nhật cache history (new/reference) và chỉ in đường dẫn, số nguồn, ID memory, pending, context_id/ledger mới và lệnh view kế tiếp; không thay việc đọc nguồn. Thay placeholder thật; `--species` lặp cho nhiều loài. Loài chưa có profile phải nghiên cứu đúng đối tượng; chưa rõ interaction giữ unspecified. Pending trống không chứng nhận brief đầy đủ. Output gate loài/tag/key riêng Project không áp sang mọi Project.

New/reference có thể chia `orient → concept → write → review → save`: orient làm rõ brief; concept đọc creativity/story, format và Knowledge trước chọn chuyện; write đọc contract/model/giọng và nguồn liên quan; review tự kiểm; save đọc production/IDs trước cấp mã/lưu. Giữ nguồn theo chuẩn reference, không ép mới so mẫu. Revision dùng write/review/save, caption dùng write; `--stage all` đọc đầy đủ một lần khi chưa chắc. Source mới chưa phân stage vẫn được nạp. Nguồn đang ảnh hưởng quyết định phải mở ngay, không chờ stage sau.

Thêm `--effect camera|rig|species|environment|story|audio-level|audio-source` cho ảnh hưởng thật; effects chỉ thêm phụ thuộc. Khi có nhiệm vụ review render/âm, dùng effect video-review/audio-review hoặc lặp `--task` đúng nhiệm vụ. Không giả review chỉ từ prompt.

View verify trước đọc và in nguyên văn theo batch; không cần đọc JSON/hash. `--max-chars` theo giới hạn output của tool: khoảng 30000 khi tool nhận đủ, 10000 khi tool cắt output sớm. `--page-large` chia nguồn dài hơn batch thành các trang theo heading; nguồn chỉ tính đã đọc khi đủ mọi trang trong cùng context. Không có cờ này thì nguồn lớn đứng riêng, không bị cắt. Còn NEXT SOURCES.count thì gọi lại đúng lệnh view kèm `--retained`; ledger `.nature-studio/context/<context_id>.json` tự ghi các nguồn/trang đã hiện. Truncated thì không dùng `--retained` cho phần đó; đọc đủ bằng `--source`/file tools hoặc fallback đọc gốc, ghi chưa được helper kiểm. `--retained` chỉ khi mọi nguồn trong ledger đã đọc đủ và nguyên văn còn trong context. Ledger không chứng minh AI đã hiểu. Chat mới, sau compaction hoặc không chắc: chạy `chayvideo_context.py context-id` lấy context_id/ledger mới và đọc lại; ledger của chat khác không bao giờ tính là đã đọc. Packet stale phải dựng lại. `--seen/--receipt` cũ vẫn dùng được.

Trước lưu/giao, `python scripts/chayvideo_context.py coverage <các-packet-đã-đọc> --ledger <ledger> --context-id <context_id> --retained`. Complete=false phải đọc nguồn thiếu/dựng lại nguồn stale. Coverage chỉ kiểm khai báo đủ nguồn, không thay QA ngữ nghĩa/history/media. Lưu manifest paths/version/hash vào INPUTS, không in vào bốn mục. [Cấu hình/tuỳ chọn chi tiết](context-routing.md) đọc khi bảo trì hoặc chưa rõ lệnh, không nạp mỗi lượt.

Memory theo [truy xuất chọn lọc](memory-retrieval.md): descriptor Project/shared theo task, xét hết trang/unknown/legacy và mở bài gốc phù hợp. Candidate không là luật. Nguồn tham chiếu/hồ sơ thực vẫn cần đọc riêng; quyết định/baseline/benchmark chỉ mở khi cần, không mặc định nạp lại. Thiếu Python/map/nguồn hoặc cấu hình sai: đọc Project/format/contract/giọng và Knowledge/model/creativity/story cần cho mode, bổ sung nguồn gốc; không đoán cấu hình hoặc nhận helper đã kiểm.

## Lưu và kiểm

### Fingerprint lịch sử

Sau khi đọc các nguồn thực, AI viết JSON gồm chuỗi `opening`, `interaction`, `objects`, `terrain_role`, `trigger`, `key_action`, `consequence`. Ghi cơ chế đủ cụ thể để so xuyên loài, không chỉ nhãn/tóm tắt tiêu đề. Chạy `python scripts/chayvideo_context.py fingerprint <slug> <ID> <json> --from-history`: helper lấy `source_hashes` từ lần `history` AI đã xem, không cần chép hash; công cụ từ chối nếu nguồn đổi sau đó, nhưng không chứng minh AI đã đọc hoặc hiểu. `history` mặc định in đường dẫn tương đối production; `--full` mới in hash. Với hồ sơ mâu thuẫn/nhiều revision, phản ánh trạng thái và các cơ chế đã giao, không xóa nháp cũ khỏi đối chiếu. Bất kỳ thay đổi văn bản/attempt sau đó làm capsule hết hạn. Không backfill toàn kho ngoài nhu cầu nhiệm vụ; khi không có capsule thì đọc nguồn gốc như thường.

Đủ bộ nội dung thật mới reserve video mới qua `python scripts/video_ids.py reserve <slug>`; sửa clip dùng ID cũ. Đọc production.md và video-identifiers.md trước lần cấp mới trong phiên. Không cấp ID từ tra cứu/caption-only.

Lưu một JSON local với các trường đầu ra được giao; cho Underwater fullset thêm metadata nội bộ `checks.key_onset` là số giây dự định thật `checks.hook_signal` là giây dự định của tín hiệu mới trong 3 giây đầu (0 < t ≤ 3.0, UF-D025) và `checks.location_tag` là hashtag địa điểm đã khóa (legacy chưa có setting: `checks.location_none_reason`). Helper kiểm tag đó có đúng một lần trong mọi caption và video prompt new/reference có camera handheld (UF-D021); việc chọn đúng vùng vẫn là QA nội dung. Metadata không xuất thêm vào bốn mục cho người dùng. Chạy `python scripts/chayvideo_output.py check <json> --project <slug> --mode <mode>`. Script chỉ kiểm cú pháp/số tag/timecode, không xác nhận tiếng Anh, sinh học, key thật hay QA media; AI vẫn tự kiểm nội dung theo Project. Nếu kiểm lỗi thì sửa trước giao. Không lách validator bằng timecode/metadata khác lời prompt.

Có thể dùng `save <json> --project <slug> --production <ID> --mode <mode>` thay `check` để tạo attempt mới. Trong JSON thêm `files` gồm chuỗi `INPUTS.md`, `settings.md`, `review.md`, tùy chọn `revision.md`; ghi trung thực nguồn/hash/lesson/ảnh input và phần giữ nguyên, model/settings chưa thực thi/unknown, review prompt-only. Script chỉ tạo attempt, không tự viết nghiên cứu hoặc kết luận. Thiếu công cụ thì lưu theo template bằng file tools, không ghi đè attempt.

Sau lưu, hoàn tất brief/research/concept/SUMMARY/feedback/performance thực và ledger theo production.md; không để save attempt thay phần hồ sơ này. Concept ghi story card/so sánh/giới hạn; cập nhật ledger ngay drafted, không chờ render. Caption-only ghi revision/nguồn attempt trước, giữ prompt/chuyện cũ bằng tham chiếu, không chế bốn output mới hoặc đánh dấu selected/approved/published. Nếu có FIRST-FRAME.json, kiểm file/hash/review và ảnh thật khi cần tiếp nối; không sửa quota/handoff từ việc soạn prompt.

Rà cú pháp đạt khác với nội dung đạt, ảnh/video đạt hoặc khán giả thích. Báo giới hạn quan trọng, không tự render để kiểm. Không in suy luận nội bộ hay báo cáo dài vào bốn mục.

### Tiếp tục đúng bộ đầu vào

Khi tiếp tục/revision/caption, xác định attempt theo yêu cầu, SUMMARY và nguồn thực; không lấy Axx lớn nhất. `python scripts/chayvideo_output.py resolve A03 --project <slug> --production <ID>` trả bốn trường đã ghép và nguồn từng trường; nếu layout dùng attempts/ thì truyền `attempts/A03`. Lệnh chỉ đọc, không chọn/duyệt bản hoặc cập nhật SUMMARY. Chỉ resolve khi cần tiếp nối, không đọc toàn chuỗi thủ công nếu kết quả đủ và không mâu thuẫn brief/chat hiện hành.

JSON gửi `save` ở mode revision/caption bắt buộc có `base_attempt` (đường dẫn attempt tương đối production) và `base_sha256` từ resolve bản gốc vừa kiểm: chạy `resolve ... --out .nature-studio/context/<ID>-base.json` rồi `save ... --from-resolve <file đó>` để helper tự điền, không chép hash; nếu JSON tự ghi base thì phải khớp file resolve. Chỉ ghi trường thật sự sửa. Helper giữ quan hệ/hash trong OUTPUT.json; từ chối nguồn thiếu/đổi, vòng tham chiếu hoặc SAVE-INCOMPLETE.txt. Nhánh khác không tự nhập vào bộ đang dùng. Resolve không xác minh ngữ nghĩa; AI kiểm tính liên đới giữa phần giữ và phần sửa. `check` vẫn chỉ kiểm cú pháp; `save` mới kiểm nguồn kế thừa.

`frame_state` là object nội bộ gồm bốn chuỗi không rỗng: `subjects` (chủ thể, số lượng, nhận dạng, vật/rig), `environment` (sinh cảnh/ánh sáng/chất liệu), `composition` (camera, vị trí/tỷ lệ, đường diễn biến cần chừa), `initial_state` (trạng thái/quan hệ tại t=0). Ghi đủ chi tiết khóa theo concept. Nên ghi từ fullset mới và bắt buộc đủ trước khi tạo handoff ảnh schema 2; không xuất thành mục thứ năm. Đây là khai báo AI cần đối chiếu, không phải máy chứng minh t=0 đúng.

Revision đổi idea/video/first-frame prompt phải đánh giá lại frame_state: nếu t=0 không đổi, truyền nguyên object đã đối chiếu; nếu đổi, ghi trạng thái mới. Không khai báo thì resolver đánh dấu unverified, không âm thầm kế thừa xác nhận cũ. Caption-only chỉ sửa caption, tự kế thừa frame_state và không làm mất hiệu lực ảnh. Thay câu chữ concept không tự bắt QA ảnh nếu opening đã được đối chiếu giữ nguyên. First-frame prompt đổi thì cần đối chiếu ảnh lại, không tự sinh lại.

Hồ sơ cũ fullset có OUTPUT.json vẫn resolve được; thiếu frame_state là unverified. Attempt chỉ có Markdown hoặc partial không rõ base phải mở nguồn để xác định, không suy theo số/thời gian. Nếu cần tiếp nối bằng helper, lưu một fullset snapshot mới sau khi đọc/đối chiếu bốn trường thật (`save --mode new` với **ID hiện có**, ghi nguồn legacy vào INPUTS); không cấp ID mới, không sửa attempt cũ và không giả đã tạo concept/media mới. Snapshot là cầu nối rõ ràng, không backfill toàn kho. Không có Python thì dùng tham chiếu từng trường trong INPUTS, ghi chưa được helper kiểm, không giả resolve đạt.

Nếu dùng ảnh đã QA, theo [kiểm liên kết first frame](first-frame.md#kiểm-liên-kết-ảnh-trước-tái-dùng); không chạy kiểm ảnh cho caption-only khi không có việc dùng ảnh.

## Khi tiếp nhận media thực — v1.7

Theo [kiểm media và finishing](media-review-and-finishing.md) khi nhận reference hoặc render; chỉ viết prompt không cần chạy đo. Tách khả năng trích xuất, ASR và hiểu hình/âm thực; giữ trạng thái text/render/QA/approval độc lập trong SUMMARY. Bộ đầu ra vẫn bốn mục.

## Bộ nhớ schema2 — v1.8

Task/hint từ nhiệm vụ thật, cùng lõi memory_retrieval.py cho new/revision/caption/reference và skill ảnh/đóng phiên. Đọc memory-retrieval.md lần đầu dùng; packet chưa chọn lesson không chứng minh đã áp bộ nhớ. Lưu selection/query local, mở nguyên văn bài có thể dùng; tiếp tục next_cursor hoặc --broad khi cần. Verify xét cả inventory namespace để phát hiện bài mới/đổi status ngoài selection, không chỉ hash bài đã dùng. Khối sources và memory.errors/pending cần kiểm trước giao.

## Profile và planned asset — v2.1.0

Profile đúng loài cung cấp nhận dạng, cỡ/biến thể, hành vi và điểm đáng xem có điều kiện; phát triển chuyện mới theo creativity/Story Development, không biến cá thể lớn thành mặc định hoặc lịch bản mẫu. Sau chọn cảnh, tra asset đúng entity/stage/role/rig theo [hướng dẫn catalog](knowledge-routing.md#catalog-asset-local) khi cần ref. Không xem toàn album hoặc thêm rig cho natural prey. Caption chỉ cần thêm nguồn nếu có claim mới; revision giữ phần đã tốt và kiểm ảnh hưởng thực.

Receipt asset có thể gắn packet bằng `--asset-selection <receipt.json>` và gắn output bằng `asset_selection` ngoài frame_state. View chỉ hiện ID/path/giới hạn liên quan; mở ảnh thật riêng, không dump catalog. Thiếu review nằm ở `asset_review_pending`, độc lập source coverage; không giả visual pass. Selection stale phải dựng lại. Planned refs khác actual inputs/settings của render; khi đổi nội dung có liên quan, resolve giữ thiếu binding là unverified chứ không tự chứng nhận ảnh cũ.

Check/save giữ `checks` và phiên bản contract; metadata dự định không là kết quả render. Mặc định Underwater 5–10 beat, beat đầu kết thúc ≤3.0s và các gate hiện hành. Ngoại lệ số beat chỉ theo yêu cầu thật được đối chiếu, có scope/hash/target attempt; đọc [binding ngoại lệ](templates/README.md#binding-ngoại-lệ-beat) khi cần, không nạp schema này ở mọi lượt. Nhiều cử động trong một beat không tự đòi tăng beat.

## Nhu cầu tham chiếu nội dung → ảnh — v2.1.1

Mỗi bộ nội dung mới/reference hoặc revision hình ghi `reference_requirements` trong OUTPUT/INPUTS: đối tượng/entity, variant/stage/view khi biết, role, must_preserve, reason, essential, applies_to=first_frame/video/both. Khi không cần ghi items=[] và none_reason. Contract và cách dùng theo [quy trình tham chiếu](first-frame-asset-references.md), chỉ đọc phần thao tác chi tiết khi cần asset. Đây là metadata nội bộ, không thêm mục vào bốn phần người dùng nhận. Helper đọc legacy thiếu trường như unverified; revision phải khai lại nhu cầu còn hiệu lực, caption giữ nguyên không query ảnh.

/na-chayvideo viết từ brief và Knowledge trước, metadata catalog hỗ trợ xác định ref; mở ảnh khi cần chi tiết thị giác, không giả đã xem từ descriptor. /na-taoanh tự đối chiếu t=0 và chọn bộ ảnh thực gửi. Asset sau t=0 thuộc nhu cầu video, không ép vào ảnh mở đầu. Giữ ý định/cỡ có căn cứ dù thư viện thiếu; không tự đổi loài/Project để tận dụng ảnh. Prompt không coi đường dẫn local là ảnh model đã nhận. Chất lượng motion/audio vẫn kiểm trên video thật.

## Caption có lựa chọn — schema1

Dùng giọng/khán giả và hashtag của đúng Project. Underwater mặc định ba bản standard/humor/curiosity theo audience-and-caption, mỗi bản caption EN → caption_vi → hook_text EN 1–9 từ → hook_vi. Không áp ngôn ngữ/tag Underwater sang Project khác. Mỗi chuỗi một đoạn; không gộp cả ba lựa chọn vào caption hoặc tạo field hashtags. Giữ bốn mục trả lời, ba bản nằm trong CAPTION; không tự vẽ hook lên ảnh/video.

Dùng [template](templates/caption-variants.json). Caption gốc là chuỗi EN của caption_variant (mặc định standard, không phải user approval); caption_variants có schema=1 và variants keyed theo style. Mặc định giao đủ ba, ngoại lệ user chỉ yêu cầu một bản thì lưu tập được giao. Chọn một bản có sẵn phải ghi caption, caption_variant và item tương ứng bằng đúng nội dung đã resolve. Không sửa caption/translation/hook rời để làm mất liên kết.

Check/save kiểm từng bản, hook 1–9 từ và trường chọn. Save caption-only hoặc revision chỉ caption có thể nhận patch một style + selected caption, merge với bundle gốc theo base_attempt/base_sha256; kiểm lại bundle đã merge, ghi snapshot mới và caption-variants.md đúng thứ tự trình bày. Không truyền lại toàn bộ prompts/frame/assets để sửa caption. Caption-only giữ nguyên binding ảnh/video; không cấp ID hay query asset. Đổi chuyện/prompt thì bundle cũ thành unverified trừ khi khai bundle mới sau rà soát. Ghi caption đơn lẻ không bundle sẽ bỏ chứng nhận bundle cũ, không giả ba bản còn khớp. Legacy chỉ có caption vẫn đọc và giữ unverified phần variants; không backfill lịch sử. Không đặt tiêu chí native là pass tự động từ helper.

Nếu người dùng đã chọn một bản và chỉ sửa bản khác, giữ caption_variant/caption đang dùng, truyền bundle đầy đủ đã ghép để helper kiểm đồng bộ; không tự chuyển bản chọn sang bản đang sửa. Việc dùng standard mặc định chỉ là tương thích dữ liệu, không thay quyết định của người dùng.

## Bối cảnh có địa điểm thực — v1.5

Khi Project/yêu cầu dùng địa điểm thực, theo [location-context.md](location-context.md). Khóa một setting trong INPUTS, đưa đặc điểm thị giác vào frame_state.environment hiện có và hai prompt; caption dùng cùng vùng. Chỉ mở descriptor đúng loài và hồ sơ vùng chọn, ghi nguồn động path/version/hash riêng ngoài packet. Revision đổi vùng/mùa/sinh cảnh phải kiểm lại ảnh/prompt/caption/ref; caption-only giữ setting, không tự sửa môi trường hoặc tra toàn thư viện.
