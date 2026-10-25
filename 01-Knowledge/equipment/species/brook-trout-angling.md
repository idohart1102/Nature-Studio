# Module câu — brook trout

Module `angling` của [K-SP-BROOK-TROUT-001](../../species/brook-trout.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn brook trout](../../sources/species/brook-trout.md). Version: 1.0 | Updated: 2026-10-25

## Bối cảnh và cách câu

- Suối nhỏ, nước trong: Iowa khuyên dây mảnh và tiếp cận vực thật nhẹ [S5]. Cá giữ chỗ dưới bờ khoét, gỗ chìm, đá; cảnh câu đặt mồi trôi về các chỗ đó [S4, S5].
- Thức ăn tự nhiên là côn trùng, giáp xác, cá nhỏ [S2, S4]; ruồi khô cũng được dùng (ảnh của Virginia DWR có cá ăn dry fly) [S4]. Natural: không tự thêm dây/móc.
- Ba hướng tách biệt, không gộp phụ kiện: spinning ultralight với spinner/jig nhỏ; fly (mẫu bắt chước mayfly, caddis, stonefly, sculpin, minnow, châu chấu, midge); mồi tự nhiên trôi theo dòng [S8].

## Thông số có nguồn

Các số dưới đây là hướng dẫn trout chung của Iowa DNR, không riêng brook trout [S8].

| Hạng mục | Giá trị | Nguồn |
|---|---|---|
| Dây mono spinning | 6 lb test trở xuống | S8 |
| Cần spinning | 5–7 ft, ném được mồi 1/16 oz | S8 |
| Spinner, plug, jig nhỏ | 1/16 – 1/64 oz, ném ngược dòng | S8 |
| Cần fly | 7½–8 ft, action trung bình–chậm | S8 |
| Tippet | 3 lb test | S8 |
| Lưỡi cho mồi tự nhiên | No. 6 – 14, theo cỡ mồi | S8 |

`No. 6` khác `6/0`; lb-test là sức chịu lực danh định, không phải đường kính hay cân nặng cá.

## Lỗi cần tránh

- Mồi giun để hở mũi lưỡi: cá hay ngậm, cắn rồi nhả; Iowa hướng dẫn xỏ giun hai chỗ và phủ kín lưỡi [S8].
- Lội và câu trên redd lúc cá đẻ hoặc khi trứng còn trong sỏi (Virginia: trứng nở giữa tháng 1 – tháng 2) [S4].
- Dùng cỡ lưỡi/dây biển cho suối nhỏ; dàn cảnh cá câu được cỡ quá lớn so với bảng mục 2 của hồ sơ.
- Mùa và quy định (mùa đóng, cấm mồi sống) theo bang chưa kiểm; tra trước khi viết cảnh có câu.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species brook-trout`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-LURE-JIG",
   "when": "spinning ultralight, jig nhỏ",
   "source": "S8"
  },
  {
   "id": "EQP-LURE-FLY",
   "when": "không gắn mùa",
   "source": "S8"
  },
  {
   "id": "EQP-LURE-INLINE-SPINNER",
   "variants": [
    "standard-inline"
   ],
   "when": "spinning ultralight, ném ngược dòng",
   "source": "S8"
  }
 ]
}
```
