# Module câu — yellowfin tuna

Module `angling` của [K-SP-YELLOWFIN-TUNA-001](../../species/yellowfin-tuna.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn yellowfin](../../sources/species/yellowfin-tuna.md). Version: 1.0 | Updated: 2026-10-25

## Phương pháp có nguồn

- Câu giải trí: tỷ lệ lớn sản lượng từ rod and reel; được thả lại (catch-and-release) [S5].
- Ngư cụ giải trí được phép cho tuna: rod and reel, handline; bandit, greenstick theo permit; speargun chỉ với cá BAYS (gồm yellowfin) **bơi tự do**, không bắn cá đang mắc dây [S7].
- Surface trolling: tàu chạy liên tục >4 knot, có vệt sóng; không dùng downrigger/wire/planer [S7]. Greenstick: dây chính treo trên mặt, tối đa 10 lưỡi [S7].
- Thương mại: chủ yếu longline, rod and reel, handline [S5].
- Hành vi liên quan: tụ dưới gỗ trôi và vật nổi [S3, S8]; kiếm ăn bằng mắt ở tầng mặt ban ngày [S8].
- Circle hook: mũi quay vuông góc về thân lưỡi; J-hook không đạt định nghĩa đó [S7]. Chọn một loại, giữ nguyên qua frame.

## Quy định ảnh hưởng cảnh (kiểm lại trước khi dùng)

| Nội dung | Giá trị | Nguồn |
|---|---|---|
| Cỡ tối thiểu | 27 in CFL | S6, S7 |
| Bag limit | 3 cá/người/ngày hoặc chuyến | S6, S7 |
| Cá bị cá mập cắn | Phần còn lại vẫn phải ≥27 in (69 cm) CFL | S7 |
| Cá thả | Thả ngay, không đưa khỏi nước | S7 |

CFL đo theo đường cong thân từ mút hàm trên tới chẽ đuôi [S6]. Cần permit HMS Angling hoặc Charter/Headboat [S6].

## Lỗi cần tránh

Không có nguồn A/B đã mở cho lb-test dây, cỡ lưỡi hay leader của yellowfin: không ghi số cụ thể vào prompt. Không bắn speargun vào cá đang mắc câu; không trộn trolling với downrigger khi đã gọi là surface trolling. Không gán cảnh đi cùng cá heo cho vùng Mỹ khi chưa có nguồn.

## Mồi có nguồn (bổ sung 2026-10-25)

- Ngoài khơi Maryland, yellowfin bị câu bằng hai cách chính: kéo ballyhoo rig (thường trong dàn trộn với mồi giả) và chunking [S15, S16].
- Chunking cho yellowfin hay làm vào ban đêm ở vùng canyon, tàu đi qua đêm, cuối hè–đầu thu [S17, S18]. Đây là kỹ thuật "đặc biệt cho tuna": ném khúc cá cắt xuống nước để dụ cá tới tàu [S14].
- Mồi tự nhiên phổ biến trên tàu câu HMS: herring, mackerel, whiting, mullet, menhaden, ballyhoo, butterfish, mực. Dàn kéo tuna thường gồm umbrella rig mồi nhựa mềm dưới mặt nước, ngoài ra có thể ném mồi giả vào đàn đang đớp mặt hoặc jig thẳng đứng [S14].
- Cedar plug cho yellowfin mới chỉ có nguồn E [S19]; nếu dùng trong cảnh thì ghi là giả định dàn cảnh.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species yellowfin-tuna`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-BALLYHOO",
   "variants": [
    "rigged-trolling"
   ],
   "when": "kéo ngoài khơi mùa hè",
   "source": "S15, S16"
  },
  {
   "id": "EQP-BAIT-MENHADEN",
   "variants": [
    "cut-bunker-chunk"
   ],
   "when": "chunking ban đêm ở canyon, cuối hè–thu",
   "source": "S14, S17"
  },
  {
   "id": "EQP-LURE-OFFSHORE-TROLLING",
   "variants": [
    "skirted-trolling-lure"
   ],
   "when": "trolling ngoài khơi",
   "source": "S14, S16"
  }
 ]
}
```
