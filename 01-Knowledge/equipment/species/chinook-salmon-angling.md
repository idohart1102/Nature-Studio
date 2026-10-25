# Module câu — Chinook salmon

Module `angling` của [K-SP-CHINOOK-SALMON-001](../../species/chinook-salmon.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn chinook-salmon](../../sources/species/chinook-salmon.md). Version: 1.0 | Updated: 2026-10-25

## Cách câu theo bối cảnh

- **Ngoài hồ Great Lakes (xuân–hè):** tìm cá lơ lửng ở nước 50–55 °F; downrigger, diver, dây wire; spoon hoặc flasher/fly [S9]. Michigan: downrigger, dây lead-core hoặc copper đưa spoon, dodger–fly, cut bait xuống sâu, thường 100 ft+ [S10].
- **Cửa suối mùa thu:** kéo từ mặt tới 60 ft với spoon, J-plug, cut bait, flasher/fly [S9].
- **Trong suối:** spoon, spinner, plug; spawn túi hoặc mẩu skein dưới phao/sát đáy [S10]; mồi nhựa giả trứng, ruồi, egg sac, streamer [S9].
- Cá chạy đẻ không ăn [S6]; không diễn tả cắn mồi như cá đang săn.

## Bộ spin sông (ví dụ ADF&G, Alaska)

| Thành phần | Thông số | Nguồn |
|---|---|---|
| Cần | medium heavy–extra heavy, action moderate–fast, 7–8,5 ft, chịu 15–30 lb test | S14 |
| Máy | cân với cần (cần 20 lb thì máy cũng 20 lb) | S14 |
| Dây | 15–30 lb test; mono, braid hoặc fluorocarbon | S14 |
| Mồi giả | Pixee spoon 1/2–7/8 oz; Vibrax spinner cỡ 5–6; Tee spoon 9–13; Spin-n-glow 3/4–1,25 in; egg-sucking leech cỡ 1–2 | S14 |
| Phụ kiện | khóa xoay (snap/lock), chì kẹp/xoắn; trứng muối nơi luật cho phép | S14 |

ADF&G nêu đây là ví dụ, không bảo đảm hiệu quả, không xác nhận sản phẩm [S14]. Chưa có nguồn đã mở về dây/lưỡi cho câu kéo Great Lakes.

## Lỗi cần tránh

- Không gộp downrigger/flasher của bộ kéo hồ với phao/egg sac của bộ suối.
- Kiểm quy định mồi tự nhiên theo vùng [S14]. lb-test là sức chịu danh định, không phải cân nặng cá.
- Cá lớn chạy mạnh: máy phải đủ dây (Michigan ghi chinook có thể kéo hết dây máy thiếu sức chứa [S10]).

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species chinook-salmon`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-LURE-SPOON",
   "when": "xuân–hè, Great Lakes, trolling xuống sâu",
   "source": "S9, S10",
   "variants": [
    "trolling-spoon"
   ]
  },
  {
   "id": "EQP-LURE-PLUG",
   "when": "cửa suối mùa thu, kéo từ mặt tới 60 ft",
   "source": "S9",
   "variants": [
    "slip-head-plug"
   ]
  },
  {
   "id": "EQP-LURE-FLASHER-RIG",
   "when": "xuân–hè, Great Lakes, downrigger đưa mồi xuống sâu",
   "source": "S9, S10",
   "variants": [
    "flasher-fly",
    "dodger-fly"
   ]
  },
  {
   "id": "EQP-BAIT-SALMON-ROE",
   "when": "trong suối, dưới phao hoặc sát đáy",
   "source": "S10",
   "variants": [
    "spawn-sac",
    "skein-chunk"
   ]
  },
  {
   "id": "EQP-LURE-EGG-IMITATION",
   "when": "trong suối",
   "source": "S9",
   "variants": [
    "soft-plastic-egg"
   ]
  },
  {
   "id": "EQP-LURE-FLY",
   "when": "trong suối",
   "source": "S9"
  },
  {
   "id": "EQP-LURE-INLINE-SPINNER",
   "variants": [
    "standard-inline"
   ],
   "when": "trong suối",
   "source": "S10"
  }
 ]
}
```
