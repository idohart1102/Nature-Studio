# Knowledge chung, phạm vi riêng

Version: 1.2 | Updated: 2026-10-25

`01-Knowledge/` là thư viện toàn workspace, không thuộc riêng Underwater. Mỗi hồ sơ vẫn có phạm vi: loài, habitat, tương tác, dụng cụ, nguồn và trạng thái. Nội dung hiện tại tập trung Underwater; hồ sơ cá không tự áp cho deer. Quyết định format, khán giả và cách kể nằm trong Project, không chép vào Knowledge chung.

## Thêm loài hoặc Project

1. Thêm hồ sơ theo [chuẩn hồ sơ loài v3](species-profile-standard.md) bằng `scripts/species_profiles.py new`, có sổ nguồn, validate và index. Một loài một nguồn chính; không thay tên loài trong hồ sơ cũ.
2. Thêm key/đường dẫn trong `03-Projects/<slug>/context-map.json` đúng Project. Thêm mười hồ sơ cá không làm AI đọc cả mười: species map chọn hồ sơ đúng loài; các ràng buộc liên quan vẫn phải đọc.
3. Với Project deer mới: dùng mẫu Project, ID/slug riêng; map chỉ trỏ nguồn deer/habitat/tương tác và chuẩn liên quan, không kế thừa map Underwater. Chưa có dự án rõ thì hỏi/chốt trước khi sản xuất.
4. Xếp nguồn vào stage/effect trong `context-routing.json` nếu cần. Mode source list là mức bao phủ tối thiểu; nguồn chưa xếp stage được đọc rộng để tránh mất gate. Không đưa mọi loài vào danh sách nguồn nền của mọi mode.
5. Kiểm packet/verify/coverage, fallback thiếu loài và tác vụ revision/caption. Nguồn hash đổi thì dựng lại packet/đọc lại phần liên quan. Không sửa skill chỉ để thêm dữ liệu.

Xem [cấu hình và cơ chế đọc](context-routing.md). Giữ nguyên văn nguồn cần thiết, chỉ giảm đọc thừa/đọc lặp; không dùng quota token để bỏ dữ kiện hoặc ràng buộc. Thư viện lớn lên giúp chọn nguồn có lợi hơn so với đọc toàn kho, nhưng không có tỷ lệ tiết kiệm cố định hoặc bằng chứng tự động về chất lượng sáng tạo.

## Hồ sơ phục vụ sáng tạo — v2.1.0

Từ 2026-10-25 thay bằng tám mục của [chuẩn v3](species-profile-standard.md); đoạn này giữ để truy vết. Bản v2.1.0 dùng mẫu sáu phần: nhìn đúng; cỡ/biến thể; hành vi; điểm đáng xem; điều kiện/lỗi cần tránh; nguồn/asset. Giữ ID/đường dẫn đang có. Cỡ và stage là hai thông tin riêng; chỉ bổ sung các giai đoạn đúng loài và nhu cầu, không ép thú có trứng hoặc mọi loài phải săn mồi. Nét đặc biệt phải có căn cứ và đọc được trên hình; gợi ý ý tưởng không là kịch bản cố định hoặc điểm dự đoán viral.

Cá thể lớn và trường hợp đặc biệt được khai thác theo đúng scope nguồn. Không biến số liệu một trường hợp thành phổ biến; không ghép các cực trị độc lập hoặc đổi khối lượng thành chiều dài bằng đoán. Thiếu nguồn thì nghiên cứu, không tự gọi bất khả thi hoặc tự thu nhỏ để dễ sinh. Cảnh có thể hấp dẫn bằng hành vi/tương tác/biến thể khác. Một profile không phải hồ sơ khoa học đầy đủ; giữ thông tin có tác dụng với output và giới hạn thực.

## Catalog asset local

