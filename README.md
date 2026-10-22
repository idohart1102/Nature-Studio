# Nature Studio v2.2.0

Workspace sản xuất nội dung thiên nhiên bằng AI, tổ chức theo **Project**. Tài liệu và lịch sử được lưu bằng file để tiếp tục công việc qua nhiều phiên làm việc.

Đọc [START-HERE.md](START-HERE.md) và [SYSTEM.md](SYSTEM.md) trước khi bắt đầu. AI đọc [AGENTS.md](AGENTS.md) để nhận quy tắc workspace.

## Mới trong v2.2.0

Hook 3 giây đầu (UF-D025): chuẩn chung cho mở đầu và mục riêng Underwater; 5–10 beat, beat đầu ≤3.0s, `checks.hook_signal` ≤3.0s, key vẫn sau 5.0s. Xem [07-Releases/v2.2.0.md](07-Releases/v2.2.0.md).

## Kế thừa v2.1.6

Giảm lượt gọi tool và chi phí phiên dài mà không hạ gate: `preflight`, ledger đọc theo phiên, chia trang nguồn lớn, hash lấy từ output đã xem, lệnh `handoff` cho ảnh, ghi feedback mỗi lượt sửa và tách phiên theo pha. Script chạy đúng trên console Windows; CI thêm Windows. Xem [ghi chú v2.1.6](07-Releases/v2.1.6.md).

## Kế thừa v2.1.5

15 hồ sơ vùng Mỹ cho Redfish/Muskie/Walleye; chọn theo phân bố + sinh cảnh, đọc đúng vùng đã chọn. Một setting xuyên ảnh/video/caption; mỗi caption có một hashtag địa điểm trong tổng 3–5. Không thêm database/schema hoặc ảnh môi trường chưa QA. Xem [ghi chú v2.1.5](07-Releases/v2.1.5.md).

## Kế thừa v2.1.4

/chayvideo trả ba caption Chuẩn/Hài hước/Tò mò cho Underwater; mỗi bản theo thứ tự caption Anh Mỹ + hashtag → lược dịch Việt → hook Anh 1–9 từ → lược dịch Việt. Viết Anh trước, dịch ý sau; giữ giọng người câu cá Mỹ và quy tắc hashtag. Helper lưu/kiểm từng bản, tương thích caption cũ. Xem [v2.1.4](07-Releases/v2.1.4.md).

## Kế thừa v2.1.3

/taoanh mặc định màu chân thực, hạn chế ám vàng/cam mạnh toàn cảnh; giữ màu vàng/vàng đồng thật của đối tượng. Prompt và QA cùng áp dụng, không khử vàng bằng ám màu khác. Xem [v2.1.3](07-Releases/v2.1.3.md).

## Kế thừa v2.1.2

Repo và ZIP có sẵn **64 ảnh tham chiếu** (~106 MB) trong [08-Assets](08-Assets/README.md), dùng được trên máy khác. AI nhập catalog khi cần bằng `python scripts/asset_catalog.py import-bundle 08-Assets/reference-library.json`; chạy lại giữ dữ liệu local, không tiêu lượt model. Chỉ đọc ảnh đúng nhu cầu. Xem [v2.1.2](07-Releases/v2.1.2.md).

## Kế thừa v2.1.1

/chayvideo xác định nhu cầu tham chiếu; /taoanh đánh giá/chọn/gửi asset đúng Project, ghi input thực và QA. Catalog lọc view/phạm vi; metadata trước, ảnh sau, không nạp toàn thư viện. Handoff schema3, legacy được giữ. Xem [ghi chú v2.1.1](07-Releases/v2.1.1.md) và [quy trình tham chiếu](00-Standards/first-frame-asset-references.md).

## Kế thừa v2.1.0

Hồ sơ loài thực dụng gồm ngoại hình, cỡ/biến thể, hành vi và điểm thật đáng xem; dùng chung cho cá và nhóm khác. Catalog asset local lọc đúng entity/stage/role/component, không nạp toàn thư viện. Kiểm–lưu giữ metadata, ngoại lệ beat có binding, CURRENT-STATE schema2 gắn QA đúng render/coverage. Một /chayvideo và các gate chất lượng tiếp tục được giữ. Mã **XX-YYYY** không đổi. Xem [v2.1.0](07-Releases/v2.1.0.md), [profile và asset](00-Standards/knowledge-routing.md), [phân luồng](00-Standards/context-routing.md).

## Bản vá v1.7.1 được giữ

