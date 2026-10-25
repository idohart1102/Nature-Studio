# Module câu — smallmouth bass

Module `angling` của [K-SP-SMALLMOUTH-BASS-001](../../species/smallmouth-bass.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn smallmouth bass](../../sources/species/smallmouth-bass.md). Version: 1.0 | Updated: 2026-10-25

## Mồi và cách câu

- Mồi sống hiệu quả: cá con (minnow), tôm đất, ấu trùng hellgrammite [S8]; mùa hè ở hồ dùng tôm đất lột vỏ mềm thả đáy, chì vừa đủ chìm [S9]. Mồi sống phải hợp quy định nơi câu.
- Mồi giả: jig đầu chì (lông/marabou, twister) quanh bờ đá và mỏm lúc tiền sinh sản, kéo chậm, nảy theo đáy khi nước 48–55 °F; crankbait nhỏ màu tôm đất cuối tiền sinh sản và mùa hè; mùa thu crankbait lặn sâu, jig gắn minnow, plug dạng cá mồi [S9]. Suối đục sau mưa: spinnerbait, crankbait có rattle, màu chartreuse/nâu/đen hoặc ánh kim [S9].
- Smallmouth dễ đuổi mồi mặt nước, nhất là sáng sớm và chiều tối [S9]. Ném vượt qua điểm nghi có cá rồi kéo ngang qua; sau tảng đá lớn hoặc mép vực lặng cạnh ghềnh [S9].
- Câu fly được nhiều người coi là cách câu "đỉnh" cho loài này [S8].

## Dụng cụ có số liệu

| Hạng mục | Thông số | Nguồn |
|---|---|---|
| Dây (spinning nhẹ/medium-light) | 2–6 lb test, mono; leader fluorocarbon tùy chọn; braid khi câu jig/nhiều vướng | S9 |
| Jig đầu chì tiền sinh sản (hồ) | 1/8–1/4 oz | S9 |
| Crankbait tiền sinh sản | ~2 in | S9 |
| Móc tôm đất mùa hè | #8 | S9 |
| Fly | cần 5–6 weight, tippet 6X–3X | S9 |

lb-test là sức chịu lực danh định, không phải đường kính hay cân nặng cá. Baitcast nhẹ dùng khi nước lớn, mồi to [S9].

## Lỗi cần tránh

- Cú nhảy, lộn nhào là phản ứng khi đã mắc câu [S10, S14]; dây phải căng liên tục, mồi/lure nằm đúng ở miệng cá trong mọi frame.
- Cá đực canh tổ rất dễ cắn mồi [S9]; tôn trọng quy định mùa câu tổ.
- Không dùng số dây/móc của largemouth cho smallmouth và ngược lại.
- Không mô tả "mùa thu ăn điên cuồng" như sự thật sinh học [S13].

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species smallmouth-bass`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-MINNOW",
   "when": "mồi sống; mùa thu gắn jig",
   "source": "S8, S9"
  },
  {
   "id": "EQP-BAIT-CRAYFISH",
   "when": "mùa hè ở hồ, thả đáy với chì vừa đủ chìm",
   "source": "S9",
   "variants": [
    "softshell"
   ]
  },
  {
   "id": "EQP-BAIT-INSECT-LARVAE",
   "when": "không gắn mùa",
   "source": "S8",
   "variants": [
    "hellgrammite"
   ]
  },
  {
   "id": "EQP-LURE-JIG",
   "when": "tiền sinh sản quanh bờ đá/mỏm, kéo chậm và nảy đáy ở 48–55 °F",
   "source": "S9",
   "variants": [
    "marabou-hair-jig"
   ]
  },
  {
   "id": "EQP-LURE-CRANKBAIT",
   "when": "cuối tiền sinh sản và mùa hè; mùa thu lặn sâu; suối đục sau mưa",
   "source": "S9"
  },
  {
   "id": "EQP-LURE-SPINNERBAIT",
   "when": "suối đục sau mưa",
   "source": "S9"
  },
  {
   "id": "EQP-LURE-GRUB",
   "variants": [
    "curly-tail-jighead"
   ],
   "when": "tiền sinh sản quanh bờ đá, nước 48–55 °F",
   "source": "S9"
  },
  {
   "id": "EQP-LURE-FLY",
   "when": "không gắn mùa",
   "source": "S8"
  }
 ]
}
```
