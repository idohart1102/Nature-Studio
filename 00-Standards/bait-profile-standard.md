# Chuẩn hồ sơ mồi câu

Version: 1.0 | Updated: 2026-10-25 | Phạm vi: mọi Project có cảnh câu | Công cụ: `scripts/bait_profiles.py`

Mục tiêu: khi cảnh có mồi, tra được đúng một mã mồi và đúng ảnh tham chiếu bằng metadata, không đọc cả thư viện. Hồ sơ mồi là nguồn sự kiện về hình dạng, cấu tạo, cỡ và cách gắn; module câu của loài quyết định loài nào dùng mồi nào, khi nào. Không thay [dụng cụ Mỹ](../01-Knowledge/equipment/us-angling-tackle.md) về rig, nhận lực, quy định.

## Vị trí và mã

- Hồ sơ: `01-Knowledge/equipment/baits/<slug>.md`; sổ nguồn: `01-Knowledge/sources/baits/<slug>.md` (khối JSON `bait_id` + `sources`, cùng cấp A–E/trạng thái truy cập như [hồ sơ loài](species-profile-standard.md)).
- Mã ổn định theo **loại mồi chung**, không theo nhãn hiệu: `EQP-LURE-<LOẠI>` cho mồi giả (`kind: lure`), `EQP-BAIT-<LOẠI>` cho mồi tự nhiên (`kind: natural`). Kiểu cụ thể là `variants` (kebab-case, có `label` và `aliases`): crankbait `squarebill`/`lipless`/`deep-diver`; mồi tự nhiên dùng variant cho trạng thái/cách móc (`live-lip-hooked`, `cut-chunk`...).
- Mỗi tên gọi (slug, `names`, alias biến thể) chỉ trỏ về một mã; validator chặn trùng.
- Mồi tự nhiên là sinh vật đã có hồ sơ loài thì ghi `species_profile: K-SP-...`; hồ sơ mồi chỉ mô tả dạng làm mồi. Asset cũ mang mã khác (ví dụ `EQP-MEPPS-B5M`) ghi trong `legacy_entities`, không đổi ID cũ.

## Sáu mục (≤4.500 ký tự)

1. **Nhận dạng và cấu tạo:** bộ phận nhìn thấy, số/vị trí móc, vật liệu.
2. **Biến thể và cỡ:** bảng `| Biến thể | Thông số | Giá trị | Đơn vị | Nguồn |`; chỉ ghi số có nguồn, `tất cả` khi áp chung. Không đổi đơn vị, không lấy cỡ từ ảnh.
3. **Chuyển động trong nước:** điều khiển/tốc độ tạo ra chuyển động gì; mồi chết/mồi giả không tự bơi.
4. **Cách gắn và rig:** cách móc, rig thường đi kèm; liên kết module dụng cụ, không chép lại.
5. **Checklist hình ảnh:** 3–8 dòng QA soi được trên ảnh.
6. **Chưa biết và giới hạn:** nguồn thiếu, ảnh thiếu, khác biệt theo hãng.

Mục "loài dùng" được tính từ module loài và hiện trong `INDEX.md` sinh tự động; không viết tay trong hồ sơ.

## Liên kết từ module loài

Module `angling` của loài có mục `## Mã mồi` với khối JSON:

```json
{"baits": [{"id": "EQP-BAIT-SHRIMP", "variants": ["live-popping-cork"], "when": "quanh năm, rạn hàu và mép cỏ", "source": "S7"}]}
```

`variants` bỏ trống là mọi biến thể; `when` là mùa/tình huống tiếng Việt; `source` là S-ID trong sổ nguồn **của loài**. Chỉ liên kết mồi mà module đã có nguồn.

## Ảnh tham chiếu

- Manifest `01-Knowledge/sources/baits/photo-references.json` (schema 1), file ảnh giữ local private như ảnh loài; `photos-fetch` tải lại và đăng ký catalog (`equipment` cho lure, `other` cho mồi tự nhiên).
- Ảnh thật PD/CC0/CC BY/CC BY-SA, **tối thiểu 1280×720** (quyết định người dùng 2026-10-25); `quality` 1080p hoặc 720p theo kích thước đo.
- `asset_id` `PH-LURE-...`/`PH-BAIT-...`; `view`: side/top/front/hooked/in-water/group; `roles`: `identity` (nhận ra đúng loại/biến thể bằng mắt), `anatomy` (chi tiết cấu tạo), `assembly` (cách móc/rig). Trường `basis` ghi dấu nhìn thấy làm căn cứ.
- Logo/nhãn hiệu lộ rõ thì ghi trong `use` là không chép; ảnh không nhận ra được loại mồi bằng mắt thì không đưa vào (xóa, không giữ dạng hạ cấp).

## Dùng khi viết nội dung và tạo ảnh

1. Cảnh có câu: `python scripts/bait_profiles.py for-species <loài>` (packet `/na-chayvideo` đã kèm khi interaction không phải natural) trả danh sách mồi gọn: mã, biến thể, mùa, nguồn, ảnh có sẵn và request catalog dựng sẵn.
2. Chọn **một** mồi/biến thể cho cảnh, ghi vào `reference_requirements` đúng `entity_id`/`variant`/role; chỉ mở hồ sơ mồi đó.
3. `/na-taoanh` query catalog bằng request đó; mỗi mồi gửi tối đa một ảnh `identity` và một ảnh `assembly` khi móc/rig lộ trong khung. Mồi không có ảnh thì dựa vào checklist hồ sơ, ghi lý do.

CI chạy `python scripts/bait_profiles.py validate`. Thư viện mồi không giới hạn ý tưởng; mồi chưa có hồ sơ thì nghiên cứu như mồi mới, không thay bằng mồi gần giống.
