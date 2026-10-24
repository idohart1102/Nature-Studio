# Chuẩn hồ sơ loài — v3

Version: 3.1 | Updated: 2026-10-25 | Scope: mọi nhóm sinh vật, mọi Project | v3.1: lịch mùa bắt buộc, chuẩn ảnh 1080p/720p, manifest ảnh

Hồ sơ loài là tham chiếu sự kiện có nguồn cho sản xuất, không phải chuyên khảo khoa học đầy đủ. Mục tiêu: thêm loài mới theo một quy trình, máy kiểm được, skill chỉ đọc đúng loài đang làm. Mẫu: [hồ sơ](templates/species-profile.md), [sổ nguồn](templates/species-sources.md). Công cụ: `scripts/species_profiles.py`.

## Một thư viện chung, Project cấp quyền

- Mọi loài (cá, thú, chim...) nằm phẳng tại `01-Knowledge/species/<slug>.md`; nhóm ghi ở `group`. Không tạo bản sao hồ sơ theo Project.
- Project chọn loài được dùng qua key `species` trong `03-Projects/<slug>/context-map.json`. Loài có hồ sơ mà Project không map thì không được nạp; loài chưa có hồ sơ thì nghiên cứu đúng loài, không thay bằng loài khác.
- Format, khán giả, giọng caption, hashtag thuộc Project; không ghi vào hồ sơ loài.
- ID `K-SP-...-NNN` và đường dẫn đã cấp không đổi. Đổi tên gọi thì thêm alias, không đổi slug.

## Cấu trúc hồ sơ

