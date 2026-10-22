# Nature Studio — lịch sử phiên bản

Phiên bản toàn workspace được đọc từ [VERSION](VERSION). Phiên bản của từng skill/tài liệu được quản lý riêng; không đổi tất cả thành 1.0. Commit và hash dùng để phân biệt các bản có cùng số phiên bản hoặc có chỉnh sửa local.

## v2.1.6 — 2026-10-22

- Giảm lượt gọi tool, không hạ gate: `chayvideo_context.py preflight` (packet + history trong một lệnh, chỉ in đường dẫn/số lượng/ID), `context-id` + `view --ledger` (một sổ đọc theo chat, thay receipt mỗi lượt), `view --page-large` (chia trang nguồn lớn theo heading, chỉ tính đã đọc khi đủ mọi trang), output JSON gọn.
- Hash không chép tay: `fingerprint --from-history`, `resolve --out` + `save --from-resolve`; lệnh `chayvideo_output.py handoff` tự tính hash, ghi handoff theo attempt, chạy check-frame và chỉ cập nhật FIRST-FRAME.json khi matched. context-map.json và asset_catalog.py luôn là dependency, không còn nguồn in ra hoặc làm đổi digest khi thêm asset selection.
- Gate mới (UF-D024): video prompt new/reference phải có camera handheld; `checks.location_tag` đúng một lần trong mọi caption.
- Vệ sinh phiên: ghi feedback.md mỗi lượt sửa; đề nghị chat mới sau khoảng 5 lượt sửa kèm câu nối. Template feedback thêm phần đã chốt/phương án đã loại.
- Script đặt UTF-8 cho console (Windows cp1252 không còn lỗi); CI chạy cả Windows. Nội dung: camera cầm tay trong underwater-realism, tag địa điểm trong audience-and-caption, bỏ tham chiếu ổ E:, đánh dấu gói standalone v1.9 là lưu trữ, ghi chú nâng cấp v2.1.2→v2.1.5.
- Sau tag v2.1.6: CI Windows lộ lỗi fixture test dùng thư mục tạm tên rút gọn 8.3 (RUNNER~1) trong khi helper resolve tên đầy đủ; test nay resolve gốc tạm. Không đổi code chạy thật; tag v2.1.6 giữ nguyên.
- 2026-10-22: viết lại lịch sử Git, gỡ hồ sơ UF-0001 và idea-ledger cũ khỏi mọi commit; force-push main, codex/release-v2.0.0 và các tag; thêm tag v1.8. Nội dung từng bản không đổi. Bảng mã cũ → mới và cách đồng bộ máy khác ở UPDATE.md.
- 2026-10-22: repository chính chuyển sang `idohart1102/Nature-Studio` (private) với cùng lịch sử, nhánh và tag; REPOSITORY.json ghi repo cũ bandepdao123 trong previous_repositories.
- `scripts/session_usage.py`: đọc bộ đếm token từ log Codex/Claude local (request, tool call, input/cached/output, ngữ cảnh đỉnh, compaction, theo lượt); không đọc nội dung chat.

## v2.1.5 — 2026-10-19

- Thêm 15 hồ sơ vùng Mỹ có nguồn và ba descriptor theo loài; phân bố + sinh cảnh là bắt buộc, độ phổ biến câu cá chỉ ưu tiên phụ. Năm vùng là khởi đầu, không giới hạn tối đa.
- Luồng profile → descriptor → vùng chọn; nguồn động ghi path/version/hash trong INPUTS ngoài coverage packet. Setting dùng INPUTS và frame_state.environment hiện có, không database/schema mới.
- Ảnh/video/caption giữ cùng setting; Underwater mỗi caption đúng một tag địa điểm trong tổng 3–5. Revision/legacy/caption-only giữ phạm vi; kiểm địa lý/tag là QA ngữ nghĩa, không nhận helper đã xác minh.
- Không tạo ảnh môi trường/media trong đợt nâng cấp. Bảo toàn nguồn riêng và lịch sử; xuất bản theo phạm vi người dùng đã duyệt, ghi chú tại 07-Releases/v2.1.5.md.

