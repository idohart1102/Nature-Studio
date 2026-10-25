# Module câu — muskie

Module `angling` của [K-SP-MUSKIE-001](../../species/muskie.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn muskie](../../sources/species/muskie.md). Version: 1.1 | Updated: 2026-10-25 | Chuyển từ mục 3 của hồ sơ v2.1; sửa trích dẫn dây và đánh dấu leader chưa xác nhận; 1.1 thêm cuối thu (S16).

## Mồi giả

- Plugs, spoons, bucktails là các nhóm lure cơ quan quản lý nêu [S9]. Cánh spinner cần nước chuyển động tương đối; bucktail không tự bơi như prey.
- **Mepps Musky Killer B5M standard:** một treble #5/0, cánh Aglia chạy nông, cánh cỡ 5, 3/4 oz [S14]. Không ghép với tandem hoặc Magnum; kiểm mẫu/ref trước khi khóa số điểm treo.
- **Cuối thu:** Indiana DNR khuyên nhắm các thảm cỏ còn sót (còn mồi và che chắn), dùng lure lớn hoặc sucker sống để có cú đớp của cá lớn [S16]. Đây là gợi ý mùa của một bang, không là cấu hình rig.
- Cá thường theo mồi tới thuyền mà không đớp; người câu vẽ số 8 cạnh thuyền [S4]. Không diễn figure-eight nếu điểm kéo/khung không hỗ trợ.

## Dây và leader

| Thành phần | Thông số | Nguồn | Trạng thái |
|---|---|---|---|
| Dây braid (spectra) nặng | 50–80 lb | [S4] | Xác nhận, tài liệu 2012 |
| Dây (trang hướng dẫn cơ bản) | 20–35 lb | [S8] | Xác nhận |
| Leader wire hoặc fluorocarbon nặng | 12–14 in; fluoro ~100–170 lb | [S13] | Chỉ trích đoạn tìm kiếm |

Bản v2.1 ghi "fluoro 130 lb dài 14 in" theo Mercury/Saric; chưa mở được trang để xác nhận, con số 130 lb chỉ thấy ở bài báo cấp E [S15]. Leader không chống cắn tuyệt đối. Live-sucker quick-strike là cấu hình khác, cần nghiên cứu riêng và theo quy định địa phương.

## Lỗi cần tránh

Không ép một circle hook cho mọi lure; giữ số hook/nhánh/leader của mẫu thật. Phân biệt ngậm lure, attachment và lực dây. Không dùng răng/miệng pike thay thế khi thiếu ref; không dùng rig redfish.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species muskie`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-LURE-SPOON",
   "when": "không gắn mùa",
   "source": "S9"
  },
  {
   "id": "EQP-LURE-INLINE-SPINNER",
   "when": "bucktail chạy nông",
   "source": "S9, S14",
   "variants": [
    "musky-bucktail"
   ]
  },
  {
   "id": "EQP-BAIT-SUCKER",
   "variants": [
    "live-large-sucker",
    "quick-strike-rig"
   ],
   "when": "cuối thu quanh thảm cỏ còn sót",
   "source": "S16"
  }
 ]
}
```
