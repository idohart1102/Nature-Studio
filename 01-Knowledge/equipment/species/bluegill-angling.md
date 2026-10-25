# Module câu — bluegill

Module `angling` của [K-SP-BLUEGILL-001](../../species/bluegill.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn bluegill](../../sources/species/bluegill.md). Version: 1.0 | Updated: 2026-10-25

## Cách câu có nguồn

| Cách | Chi tiết | Nguồn |
|---|---|---|
| Phao + mồi tự nhiên | Giun phổ biến nhất; côn trùng, ấu trùng; phao báo cá vì bluegill hút mồi chứ không giật | S4 |
| Mồi tự nhiên/lure nhỏ | Giun, dế; spinner nhỏ | S7 |
| Mùa hè | Thuyền ở nước sâu 5–15 ft | S4 |
| Fly | Ruồi ướt hoặc khô, tốt nhất mùa côn trùng nở cuối xuân–đầu hè | S4, S7 |
| Câu băng | Cần jig ngắn nhẹ, dây nhẹ, jig nhỏ hình giọt nước gắn ấu trùng (grub), ở đám cỏ nước vùng sâu hơn | S4 |
| Câu băng (Iowa, T12/2019) | Jig nhỏ gắn waxworm ở mép cỏ nước hoặc đống cành; wigglers dọc mép cỏ | S9, S10 |

## Móc và dây

- Miệng nhỏ nên dùng móc nhỏ [S4]; NC ghi móc cỡ No. 10 [S7]. `#10` là cỡ móc nhỏ, khác `10/0`.
- Giật móc ngay khi có dấu cắn thường hiệu quả nếu mồi và móc nhỏ [S4].
- Chưa có nguồn A/B cho sức chịu lực dây (lb-test); S4 chỉ ghi "light-weight line". Không tự đặt con số.

## Lỗi cần tránh

Không dùng móc/lure cỡ bass cho miệng bluegill. Phao, dây, móc và mồi là một cấu hình; không gộp phụ kiện của mọi cách câu vào một rig. Cá mắc câu quay mình ngang chạy vòng góc vuông [S4], không lao thẳng như cá săn mồi lớn. Không suy mắc câu từ một frame cá chạm mồi.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species bluegill`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-CRICKET",
   "when": "không gắn mùa",
   "source": "S7",
   "variants": [
    "cricket"
   ]
  },
  {
   "id": "EQP-LURE-FLY",
   "when": "mùa côn trùng nở cuối xuân–đầu hè",
   "source": "S4, S7",
   "variants": [
    "wet-fly",
    "dry-fly"
   ]
  },
  {
   "id": "EQP-LURE-JIG",
   "when": "câu băng ở đám cỏ nước vùng sâu hơn",
   "source": "S4",
   "variants": [
    "teardrop-ice-jig"
   ]
  },
  {
   "id": "EQP-BAIT-INSECT-LARVAE",
   "when": "câu băng T12/2019 ở Iowa, mép cỏ nước hoặc đống cành",
   "source": "S9, S10",
   "variants": [
    "waxworm"
   ]
  },
  {
   "id": "EQP-BAIT-NIGHTCRAWLER",
   "variants": [
    "whole-hooked"
   ],
   "when": "dưới phao, mồi phổ biến nhất",
   "source": "S4, S7"
  },
  {
   "id": "EQP-LURE-INLINE-SPINNER",
   "variants": [
    "standard-inline"
   ],
   "when": "spinner nhỏ",
   "source": "S7"
  }
 ]
}
```