## v2.1.4 — 2026-10-19

- /chayvideo v2.11: Underwater mặc định ba caption Chuẩn/Hài hước/Tò mò, thứ tự caption Anh Mỹ + hashtag → lược dịch → hook Anh 1–9 từ → lược dịch. Viết Anh trước, tránh văn dịch/slang/đùa gượng; không hứa retention từ kiểm văn bản.
- Helper giữ bundle/selected caption, kiểm từng bản và lưu caption-variants.md; patch caption giữ frame/asset/history và tương thích caption cũ. Không tạo media hoặc tự xuất bản.

## v2.1.3 — 2026-10-18

- /taoanh v1.6 và tiêu chí/template QA chung: mặc định màu chân thực, hạn chế ám vàng/cam mạnh toàn cảnh; giữ màu vàng/vàng đồng thật của đối tượng và ánh sáng ấm do brief chủ đích yêu cầu. Không khử vàng bằng ám màu khác, không sửa ảnh/QA lịch sử hàng loạt.

## v2.1.2 — 2026-10-18

- Bổ sung 64 ảnh asset đã chọn trong 08-Assets, review làm sạch và manifest public/reviewed để dùng trên máy khác; không xuất production, ảnh lỗi hoặc database runtime.
- import-bundle kiểm hash/dependency, nhập catalog trên clone sạch, idempotent và dừng khi xung đột ID; ảnh bind trực tiếp vào repo, không nhân bản vào runtime.
- Skills bootstrap bộ ref đi kèm khi thiếu catalog trước khi kết luận không có ảnh. Publication guard kiểm manifest, file/review hash, quyền xuất đã ghi và không có file asset ngoài danh sách.
- 278 tests đạt; kiểm sạch với 64 ảnh thật nhập và chạy lại thành công, giữ 4 unknown-stage như trước. Chưa sinh media hoặc đo token model thực.

## v2.1.1 — 2026-10-18

- Nhu cầu reference_requirements nội bộ xuyên /chayvideo, /clonevideo và /taoanh; tự đánh giá đúng đối tượng/biến thể/role/view, tách first_frame/video/both. Caption-only giữ binding, không tra asset.
- Catalog thêm applicability shared/projects/unknown, lọc Project/view, đọc metadata theo ID và kiểm phạm vi toàn dependency. Thêm dữ liệu không làm dài skill hoặc bắt nạp toàn catalog.
- Tách tập nguồn kiểm với bộ ảnh thực gửi. Kiểm declared actual inputs/prompt/output theo hash và thứ tự; handoff schema3 liên kết call/attempt/Project/output, legacy giữ provenance unverified riêng.
- Một hướng dẫn conditional dùng chung, Knowledge vẫn xác lập sinh học/kích cỡ; ảnh AI không chứng minh scale. Không ép ý tưởng theo thư viện. Không sinh media trong đợt cập nhật.
- Xem ghi chú v2.1.1 cho kiểm thực tế/giới hạn. Asset binaries/catalog/production/registry vẫn local; không gộp dữ liệu riêng vào bản xuất.

## v2.1.0 — 2026-10-18

- Profile sáu phần phục vụ sáng tạo, giữ ID ba loài; nguồn văn bản/điểm đặc biệt/cỡ có điều kiện, không hứa viral. Asset catalog local stdlib với query phân trang, chọn role/stage/component, dependency, hash, review scope và CAS cập nhật; không render/tải ảnh hoặc tự public.
- Asset selection tùy chọn trong context/OUTPUT, view descriptor gọn; pending review tách source coverage. Giữ whole-source floor, legacy và ref planned khác actual-used.
- Check/save giữ checks/contract version, tách count/timeline; ngoại lệ beat bind request/prompt/scope/base/target attempt, dùng chung new/revision/reference. Không sửa attempt lịch sử.
- CURRENT-STATE schema2 gắn QA reviewed_render/evidence/coverage; null/type thành errors, approval độc lập selected_render. Schema1 đọc được nhưng unverified.
- Giữ ID/registry/quota/Memory/private và release cũ. Nguồn v2.1.0 chốt local; commit/tag/publish là thao tác riêng theo nhiệm vụ.

