# Module câu — rainbow trout / steelhead

Module `angling` của [K-SP-RAINBOW-TROUT-001](../../species/rainbow-trout.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn rainbow-trout](../../sources/species/rainbow-trout.md). Version: 1.0 | Updated: 2026-10-25

## Mồi và cách câu

- **Steelhead trong suối (thu–đông–xuân):** egg sac, ruồi giả trứng, trout bead, streamer, nymph; thả trôi sát đáy hoặc treo dưới phao [S8]. PA thêm minnow, sâu, mealworm, paste bait, spoon, spinner, Woolly Bugger [S7]; Ohio dùng spoon, spinner, mồi giả trứng và ruồi [S10].
- Kỹ thuật trôi: quăng ngược dòng vào chỗ cá giữ, dẫn dây bằng hoặc chậm hơn dòng; giật khi phao/mồi khựng [S7]. Chì cách mồi 6–12 in, rải trong đoạn 24 in thay vì dồn một chỗ [S7].
- **Steelhead ngoài hồ (xuân–hè):** kéo (troll) spoon và plug nhỏ quanh thermal bar; đỏ hoặc cam hiệu quả [S8]; Ohio câu ngoài hồ T5–T9 bằng spoon và mồi giả [S10].
- Rainbow thả mùa thu–đông có thể câu ngay sau khi thả [S13]; chưa có nguồn đã mở về mồi riêng cho cá thả hồ.

## Bộ dụng cụ steelhead (Lake Erie, PA)

| Thành phần | Thông số | Nguồn |
|---|---|---|
| Cần spin (noodle rod) | 8 ft 6 in–10 ft, medium-light hoặc light | S7 |
| Máy | spinning cỡ 2500 trở lên, drag tốt | S7 |
| Dây chính | mono 8 lb test | S7 |
| Leader | fluorocarbon 4 hoặc 6 lb test (tùy nước) | S7 |
| Lưỡi | cỡ 18 tới 4 (số nhỏ = lưỡi lớn) | S7 |
| Cần ruồi | 9 ft, 6–8 weight; dây weight-forward; leader 9 ft 2x–3x; 100 yd backing | S7 |

lb-test là sức chịu danh định, không phải đường kính hay cân nặng cá. Bộ này là ví dụ của PA Erie; nước khác cần kiểm nguồn riêng.

## Lỗi cần tránh

- Không gộp phụ kiện của bộ suối (phao, split shot, egg sac) với bộ kéo ngoài hồ.
- Cá đánh mạnh: mất cá thường do nút buộc kém, dây chùng, lưỡi yếu; cần nghiêng thấp, để cá kéo dây khi chạy [S7]. Không vẽ cần gập ở ngọn.
- Thả cá: dùng vợt, giữ cá trong nước khi gỡ lưỡi, làm ướt tay [S7]; không treo cá dọc theo dây.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species rainbow-trout`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-SALMON-ROE",
   "when": "steelhead trong suối thu–đông–xuân, sát đáy hoặc dưới phao",
   "source": "S8",
   "variants": [
    "spawn-sac"
   ]
  },
  {
   "id": "EQP-LURE-EGG-IMITATION",
   "when": "steelhead trong suối thu–đông–xuân, sát đáy hoặc dưới phao",
   "source": "S8",
   "variants": [
    "yarn-egg",
    "trout-bead"
   ]
  },
  {
   "id": "EQP-LURE-FLY",
   "when": "steelhead trong suối thu–đông–xuân",
   "source": "S8, S10"
  },
  {
   "id": "EQP-LURE-SPOON",
   "when": "trolling ngoài hồ xuân–hè; ném trong suối",
   "source": "S7, S8, S10"
  },
  {
   "id": "EQP-BAIT-MINNOW",
   "when": "steelhead trong suối",
   "source": "S7"
  },
  {
   "id": "EQP-BAIT-INSECT-LARVAE",
   "variants": [
    "mealworm"
   ],
   "when": "steelhead trong suối",
   "source": "S7"
  },
  {
   "id": "EQP-LURE-INLINE-SPINNER",
   "variants": [
    "standard-inline"
   ],
   "when": "steelhead trong suối",
   "source": "S7, S10"
  }
 ]
}
```