Bản vá dependency kiểm skill: thêm requirements-dev.txt và hướng dẫn xử lý thiếu PyYAML. Xem [ghi chú v1.7.1](07-Releases/v1.7.1.md). Camera Underwater cầm tay tự nhiên; kiểm capability, metadata/âm thực, tỷ lệ first frame và trạng thái text/render/QA/approval. Xem [ghi chú v1.7](07-Releases/v1.7.md) và [hướng dẫn nâng cấp](UPDATE.md#nâng-từ-v16-lên-v17).

## Python trên máy mới và PyYAML

Helper lõi dùng Python 3.11+ và thư viện chuẩn; clone/tải ZIP không tự cài package Python. Đọc skill Markdown hoặc chạy memory/publication validator không cần PyYAML. FFmpeg/FFprobe/WhisperX là công cụ media riêng, không phải dependency PyYAML.

Nếu host chạy `quick_validate.py` của skill-creator để kiểm skill, script **bên ngoài repo** đó import `yaml` từ package [PyYAML](https://pypi.org/project/PyYAML/6.0.3/). Bản vá khai báo trong [requirements-dev.txt](requirements-dev.txt); đây là dependency kiểm skill tùy chọn. Không có script quick_validate trên host thì ghi phép kiểm đó unavailable, không bắt cài cả skill-creator hoặc chặn các helper lõi.

Tại thư mục gốc repo (tên thư mục có thể khác Nature-Studio), dùng chính Python sẽ chạy validator:

```text
python -m pip install -r requirements-dev.txt
python -c "import sys, yaml; print(sys.executable); print(yaml.__version__)"
```

Nếu đã tải tag v1.7 cũ chưa có requirements-dev.txt, cài trực tiếp `python -m pip install PyYAML==6.0.3` hoặc nhận v1.7.1 theo UPDATE.md. Không cài bằng một `pip` khác interpreter. Nếu validator chạy qua Python riêng của host, dùng đường dẫn Python đó thay `python` ở cả hai lệnh. Chạy validator với `-X utf8` để đọc skill tiếng Việt trên Windows.

Có thể giữ dependency trong môi trường riêng: `python -m venv .venv`, sau đó Windows dùng `.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`, macOS/Linux dùng `.venv/bin/python -m pip install -r requirements-dev.txt`; dùng cùng executable khi gọi validator. Không cần activate hoặc thay Python toàn máy. Không commit/đóng gói `.venv`.

## Dành cho AI nhận link GitHub

Đọc [VERSION](VERSION) và [CHANGELOG.md](CHANGELOG.md) để biết phiên bản toàn hệ thống, sau đó theo START-HERE/SYSTEM. Khi kiểm tra hoặc cập nhật từ GitHub, thực hiện [UPDATE.md](UPDATE.md): xác định commit đích, so với bản local và giữ chỉnh sửa riêng trước khi ghi. Chỉ có link repo chưa đủ để biết máy người dùng đã thay đổi gì; cần quyền đọc local hoặc gói workspace/manifest của họ.

Phiên bản hiện hành là **Nature Studio v2.2.0**. Skill/project có số phiên bản riêng. VERSION không tự tạo Git tag/GitHub Release; main có thể chứa thay đổi sau một release, nên luôn ghi kèm commit và trạng thái local. Repository nguồn: [bandepdao123/Nature-Studio](https://github.com/bandepdao123/Nature-Studio).

## Dự án hiện tại

[Underwater](03-Projects/underwater/PROJECT.md): Reel camera dưới nước hướng người câu cá Mỹ. Video mục tiêu 10s, 9:16, một shot; quy chuẩn cụ thể nằm trong hồ sơ dự án. Tên cũ Under Fish US / Under Fishing US chỉ là alias; ID nội bộ và prefix UF được giữ để truy vết.

Repo hệ thống không chứa lịch sử video người dùng. Production và ledger được tạo/giữ ở local; dữ liệu đã có trên máy không bị xóa khi nâng cấp. Bài học cải thiện được chia sẻ riêng sau khi làm sạch theo publication.md.

## Hướng dẫn sáng tạo cho AI

Khi được giao tạo mới, đọc [nguyên tắc sáng tạo chung](00-Standards/creativity.md), rồi hướng dẫn riêng của dự án; Underwater dùng [Sáng tạo mở](03-Projects/underwater/creative-direction.md). Luồng làm việc: **brief/dữ kiện → rà lịch sử → tiền đề độc lập → kiểm tính đúng → chọn chuyện → bố trí nhịp → kiểm độ mới → prompt/caption**.

Ví dụ không phải danh sách tình huống đóng. Độ mới được kiểm ở hành vi và nhân quả, không chỉ đổi cá/mồi/địa điểm. Revision giữ câu chuyện đã chốt. Đây là phần bắt buộc khi AI phát triển ý tưởng, kể cả khi chỉ nhận link repo và không gọi skill. Hướng dẫn không bảo đảm mọi kết quả sẽ hay hoặc chưa từng có.

## Gọi skill /chayvideo

Trong workspace, gửi `/chayvideo` kèm loài hoặc ý tưởng, hoặc yêu cầu tạo nội dung bằng đặc trưng dự án. Ví dụ:

```text
/chayvideo Underwater — Walleye, một bộ, tự phát triển ý tưởng mới
```

Skill [chayvideo](.agents/skills/chayvideo/SKILL.md) tự tìm dự án phù hợp, đọc quy chuẩn và rà lịch sử trước khi viết. Đầu ra gồm Ý TƯỞNG tiếng Việt; FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, mỗi prompt một đoạn; CAPTION tiếng Anh Mỹ tự nhiên kèm hashtag. Lệnh chỉ tạo văn bản và hồ sơ local; không tự render hoặc đăng bài. `/chayvideo` là quy ước trong tin nhắn, không cam kết mọi giao diện có menu slash riêng.

## Chuyển thể video mẫu — /clonevideo

Gửi `/clonevideo` kèm file/link video và thay đổi mong muốn. [Skill clonevideo](.agents/skills/clonevideo/SKILL.md) xem xét hình/âm/timecode, ánh xạ vai trò và chức năng câu chuyện sang loài/nhân vật/bối cảnh đích rồi xuất bốn mục như chayvideo. Quy chuẩn được chọn theo Project; cần truy cập video thực để phân tích, thiếu coverage phải ghi rõ. Skill chỉ tạo nội dung và hồ sơ local, không tự render hoặc đăng.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| 00-Standards | Phương pháp và mẫu hồ sơ |
| 01-Knowledge | Kiến thức, nguồn và phạm vi kiểm chứng |
| 02-Models | Hướng dẫn model và giới hạn đã biết |
| 03-Projects | Hồ sơ, quy chuẩn và lịch sử ý tưởng từng dự án |
| 04-Productions | Chỉ hướng dẫn trong repo; hồ sơ video/media thật ở local |
| 05-Memory | Bộ nhớ riêng Project và shared, mỗi nơi có candidate / active / retired |
| 06-Evaluation | Tiêu chí, ca kiểm và kết quả thực |
| 07-Releases | Baseline, manifest và snapshot lịch sử |

Danh mục [dự án](03-Projects/INDEX.md) và [mẫu dự án](00-Standards/templates/project.md) hỗ trợ mở thêm dự án. Không áp quy chuẩn Underwater mặc định cho dự án khác.

## Di chuyển và đóng gói

Clone/tải toàn bộ repo vào một thư mục, mở thư mục đó làm workspace rồi đọc START-HERE.md. Không cần giữ đường dẫn ổ E:. Đường dẫn tuyệt đối trong một số hồ sơ cũ là provenance tại thời điểm tạo; các nguồn hiện hành dùng liên kết tương đối. Snapshot giữ tên Channel/đường dẫn cũ để truy lịch sử; không dùng làm cấu trúc hiện hành.

Tạo ZIP hệ thống, gồm `.agents` và nguồn được phép chia sẻ; production, ledger, registry và bài học private được loại:

```text
python scripts/package_workspace.py
```

Gói nằm trong `07-Releases/packages/`, kèm manifest SHA256 từng file, phiên bản workspace, commit nguồn và trạng thái thay đổi local. Gói không chứa `.git`, file bí mật, cache hoặc chính các gói ZIP cũ. ZIP và manifest gói được bỏ qua khi commit để tránh lưu lặp nội dung. Khi dùng ZIP, giữ PACKAGE-MANIFEST.json làm baseline để lần cập nhật sau đối chiếu; tên file gói có phiên bản nhưng không thay việc kiểm hash.

Repo không chứa API key hoặc cấu hình đăng nhập. Nguồn bên ngoài và quyền sử dụng được ghi trong hồ sơ khi biết; việc đóng gói không cấp lại quyền cho tài liệu hoặc tài sản tham chiếu. Không có lịch sao lưu, render hoặc đăng bài tự động được cài trong bản này.

## Tên repository cố định, phiên bản nằm trong nội dung

Repository là [idohart1102/Nature-Studio](https://github.com/idohart1102/Nature-Studio) (private, từ 2026-10-22; trước đó bandepdao123/Nature-Studio); không đổi tên khi nâng phiên bản. Tên hiển thị trong README, VERSION, CHANGELOG và gói ZIP thể hiện bản đang dùng, ví dụ Nature Studio v1.1. Khi chốt bản mới, cập nhật các nội dung đó; có thể tạo tag/release v1.1 khi được yêu cầu, giữ nguyên URL repo. [REPOSITORY.json](REPOSITORY.json) ghi danh tính nguồn ổn định.

## /dongvideo và bộ nhớ hai cấp — mới trong v1.1

Gửi `/dongvideo UF-0001` để [tổng kết phiên](.agents/skills/dongvideo/SKILL.md). Skill rà attempt/phản hồi thực, xét bài học riêng Project **và** đóng góp phương pháp/kinh nghiệm cho bộ nhớ chung. Không ép mỗi phiên có lesson; chạy lại không nhân đôi dữ liệu. Báo cáo bằng tiếng Việt, không tự render, duyệt video hay push.

[Memory](05-Memory/INDEX.md) tách `projects/<slug>/` và `shared/`. /chayvideo đọc active phù hợp ở cả hai nơi, ghi lesson ID/version vào INPUTS. /dongvideo tự lưu candidate; chỉ tự active phương pháp kiểm khách quan khi đạt đủ [gate](00-Standards/memory-policy.md). Kiểm cấu trúc bằng `python scripts/validate_memory.py` không chứng minh bài học đúng hay video tốt hơn.

Nâng cấp từ v1.0 theo [UPDATE.md — migration](UPDATE.md#nâng-từ-v10-lên-v11). Giữ dữ liệu riêng, phân loại lesson theo phạm vi, không chép đè cả thư mục và không đẩy production đang làm lên public chỉ vì nâng framework. GitHub main mang phiên bản workspace, không tự có GitHub Release/tag.

## Mã video — Nature Studio v1.2

Video mới dùng **XX-YYYY**, hai chữ A–Z riêng từng Project local, bốn chữ số từ **0001**. [Quy tắc và công cụ](00-Standards/video-identifiers.md): init tạo prefix, reserve cấp mã an toàn và UUID. Không cấp mã từ câu hỏi hoặc revision. Registry `.nature-studio/` không lên Git, phải được giữ khi backup/di chuyển/cập nhật; không nằm trong gói mẫu. UF-0001, mã ba chữ/năm số và các attempt lịch sử giữ nguyên. Prefix UF dành riêng cho legacy; namespace mới được chuyển khi init/reserve thật, giữ UUID Project. Xem UPDATE.md khi nâng từ v1.1.

Gói ZIP phân phối loại `.nature-studio/` để không phát tán prefix local. Muốn di chuyển workspace cá nhân đang làm, sao lưu registry riêng khi không có tác vụ cấp mã; ZIP phân phối không thay bản sao lưu danh tính Project.

## Caption Underwater — v1.3

Phong cách theo benchmark Underfishing: ít chữ, trực tiếp, một điểm đáng xem; linh hoạt câu hỏi/nhận xét/phản ứng/chỉ dẫn, tiếng Anh Mỹ tự nhiên. Giữ 3–5 hashtag khác đúng cảnh, **không dùng #Underwater**. Đọc [quy chuẩn](03-Projects/underwater/audience-and-caption.md) và [nghiên cứu 40 caption](01-Knowledge/benchmarks/underfishing-captions-2026-10-16/REPORT.md). Đây là lựa chọn biên tập, chưa chứng minh hiệu quả nền tảng. Ảnh UI nghiên cứu chỉ lưu local, không có trong repo/gói phân phối.

## Xuất bản hệ thống và bộ nhớ — v1.4

Đọc [publication.md](00-Standards/publication.md) trước khi commit/push hoặc cập nhật GitHub bằng API. Production/attempt/media/ledger/registry giữ local; không đưa vào cây repo hoặc gói hệ thống. Bài học cải thiện ở Project/shared vẫn đi cùng cập nhật sau khi làm sạch và đánh dấu public/reviewed; không tự active. Chạy `python scripts/validate_publication.py` trên cây index trước publish; CI kiểm lại. Không xóa dữ liệu local theo các deletion runtime từ upstream. Commit cũ vẫn có thể chứa dữ liệu đã từng công khai; lần cập nhật này không rewrite lịch sử.

## Tạo first frame — /taoanh

Dùng `/taoanh <mã video>`, “tạo ảnh” hoặc “tạo first frame” khi thực sự cần ảnh cho Project. [Skill](.agents/skills/taoanh/SKILL.md) tự QA ảnh thật, sửa có mục tiêu và giữ ý định; tối đa 5 lượt sinh/sửa, xin thêm khi chưa đạt. /chayvideo vẫn chỉ tạo văn bản; /dongvideo tổng kết bài học.

Model ưu tiên là GPT Image 2.5 Sunburst qua built-in image_gen. [Profile thực thi](02-Models/model-profiles/sunburst-imagegen.md) ghi rõ tool hiện không có selector; không bảo đảm/nhận đã dùng Sunburst khi backend chưa xác minh. Không tìm được Sunburst thì dùng model mặc định và tiếp tục không hỏi lại; danh tính model không là tiêu chí QA. Ảnh, QA, bộ đếm và lịch sử giữ local theo publication.md.