## v2.0.0 — 2026-10-17

- /chayvideo v2.7: một dispatcher, nguồn theo stage và effect; cấu hình Project độc lập với skill, unknown/unassigned giữ đường đọc đầy đủ. Fullset đủ brief ưu tiên all + view để tránh overhead chia stage không cần thiết.
- Thêm view nguyên văn + receipt local có context epoch, task union cho review hình/âm, coverage tập nguồn nền và fingerprint builder/router/config. Receipt không là bằng chứng hiểu nguồn; sau compaction phải đọc lại.
- Giữ nguồn và gate hiện hành, compatibility packet schema1/2; schema3 chỉ dùng khi chọn stage. Chưa công bố chất lượng model tương đương hoặc tỷ lệ tiết kiệm usage thực; kiểm helper và số đo proxy lưu trong hồ sơ triển khai local. Chốt các tối ưu local vào phiên bản hệ thống v2.0.0.

- Mã video mới XX-YYYY: hai chữ ASCII và bốn số 0001–9999; UF giữ riêng cho legacy. Migration registry theo nhu cầu trong transaction, giữ UUID, mã cũ và bộ đếm cũ; chặn allocator cũ ghi sai định dạng. Không cấp video hoặc migrate registry thật khi nâng mã nguồn.
- Phân biệt Knowledge dùng chung có phạm vi với quy chuẩn Project; hướng dẫn thêm loài/Project độc lập qua map.
- VERSION 2.0.0; mặc định bản vá nhỏ tăng thành 2.0.1, 2.0.2… Có helper kiểm phiên bản/đề xuất số kế tiếp, không tự phát hành sau mỗi clip.

## v1.8 — 2026-10-17

- Thêm engine truy xuất metadata Project/shared, task aliases và nhãn chủ đề/đối tượng/tương tác; phân trang summary, mở nguồn hash-bound, unknown/legacy fallback. Topic xếp hạng, không là quyền áp dụng.
- Packet schema2 không nạp toàn bộ Memory INDEX/active; selection theo ID, freshness bắt thêm/sửa/xóa/chuyển trạng thái bài học. Giữ verify packet legacy.
- Đồng bộ bốn skill, policy/template/validator và publication guard; catalog/query chỉ local, không xuất JSON Memory. Không thay gate activation/format/registry/quota hoặc duyệt video.
- Giữ bản vá dependencies v1.7.1; ca kiểm/đo thực ghi riêng sau triển khai.

## v1.7.1 — 2026-10-17

- Sửa thiếu khai báo/hướng dẫn PyYAML cho bước kiểm skill external trên máy mới; thêm requirements-dev.txt, phân biệt dependency dev và runtime stdlib, cài đúng interpreter.
- CI kiểm dependency dev và parse frontmatter bốn skill riêng với job lõi. Không di chuyển tag v1.7 hoặc sửa release cũ; [ghi chú bản vá](07-Releases/v1.7.1.md).

## v1.7 — 2026-10-17

- Underwater UF-D021: thay mặc định camera cố định bằng camera cầm tay chuyển động nhẹ tự nhiên như người cầm điện thoại quay; đồng bộ format/output-contract/Project/QA, hướng dẫn new và chuẩn reference. Phân biệt chuyển động máy và cá; giữ quy chuẩn còn lại. Không tuyên bố đã kiểm độ tự nhiên của render bằng video liên tục.

- Thêm media_review.py: preflight executable, ffprobe, LUFS/true peak đầu–giữa–cuối và two-pass normalization có quyền riêng; không coi đo tín hiệu là nghe thực.
- Bảo toàn quan hệ camera–chủ thể khi chuyển thể; chấp thuận partial không cho phép đổi cơ chế. QA reveal/ending cho phần ngoài first frame.
- Tỷ lệ ảnh đầu vào cho phép sai số tương đối ≤0.1%; công bố pixel thật, export chính xác kiểm riêng.
- Thêm production_state.py và mẫu CURRENT-STATE: text/render/QA/tạm duyệt/final độc lập. Xuất hai candidate đã làm sạch, không tự active.
- Chi tiết kiểm và giới hạn tại [ghi chú v1.7](07-Releases/v1.7.md).

