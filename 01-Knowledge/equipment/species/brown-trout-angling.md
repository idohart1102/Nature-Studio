# Module câu — brown trout

Module `angling` của [K-SP-BROWN-TROUT-001](../../species/brown-trout.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn brown trout](../../sources/species/brown-trout.md). Version: 1.0 | Updated: 2026-10-25

## Bối cảnh và cách câu

- **Suối:** câu quanh cây đổ, bờ khoét [S5]; cá chui vào chỗ trú khi thấy động trên bờ [S5], nên cảnh tiếp cận phải kín.
- **Brown lớn ăn cá:** Iowa dùng minnow cho brown lớn, móc nhẹ qua lưng hoặc môi, thả trôi vào vực sâu có chỗ trú [S7]; cá là phần quan trọng trong khẩu phần brown lớn [S5]. Ruồi bắt chước sculpin/minnow là một lựa chọn fly [S7]. Ăn đêm là đặc điểm được Iowa ghi [S5].
- **Cá hồ chạy suối (NY, Lake Ontario):** chủ yếu tháng 10–11 ở Black River, Stony Creek; egg sac, spinner và fly phổ biến nhất [S6].
- Mỗi cảnh chọn một hướng: spinning ultralight, fly, mồi tự nhiên trôi, hoặc egg sac ở suối nhánh; không gộp phụ kiện.

## Thông số có nguồn

Hướng dẫn trout chung của Iowa DNR cho suối, không riêng brown trout, không dành cho cá hồ cỡ lớn [S7].

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Dây mono spinning | 6 lb test trở xuống | S7 |
| Cần spinning | 5–7 ft, ném được mồi 1/16 oz | S7 |
| Spinner, plug, jig nhỏ | 1/16 – 1/64 oz, ném ngược dòng | S7 |
| Cần fly | 7½–8 ft | S7 |
| Tippet | 3 lb test | S7 |
| Lưỡi cho mồi tự nhiên | No. 6 – 14, theo cỡ mồi | S7 |

Chưa có nguồn A/B cho dây/lưỡi khi câu brown hồ chạy suối; không tự suy từ bảng trên.

## Lỗi cần tránh

- Dùng thông số suối nhỏ cho cá hồ 10+ lb, hoặc ngược lại.
- Minnow bị móc xuyên thân nặng nề khi nguồn chỉ nói móc nhẹ qua lưng/môi [S7]; mồi sống phải được phép tại bang đó.
- Lội lên redd khi cá đang đẻ hoặc trứng còn ủ (Virginia: 3–6 tuần) [S4].
- Thêm streamer, egg sac, spinner trong cùng một rig. Mùa đóng câu theo bang chưa kiểm.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species brown-trout`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-MINNOW",
   "when": "brown lớn, thả trôi vào vực sâu có chỗ trú",
   "source": "S7",
   "variants": [
    "lip-hooked",
    "back-hooked"
   ]
  },
  {
   "id": "EQP-BAIT-SALMON-ROE",
   "when": "T10–T11, Black River và Stony Creek, NY",
   "source": "S6",
   "variants": [
    "spawn-sac"
   ]
  },
  {
   "id": "EQP-LURE-FLY",
   "when": "T10–T11, Black River và Stony Creek, NY",
   "source": "S6"
  },
  {
   "id": "EQP-LURE-JIG",
   "when": "suối, ném ngược dòng",
   "source": "S7"
  },
  {
   "id": "EQP-LURE-INLINE-SPINNER",
   "variants": [
    "standard-inline"
   ],
   "when": "T10–T11 cá hồ chạy suối; suối nhỏ",
   "source": "S6, S7"
  }
 ]
}
```