`scripts/asset_catalog.py` là helper stdlib; metadata nguồn duy nhất ở `.nature-studio/assets/catalog.sqlite3`, không vào Git/gói hệ thống. File gốc/derived có thể nằm trong workspace, không phải chép vào từng Project. [Mẫu nhập](templates/asset-record.json) không phải asset đã QA. Catalog rỗng hoặc thiếu ảnh không tự chặn tác vụ viết; không được biến phần chưa kiểm thành ảnh đạt.

Các role khuyến nghị: `identity`, `anatomy`, `scale`, `assembly`, `production`. Có thể thêm role phù hợp công việc; role `scale`/`biological-evidence` không được chứng minh bằng ảnh generated. Identity/anatomy không tự chứng minh kích cỡ. `review.roles` chỉ rõ phần đã kiểm; pass phải có evidence file/hash. Metadata/helper không tự hiểu sinh học hoặc xem ảnh. Scope review, source và rights phải được đối chiếu thật.

```text
python scripts/asset_catalog.py query .nature-studio/context/ref-request.json
python scripts/asset_catalog.py register .nature-studio/context/asset-record.json
python scripts/asset_catalog.py select .nature-studio/context/ref-request.json --asset REF-ID --out .nature-studio/context/ref-selection.json
python scripts/asset_catalog.py verify .nature-studio/context/ref-selection.json
```

Request tối thiểu: `{"requests":[{"entity_id":"K-SP-REDFISH-001","stage":"adult","role":"identity"}]}`. Chỉ đưa stage thật đã chọn. Query trả descriptor phân trang, kiểm `missing` và `next_cursor`; không in/đọc toàn catalog. Không chọn ảnh loài/giai đoạn khác để hết missing. Có thể query bỏ stage để tìm lead còn unknown, nhưng chưa xác nhận stage không được chứng nhận selection đúng. Không đặt trần số ảnh làm mất role/dependency cần thiết.

Register ghi metadata và binding, không tải/sinh/chấm ảnh. File local và review pass cần path/sha256 đo thật. Chỉ có URL được đăng ký như lead; chưa là input local đã verify. Cập nhật asset cần `--expected-sha` hiện hành; không ghi đè thầm. Chọn rõ IDs; helper mở rộng `requires` để giữ component và từ chối vòng. Asset metadata thay đổi làm receipt stale; file/evidence hash sai làm needs_review. Thêm mục không liên quan không bắt đọc lại mọi profile. Không thêm hash toàn catalog vào source floor.

Selection là planned references; scope/hash không chứng minh model đã dùng nó. Lưu receipt local mới, không ghi đè. `select/verify`: matched=0, needs_review/stale=2, lỗi dữ liệu=1; đọc status/issues, không chỉ exit code. Query chỉ trả metadata, không là visual QA. Sau chọn phải mở đúng ảnh thật để kiểm. Không tự nhận exact SKU/kích cỡ từ ảnh sinh.

Ảnh thư viện độc lập dùng tuyến tạo ảnh thông thường khi thực sự được giao; không tạo video ID giả hoặc dùng production quota ngoài production. First frame của video thật giữ quota/flow /na-taoanh, không đổi nhãn library để reset. Catalog/binary/private evidence được backup riêng. Chỉ xuất metadata/ảnh public được rà khi có nhiệm vụ publish; không đổi visibility/status do import.

Asset crop/annotate dùng `derivation: {"parent_id":"REF-...","parent_record_sha256":"...","operation":"crop ..."}`; helper kiểm parent và tự thêm dependency. Parent đổi thì selection cần review lại lineage. Mỗi bản dẫn xuất vẫn cần QA đúng role của chính nó; parent pass không tự làm bản dẫn xuất pass. Không có dẫn xuất thì để null/bỏ trường.

## Scope và truy xuất asset — v2.1.1