## v1.6 — 2026-10-17

- `/chayvideo` v2.4: tách nhánh tạo mới/revision/caption, nạp context đúng nhiệm vụ với nguồn/hash và fallback; lịch sử có coverage/fingerprint, hồ sơ loài là tùy chọn theo Project. Helper kiểm đầu ra và lưu attempt bất biến.
- Thêm `/clonevideo` v1.2: chuyển thể video mẫu qua coverage hình/âm, timecode, vai trò và chức năng câu chuyện; ánh xạ theo brief/Project. Dùng chung workflow v1.2, quy chuẩn và helper với chayvideo. Brief được verify cả payload/schema/hash và độ mới của nguồn; helper không thay việc xem/nghe video thật.
- Revision truy nguyên từng trường theo `base_attempt`/`base_sha256`, không tự chọn bản mới nhất. First-frame handoff schema 2 ràng buộc ảnh, review, nguồn attempt, trạng thái t=0 và tiêu chí QA; `/taoanh` v1.1 hỗ trợ đối chiếu. Legacy thiếu bằng chứng giữ unverified; caption-only giữ khả năng tái dùng ảnh khi các đầu vào ảnh không đổi.
- Story Development v1.1 liên kết ý đồ với hình/âm/lời/nhịp; revision sửa đúng phạm vi, phân biệt quan sát/phản hồi/giả thuyết; chuyển thể cho phép giữ/thay/bỏ chức năng và gộp/tách event có căn cứ. Không thêm biểu mẫu bắt buộc cho các kiểm sáng tạo này.
- Hợp nhất hợp đồng Underwater và đường đọc; giữ quy chuẩn 10s, 9:16, một shot, key onset >5s, 5–8 beats, âm thanh/caption. Gate loài và caption riêng Underwater không áp thành luật cho mọi Project; reference được tái dùng mẫu có chủ đích.
- Sau hai audit độc lập: sửa verify brief, kiểm identity trước save, tách gate đúng Project, loại manifest installation local khỏi public tree/ZIP, thêm unit suite vào CI. SYSTEM v1.8/publication v1.1 phân biệt gói hệ thống và backup cá nhân.
- Kiểm gần nhất: 133/133 unit test đạt; bốn skill/memory/publication checks đạt; 480 file được bảo vệ không đổi/mất sau đợt sửa lỗi. Chi tiết và giới hạn tại [báo cáo năm sửa lỗi](06-Evaluation/results/five-repairs-implementation-2026-10-17.md); số liệu các báo cáo trước là mốc lịch sử, không cộng dồn.
- Chốt VERSION 1.6 và đồng bộ tài liệu điểm vào; [ghi chú phát hành](07-Releases/v1.6.md), [bản tổng hợp trước phát hành](07-Releases/v1.6-preparation-2026-10-17.md). Chưa đo token thực, hiệu quả sáng tạo/khán giả hoặc QA media thật trong đợt xây hệ thống.

## v1.5 — 2026-10-16

- Triển khai story-development v1.0 dùng chung và phần áp dụng Underwater UF-D017; bảy nguồn được phân loại, có giới hạn ngoại suy.
- Đồng bộ đường đọc qua creativity/production/START-HERE/PROJECT, mẫu concept và tiêu chí/ca đánh giá. Riêng Story Development không đổi skills/output-contract/format/caption; routing /taoanh được bổ sung riêng bên dưới. Bộ nhớ và production cũ giữ nguyên.
- Đồng bộ VERSION 1.5 cho bản nguồn; chưa chạy audience/model test. Các báo cáo triển khai giữ trạng thái kiểm tại thời điểm ghi; xuất bản không chứng minh hiệu quả nội dung.

