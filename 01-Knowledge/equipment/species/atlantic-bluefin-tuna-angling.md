# Module câu — Atlantic bluefin tuna

Module `angling` của [K-SP-ATLANTIC-BLUEFIN-001](../../species/atlantic-bluefin-tuna.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn bluefin](../../sources/species/atlantic-bluefin-tuna.md). Version: 1.0 | Updated: 2026-10-25

## Phương pháp có nguồn

- Ngư cụ giải trí được phép cho tuna: rod and reel, handline; bandit và greenstick chỉ với một số loại permit; speargun **không** dùng cho bluefin (chỉ cá BAYS bơi tự do) [S7].
- Greenstick: dây chính kéo chủ động, treo trên mặt nước, tối đa 10 lưỡi/gangion [S7]. Surface trolling: tàu chạy liên tục >4 knot, có vệt sóng [S7].
- Thương mại: handgear (rod and reel, handline, harpoon) và lưới vây; longline không được nhắm bluefin [S5]. Harpoon/gaff/tail rope ngoài thương mại chỉ là "secondary gear" ở mạn tàu, không dùng để bắt cá bơi tự do [S7].
- Mồi có căn cứ: cá lớn ngoài Cape Hatteras đớp menhaden mạnh [S8]; người câu nhắm vào đàn [S5].
- Circle hook: mũi quay vuông góc về thân lưỡi, hình tròn/oval; J-hook là loại không đạt định nghĩa đó [S7]. Chọn một loại cho rig, không đổi giữa các frame.

## Quy định ảnh hưởng cảnh (kiểm lại trước khi dùng)

| Nội dung | Giá trị | Nguồn |
|---|---|---|
| Cỡ tối thiểu giữ lại | 27 in CFL | S6, S7 |
| Nhóm trophy | ≥73 in CFL, 1 cá/tàu/năm | S6 |
| Gulf of America | Cấm câu nhắm bluefin | S5, S6 |
| Cá thả | Thả ngay, không đưa khỏi nước | S5, S7 |
| Bán cá câu giải trí | Không được | S5 |

CFL đo theo đường cong thân từ mút hàm trên tới chẽ đuôi [S7]. Trạng thái mở/đóng đổi trong mùa [S6].

## Lỗi cần tránh

Không có nguồn A/B đã mở cho lb-test dây, cỡ lưỡi hay leader của bluefin: không ghi số cụ thể vào prompt. Không cho bluefin bị speargun, không dựng cảnh nhắm bluefin ở Gulf of America, không kéo cá thả lên boong. Cá thả không được đưa khỏi nước; ngư cụ phụ (gaff, tail rope) chỉ xuất hiện với cá đã giữ lại hợp lệ.

## Mồi có nguồn (bổ sung 2026-10-25)

- Kéo mồi (trolling) là cách câu bluefin có căn cứ ngoài khơi Maryland: bluefin cỡ trung bị câu bằng trolling giữa tháng 5 [S20], và cùng yellowfin, dolphin ăn dàn mồi giả trộn ballyhoo rig dọc đường đẳng sâu 30 sải [S19].
- Chunking (ném khúc cá cắt xuống nước để dụ cá tới tàu, mồi trên lưỡi trôi lẫn trong đó) là kỹ thuật dùng "đặc biệt cho tuna" [S18]; với bluefin ghép thêm menhaden mà cá lớn đớp mạnh ngoài Cape Hatteras [S8].
- Mồi tự nhiên phổ biến trên tàu câu HMS gồm herring, mackerel, whiting, mullet, menhaden, ballyhoo, butterfish, mực [S18]; chọn một loại cho cảnh, không trộn nhiều mồi trên một lưỡi.
- Dàn kéo tuna thường là umbrella rig nhiều mồi nhựa mềm chạy dưới mặt nước [S18]; chưa có nguồn A/B riêng cho bluefin về cedar plug hay spreader bar, không gán cho cảnh như sự thật đã kiểm.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species atlantic-bluefin-tuna`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-MENHADEN",
   "variants": [
    "cut-bunker-chunk"
   ],
   "when": "chunking khi tàu thả trôi/neo; cá lớn ngoài Cape Hatteras",
   "source": "S8, S18"
  },
  {
   "id": "EQP-BAIT-BALLYHOO",
   "variants": [
    "rigged-trolling"
   ],
   "when": "kéo ngoài khơi mùa hè, dàn trộn mồi giả",
   "source": "S19"
  },
  {
   "id": "EQP-LURE-OFFSHORE-TROLLING",
   "when": "trolling ngoài khơi",
   "source": "S18, S19"
  }
 ]
}
```