`applicability={scope: shared|projects|unknown, project_ids: []}` dùng ID ổn định Project; projects cần danh sách ID, shared/unknown để rỗng. Thiếu trường ở record cũ là unknown, không tự shared. Publication/rights độc lập với phạm vi dùng nội bộ. Giữ một catalog; không sao chép ảnh theo Project. Thêm dữ liệu chỉ cập nhật metadata/map, không sửa skill hoặc làm dài danh sách nguồn nền.

Request hỗ trợ view ngoài entity_id/role/stage/variant. Lệnh query/select/verify/read/inputs-check dùng `--project-id <ID>`; luôn truyền khi chứng nhận dùng cho Project. Query loại scope projects khác, hiện unknown với scope_issue và vẫn báo missing nếu chưa có mục đủ scope. Query không truyền Project chỉ phục vụ discovery legacy, không chứng nhận Project. `read <request.json> --asset <ID>` mở metadata đầy đủ đúng ID. `select ... --project-id <ID>` tạo receipt schema2; schema1 legacy vẫn đọc, verify với Project sẽ yêu cầu chọn lại. Kiểm scope trên cả dependency. Chi tiết chọn/gửi/QA theo [quy trình dùng ref](first-frame-asset-references.md).

Không tăng schema database chỉ vì metadata mới. CAS/revision/derivation như cũ: parent đổi thì child cần cập nhật lineage đã kiểm; không sửa receipt/handoff lịch sử. Selection cũ không tự stale vì thêm asset khác; cursor query matching đổi có thể phải dựng lại. Tập nguồn phải verify khác tập ảnh thực gửi. Không thêm hash toàn catalog vào packet. Nhãn dimensions của ảnh AI không thay size có nguồn.

## Asset đi cùng repo — v2.1.2

Khi lần đầu tra mà catalog chưa có hoặc thiếu bộ tham chiếu đi kèm, chạy `python scripts/asset_catalog.py import-bundle 08-Assets/reference-library.json` nếu manifest tồn tại, rồi query lại. Helper đọc manifest/hash bằng code, không nạp toàn bộ vào context. Import idempotent: giữ nguyên ID local có cùng nội dung/role/scope; xung đột phải xử lý, không ghi đè hoặc tự đổi ID. Ảnh bind trực tiếp vào `08-Assets/images/`, không sao chép sang runtime. Clone sạch có đầy đủ 64 ảnh công khai; production/catalog/quota/registry riêng vẫn local. Asset mới chỉ thêm vào bundle sau khi đã được phép xuất bản và review làm sạch; xem [hướng dẫn](../08-Assets/README.md).

## Vùng bối cảnh — v2.1.5

Theo [chuẩn địa điểm](location-context.md): profile loài → descriptor vùng của loài → hồ sơ vùng được chọn. Knowledge lưu sự kiện có nguồn; Project giữ hashtag/khán giả. Thêm vùng bằng hồ sơ có ID/path/version/source và một dòng descriptor, không sửa skill hoặc nạp mọi vùng vào context-map. Chỉ mục loài hiện có tại `01-Knowledge/locations/<species>/INDEX.md`; mỗi loài khởi đầu năm vùng, không giới hạn tối đa. Hồ sơ vùng nằm ngoài packet nền: ghi path/version/hash của bản thực đã đọc trong INPUTS. Không tuyên bố coverage packet đã kiểm nguồn động.

## Hồ sơ loài v3 — 2026-10-25

Hồ sơ mọi nhóm sinh vật theo [species-profile-standard.md](species-profile-standard.md): khối metadata JSON, tám mục, bảng cỡ có Loại/Nguồn, Checklist hình ảnh, sổ nguồn có cấp A–E và trạng thái truy cập. `chayvideo_context.py` resolve alias/tên khoa học qua `species_profiles.py` nhưng chỉ nạp loài có trong context-map của Project; module (ví dụ `angling` → `01-Knowledge/equipment/species/<slug>-angling.md`) chỉ vào packet khi tác vụ cần. Không nạp chỉ mục loài, sổ nguồn hoặc hồ sơ loài khác. CI chạy `species_profiles.py validate`.