### /taoanh

- Thêm skill tạo/sửa first frame qua image_gen; QA ảnh thực và bộ đếm 5 call lưu qua phiên, hết chưa đạt phải xin thêm.
- Ưu tiên Sunburst; không có lựa chọn phù hợp thì dùng model mặc định image_gen, không hỏi lại. QA chỉ kiểm chất lượng ảnh; danh tính model ghi theo công bố thực, không tự dùng API/CLI.
- Thêm gate chung, QA Underwater, template review/handoff và script budget stdlib; không sinh media hoặc publish trong lần xây skill.

## v1.4 — 2026-10-16

- Bỏ production UF-0001/A01–A04 và ledger khỏi cây Git hiện hành; giữ nguyên file local. Không rewrite các commit cũ.
- Cập nhật hệ thống giữ runtime ở local; bài học public đã làm sạch ở Project/shared vẫn được phân phối, không đổi candidate thành active.
- Thêm publication policy, validator cây Git, CI Public tree guard và template ledger; packager bỏ runtime/private lessons, kiểm evidence/index công khai.
- UPDATE.md hướng dẫn nhận deletion upstream mà giữ dữ liệu local. Các công việc local chưa được giao publish không gộp vào lần này.

## v1.3 — 2026-10-16

- Underwater UF-D015: chốt phong cách caption học từ Underfishing, ít chữ/trực tiếp/đa dạng kiểu câu, độ dài linh hoạt; giữ tiếng Anh Mỹ và 3–5 hashtag. Quyết định biên tập không là kết luận performance. Phát hành cùng UF-D016: không dùng #Underwater, giữ 3–5 hashtag khác đúng cảnh.
- Thêm benchmark 40 caption và một candidate riêng Underwater, chưa kiểm hiệu quả. Chỉ đưa dữ liệu nghiên cứu văn bản lên repo; ảnh giao diện, registry và production đang làm giữ local.
- Cập nhật đường đọc skill/quy chuẩn, hướng dẫn nâng từ v1.2 và kiểm đóng gói bỏ ảnh UI nghiên cứu.

## v1.2 — 2026-10-16

- Chuẩn mã video mới XXX-yyyyy, prefix ba chữ sinh riêng Project trên local, số từ 00001; revision giữ mã và tăng attempt.
- Thêm script SQLite stdlib init/reserve, UUID nội bộ và IDENTITY.json; kiểm trùng, không tái sử dụng số, dừng khi hết 99999.
- Registry .nature-studio/ không vào Git/gói mẫu; hướng dẫn backup và tiếp tục Project trên máy khác. Mã legacy UF-0001 giữ nguyên.
- Cập nhật hai skill, mẫu Project, quy trình sản xuất và UPDATE.md. Không thay format hoặc đẩy production đang làm lên repo.

## v1.1 — 2026-10-16

- Thêm skill /dongvideo: tổng kết production thực, luôn xét bài học Project và đóng góp shared; ghi SESSION-REVIEW, tránh trùng khi gọi lại.
- Bộ nhớ tách projects/<slug>/ và shared/; chỉ áp active đúng điều kiện, một bản gốc/ID ổn định. Bản nguồn trước chuyển có 0 lesson, không tự tạo lesson từ lịch sử chat.
- /chayvideo v1.5 đọc hai cấp, ghi ID/version/cách dùng vào INPUTS; giữ hợp đồng đầu ra và sáng tạo mở.
- Policy v2.0 cho /dongvideo quyền tự active procedural lesson khi có phép kiểm khách quan, hồi quy/ngoại lệ, bằng chứng và không đổi chính sách. Kết luận sáng tạo/hiệu quả model/khán giả chưa kiểm giữ candidate.
- Thêm metadata lesson, mẫu tổng kết, validator stdlib và fixture tests. Validator không thay QA nội dung hoặc chứng minh cải thiện media.
- UPDATE.md có mapping v1.0 → v1.1, bảo toàn dữ liệu riêng, hướng dẫn Git/ZIP và rollback. Tên/URL repo giữ nguyên.
- Phạm vi phát hành là framework. Những thay đổi production có sẵn ở local được bảo toàn và không tự đẩy vào commit nâng cấp.