Khối ```json đầu file (máy đọc): `id`, `slug`, `scientific_name`, `taxonomy{authority, order, family, checked_with}`, `common_names{en, vi...}`, `group`, `stages`, `look_alikes[{id?, scientific_name, name}]`, `modules{tên: đường dẫn}`, `status`, `version`, `updated`, `review_due`, `sources_file`.

Tám mục cố định: 1 Nhận dạng · 2 Kích cỡ và giai đoạn · 3 Sinh cảnh và phân bố · 4 Hành vi · 5 Tương tác · 6 Điểm đáng xem · 7 Checklist hình ảnh · 8 Chưa biết và giới hạn.

- Mục 2 là bảng `Thông số | Giá trị | Đơn vị | Phạm vi | Loại | Nguồn`; Loại chỉ là `typical`, `large`, `record`, `estimate`. Cỡ dàn cảnh mặc định lấy từ `typical`; `large`/`record` chỉ dùng khi brief chủ đích và ghi phạm vi. Không suy chiều dài từ cân nặng.
- Mục 4 có bảng lịch mùa `Tháng | Vùng | Hành vi | Nguồn` (tháng ghi T1–T12 hoặc khoảng); mỗi dòng có nguồn. Ghi chú mùa từ danh sách nội bộ chỉ là đầu mối, phải kiểm bằng nguồn A/B trước khi vào bảng.
- Mục 7 là 3–12 dòng kiểm nhanh mà /na-taoanh và /na-danhgia dùng khi chấm ảnh/video của loài đó. Checklist không thay quy chuẩn Project.
- Thông tin chỉ cần cho một kiểu nội dung đặt trong module, ví dụ `angling` → `01-Knowledge/equipment/species/<slug>-angling.md`. Module chỉ được nạp khi tác vụ cần (angling: interaction khác `natural`). Module hợp lệ: `angling`, `hunting`, `life-cycle`, `seasonal`, `sign`. Hiện chỉ `angling` được packet tự nạp; module khác cần nối điều kiện nạp trong `chayvideo_context.py` (kèm test) trước khi dựa vào nó.
- Ngân sách mềm 9.000 ký tự mỗi hồ sơ: hồ sơ được đọc nguyên văn mỗi lượt dùng loài, nên chi tiết dài chuyển sang module hoặc sổ nguồn.

## Theo nhóm sinh vật

Tám mục giống nhau cho mọi nhóm; nội dung trong mục đổi theo nhóm.

- **Cá:** chiều dài TL/FL/SL ghi rõ loại; khối lượng tách riêng; stage trứng/ấu trùng/con non/trưởng thành khi cần; module `angling` khi Project có câu.
- **Thú:** bảng cỡ tách theo giới và loại số đo (chiều cao vai, dài thân, dài đuôi, cân nặng); stage theo loài (ví dụ fawn/yearling/adult). Mục 1 ghi dị hình giới tính và thay đổi theo mùa (gạc mọc–nhung–rụng, lông hè/đông); mục 4 ghi mùa động dục/sinh sản, hoạt động ngày/đêm, dáng đi và tốc độ khi có nguồn. Checklist hình ảnh gồm gạc/sừng đúng giới và mùa, số chạc không dùng để suy tuổi, dáng chân/móng, màu lông theo mùa. Dấu vết chi tiết đặt ở module `sign`, chu kỳ mùa dài đặt ở `seasonal`, săn bắn và quy định ở `hunting`.
- **Chim/bò sát/khác:** cùng nguyên tắc: tách giới, mùa, stage; số đo ghi đúng loại (sải cánh, dài mai...).

Vùng bối cảnh dùng cùng cơ chế `01-Knowledge/locations/<slug>/`. Project nội dung về thú tạo context-map riêng, chỉ map loài nó dùng; không kế thừa map Underwater.

## Nguồn

Sổ nguồn `01-Knowledge/sources/species/<slug>.md` có khối JSON. Mỗi nguồn: `id` (S1…), `tier`, `title`, `publisher`, `url`, `published`, `accessed`, `access`, `supports`, `limits`.

| Cấp | Loại | Dùng cho |
|---|---|---|
| A | Bình duyệt; ITIS/WoRMS/Catalog of Fishes; FishBase; USGS NAS; IUCN | Phân loại, cỡ, sinh học |
| B | Cơ quan quản lý (NOAA, USFWS, DNR/fish & wildlife bang) | Nhận dạng, hành vi, phân bố, quy định |
| C | Bảo tàng, đại học, extension | Bổ sung |
| D | Nhà sản xuất | Chỉ dụng cụ |
| E | Báo, người câu, mạng xã hội | Chỉ là đầu mối |

- `access`: `opened` (mở chính trang), `indexed-only` (chỉ thấy trích đoạn tìm kiếm), `not_accessed`. Không ghi ngày truy cập cho nguồn chưa mở.
- Tên khoa học kiểm bằng nguồn cấp A (`taxonomy.checked_with`). Mỗi hồ sơ có ít nhất một nguồn A/B đã truy cập được trích dẫn. Dữ kiện cỡ nên có hai nguồn; một nguồn thì ghi rõ ở mục 8.
- `snapshot <slug>` tải trang nguồn, lưu bản và hash văn bản hiển thị tại `.nature-studio/knowledge-snapshots/` (local, không vào Git). Lần sau `changed` nghĩa là cần đọc lại nguồn đó, không tự kết luận hồ sơ sai.

## Ảnh tham chiếu

- Chỉ ảnh thật (`origin: photo`) làm nhận dạng/anatomy; giấy phép Public domain, CC0, CC BY hoặc CC BY-SA, ghi tác giả.
- **Chất lượng:** `1080p` = file gốc tối thiểu 1920×1080 (cạnh dài ≥1920, cạnh ngắn ≥1080). Khi không có ảnh 1080p cho một stage/góc, chấp nhận `720p` (≥1280×720) chỉ khi đối tượng chiếm phần lớn khung (`subject_coverage: large`). Kích thước đo từ file thật, không phóng to ảnh nhỏ. Ảnh dưới mức này không vào hồ sơ.
- Mục tiêu mỗi loài: ảnh adult nhìn ngang cho `identity`; thêm juvenile, biến thể (ví dụ steelhead) và cận đầu/miệng cho `anatomy` khi có. Mỗi ảnh được người/AI mở xem thật, xác nhận đúng loài và ghi `observed`, `species_basis`.
- Manifest chung `01-Knowledge/sources/species/photo-references.json` (trong Git) ghi URL trang/file, giấy phép, tác giả, sha256, kích thước, tier và review. File ảnh chỉ lưu local: `python scripts/species_profiles.py photos-fetch [slug]` tải lại, kiểm sha256 + kích thước thật rồi đăng ký vào catalog (`private`). Máy khác chạy cùng lệnh để có ảnh.
- Ảnh AI trong `08-Assets` đều dưới 1080p: chỉ hỗ trợ `production`, không thay ảnh thật; tạo lại ở độ phân giải cao là việc tạo media riêng, cần người dùng giao.
- `scale` cần số đo có nguồn, không lấy từ ảnh.

## Vòng đời

`draft` → `researched` (đủ mục, validator pass) → `reviewed` (người dùng hoặc lượt đối chiếu độc lập đã duyệt) → `stale` (quá `review_due` hoặc nguồn `changed` chưa đọc lại). Hồ sơ `draft` vẫn dùng được nhưng output phải ghi là chưa xác minh trong INPUTS.

## Thêm loài mới

1. `python scripts/species_profiles.py resolve "<tên>"` — đã có thì sửa hồ sơ cũ, không tạo trùng.
2. `python scripts/species_profiles.py new --slug <slug> --id K-SP-<TEN>-001 --scientific "<Genus species>" --name "<Tên>" --group <nhóm>`.
3. Nghiên cứu theo [research.md](research.md), điền sổ nguồn trước rồi hồ sơ; module nếu cần.
4. `python scripts/species_profiles.py validate <slug>` cho tới khi pass; xử lý warning về nguồn chưa trích, thiếu `typical`, quá ngân sách.
5. `python scripts/species_profiles.py snapshot <slug>` và `index`.
6. Thêm key vào context-map của Project được dùng; thêm descriptor vùng và ảnh tham chiếu nếu cần. Không sửa skill.

## Truy xuất và chi phí đọc

`chayvideo_context.py packet` nhận tên bất kỳ trong `common_names`/tên khoa học (ví dụ "red drum") qua `resolve`, nhưng chỉ nạp loài có trong context-map của Project. Mỗi loài được chọn nạp đúng một hồ sơ, cộng module khi tác vụ cần; không nạp chỉ mục, sổ nguồn hay hồ sơ loài khác. `resolve` và `validate` chạy bằng code, không đưa danh sách loài vào context, nên thư viện lớn lên không làm tăng chi phí mỗi lượt. Sổ nguồn chỉ mở khi cập nhật/kiểm dữ kiện.
