# Module câu — black crappie

Module `angling` của [K-SP-BLACK-CRAPPIE-001](../../species/black-crappie.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn black crappie](../../sources/species/black-crappie.md). Version: 1.0 | Updated: 2026-10-25 | Module mới; MDC và AGFC nói chung cho "crappie", PA tách riêng black crappie.

## Cách câu có nguồn

| Cách | Chi tiết | Nguồn |
|---|---|---|
| Mồi tự nhiên gần đáy hoặc dưới phao | Grub, giun, minnow; dế/châu chấu trên móc dây mảnh thả mặt nước | S7 |
| Lure nhỏ | Spinner, twister, crankbait nhỏ | S7 |
| Vertical jigging | Thả thẳng vào bụi tới đáy, kéo lên chậm tới khi có cá, giữ đúng tầng đó | S6 |
| Jigging spoon nhỏ | Nhấc–hạ 1–2 ft trên bụi sâu; cá hay đớp khi spoon đang rơi | S6 |
| Ném qua bụi | Ném quá bụi, chìm tới đáy trên dây căng, kéo chậm qua cành; dùng ở bụi nông hoặc nước trong | S6 |
| Phao | Jig/minnow treo gần như đứng yên khi cá lười | S6 |
| Theo mùa | Mùa thu quanh cầu tàu tầng 10 ft trên; mùa đông kéo rất chậm | S6 |
| FFS (sonar quét trước) | Chiếu sonar vào bụi chìm để xem có cá trước khi thả; cần crappie 10–12 ft, minnow | S10 |

## Dây, móc, mồi giả

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Dây | 4–8 lb test | S7 |
| Cỡ móc | 4–8 | S7 |
| Lure | 1/32–1/8 oz | S7 |
| Màu lure | đen, nâu, xanh lá | S7 |

Dây, móc và cỡ lure lấy từ bảng mẹo black crappie của PA [S7]; MDC không ghi số [S6]. Jig weedless hợp nhất khi đưa mồi vào trong bụi [S6]. lb-test là sức chịu lực danh định, không phải đường kính hay cân nặng cá.

## Lỗi cần tránh

- Không tự thêm wire leader hay móc lớn của loài khác; giữ một cấu hình (jig, mồi–phao, hoặc spoon) mỗi cảnh.
- Cảnh FFS: cá thấy trên màn hình không có nghĩa là sẽ cắn; cá có thể chìm vào cành khi thuyền tới gần [S10].
- Màn hình sonar là hình hiển thị âm, không vẽ thành ảnh quang học của từng con cá.
- Cảnh câu băng: chưa có nguồn đã mở về dụng cụ câu băng cho loài này; không tự đặt thông số.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species black-crappie`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-MINNOW",
   "when": "gần đáy hoặc dưới phao",
   "source": "S7"
  },
  {
   "id": "EQP-LURE-JIG",
   "when": "treo gần như đứng yên khi cá lười",
   "source": "S6"
  },
  {
   "id": "EQP-LURE-SPOON",
   "when": "nhấc–hạ 1–2 ft trên bụi sâu",
   "source": "S6",
   "variants": [
    "jigging-spoon"
   ]
  },
  {
   "id": "EQP-BAIT-CRICKET",
   "when": "thả mặt nước trên móc dây mảnh",
   "source": "S7",
   "variants": [
    "cricket",
    "grasshopper"
   ]
  },
  {
   "id": "EQP-LURE-CRANKBAIT",
   "when": "lure nhỏ, không gắn mùa",
   "source": "S7"
  },
  {
   "id": "EQP-BAIT-NIGHTCRAWLER",
   "when": "gần đáy hoặc dưới phao",
   "source": "S7"
  },
  {
   "id": "EQP-LURE-GRUB",
   "variants": [
    "curly-tail-jighead"
   ],
   "when": "twister nhỏ 1/32–1/8 oz",
   "source": "S7"
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