Giới hạn: chưa chạy /dongvideo trên production thật, chưa kiểm hành vi skill bằng một lượt AI độc lập, chưa chứng minh hiệu quả render/retention hoặc chất lượng sáng tạo cải thiện. Kết quả kiểm thực được ghi tại 06-Evaluation/results/v1.1-implementation-2026-10-16.md.

## v1.0 — 2026-10-16

Bản đầu tiên được đặt phiên bản toàn hệ thống theo yêu cầu người dùng. Các thay đổi trước ngày này được gom vào nền v1.0, không suy ra rằng workspace từng phát hành v1.1/v1.2 từ số phiên bản module.

- Tổ chức theo Project, với dự án Underwater; giữ ID/prefix và lịch sử tên cũ.
- Có Standards, Knowledge, Models, Productions, Memory, Evaluation và Releases.
- Skill chayvideo v1.3 nhận diện dự án theo đặc trưng, rà lịch sử và kiểm độ mới ở nhân quả; ý tưởng tiếng Việt, hai prompt tiếng Anh một đoạn và caption tiếng Anh Mỹ.
- Hướng dẫn sáng tạo mở tránh dùng ví dụ làm danh sách tình huống đóng; revision giữ ý định đã chọn.
- Bổ sung UPDATE.md để AI đọc repo, xác định phiên bản đích và đối chiếu thay đổi với workspace local trước khi cập nhật.
- Script đóng gói ghi VERSION, nguồn repository, commit và trạng thái local vào PACKAGE-MANIFEST.json, cùng hash từng file.
- Giữ hồ sơ UF-0001 và các attempt hiện có đến A04. Chốt v1.0 không có nghĩa các attempt đã đạt QA hoặc được duyệt.

Giới hạn: chưa chạy đánh giá hành vi EV-UF-006/007; chưa chứng minh độ mới/chất lượng media hoặc hiệu quả nền tảng. Không cài tự động pull, render, publish hoặc sao lưu theo lịch. Việc có VERSION không tự tạo Git tag hay GitHub Release.

### Bổ sung vào v1.0 — 2026-10-16

- Đưa cấu trúc hướng dẫn sáng tạo chung vào 00-Standards/creativity.md, dẫn từ README, START-HERE, AGENTS và skill chayvideo v1.4.
- Giữ hướng dẫn cụ thể của Underwater trong creative-direction.md; không nhân bản thành một danh mục tình huống đóng. Giữ nguyên quy tắc revision và hợp đồng đầu ra.
- VERSION tiếp tục là 1.0 theo yêu cầu người dùng; commit và manifest bổ sung phân biệt nội dung với bản v1.0 trước đó. Giữ nguyên manifest/gói cũ, không coi các bản cùng VERSION là byte-identical.

## Quy tắc ghi lần cập nhật tiếp theo

Trong quá trình phát triển, ghi mục `Chưa phát hành` ở đầu lịch sử. Khi chốt bản mới, cập nhật VERSION và mục tương ứng, nêu thay đổi/di chuyển dữ liệu, điều người dùng cần làm và giới hạn đã kiểm. Không sửa mô tả bản đã đóng để che lịch sử. Chỉnh dữ liệu sản xuất có thể chỉ cần commit mới, không tự tăng phiên bản toàn hệ thống sau mỗi clip.

### Quyết định giữ URL repository — 2026-10-16

- Giữ tên repo Nature-Studio, đưa tên thử Nature-Studio-v1.0 trở lại tên ổn định; vẫn là cùng repository ID 1421542100 và giữ toàn bộ lịch sử.
- Phiên bản chỉ ghi trong README/VERSION/CHANGELOG/manifest/gói và tag/release khi được tạo. Không đổi tên repo theo mỗi phiên bản. Quyết định này thay chính sách đổi tên thử trước đó; VERSION hiện vẫn 1.0.
