# Module câu — redfish

Module `angling` của [K-SP-REDFISH-001](../../species/redfish.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn redfish](../../sources/species/redfish.md). Version: 1.1 | Updated: 2026-10-25 | Chuyển từ mục 3 của hồ sơ v2.1, số dây đã mở kiểm lại S6; 1.1 thêm cần surf cho bull red [S6].

## Mồi và cách câu

- Thức ăn tự nhiên gồm cá, cua, tôm [S9]; cá lớn dùng cut mullet là hướng có cơ sở. Dead bait không tự bơi.
- "Bull" red (cá lớn mùa thu ở bãi biển/cầu cảng) câu tốt nhất bằng mồi tự nhiên; người câu surf/pier dùng cần dài hơn 10 ft, đủ cứng cho bộ chì nặng [S6].
- Natural: không tự thêm dây/móc. Angling: chọn một bộ cụ thể; circle hook nhận lực tăng dần theo rig, không tự set ngay lúc chạm. Ngậm mồi, mắc câu và phản kháng là các kết luận khác nhau.
- Popping cork–shrimp, slip-sinker–bait, spoon/jig/plug là các hướng khác nhau, không gộp phụ kiện của mọi bộ.

## Dây (đã kiểm lại 2026-10-25)

| Bối cảnh | Sức chịu lực danh định | Nguồn |
|---|---|---|
| Grass flats | 8–15 lb | S6 |
| Gần vỏ hàu, đá, cọc | 17–25 lb | S6 |
| Surf/pier, máy chứa vài trăm yard | 25–40 lb | S6 |

lb-test là sức chịu lực danh định, không phải đường kính, lực căng hay cân nặng cá. Mono/braid với leader chống mài mòn theo vật cản.

## Lỗi cần tránh

Hook cứng, leader mềm, bait mềm có attachment liên tục. Che khuất không tự là mất vật; không dùng connector mới để nối môi với rig. Không suy độ đau hoặc buộc mọi cá giãy tới hết. Ref circle-hook/assembly tra catalog khi rig cần.

## Mồi có nguồn (bổ sung 2026-10-25)

- Texas: tôm sống là mồi được chọn nhiều nhất cho cá biển ven bờ, gồm red drum; ít red drum bỏ qua finger mullet sống; mồi giả hàng đầu là nhựa mềm đuôi tôm/đuôi shad/paddle tail [S15].
- Cua được dùng làm mồi câu red drum [S16]; cách bẻ đôi cua móc qua thân trong nguồn là cho black drum, chỉ dùng như cách móc phổ biến, không coi là quy định cho red drum.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species redfish`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-SHRIMP",
   "variants": [
    "live-horn-hooked",
    "live-tail-hooked",
    "live-popping-cork"
   ],
   "when": "mồi được chọn nhiều nhất ở Texas",
   "source": "S15"
  },
  {
   "id": "EQP-BAIT-MULLET",
   "variants": [
    "finger-mullet-live"
   ],
   "when": "finger mullet sống",
   "source": "S15"
  },
  {
   "id": "EQP-LURE-SWIMBAIT",
   "variants": [
    "paddletail"
   ],
   "when": "mồi giả hàng đầu ven bờ Texas",
   "source": "S15"
  },
  {
   "id": "EQP-BAIT-BLUE-CRAB",
   "when": "cua làm mồi",
   "source": "S16"
  }
 ]
}
```
