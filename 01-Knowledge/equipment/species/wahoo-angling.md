# Module câu — wahoo

Module `angling` của [K-SP-WAHOO-001](../../species/wahoo.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn wahoo](../../sources/species/wahoo.md). Version: 1.0 | Updated: 2026-10-25 | Module mới.

## Cách câu có căn cứ

- Ở Mỹ wahoo là cá câu thể thao, bắt bằng hook-and-line [S4]. Dụng cụ được phép ở Atlantic: automatic reel, bandit gear, câu tay, longline nổi, cần–máy, súng/xiên lặn (kể cả powerhead) [S5].
- Đặt cảnh ở biển khơi gần mặt nước, quanh gò ngầm, đỉnh đá, vật trôi hoặc Sargassum [S4, S5]. Cá đơn lẻ hoặc vài con [S3, S5].
- Mồi tự nhiên hợp sinh học: cá biển khơi nhỏ và mực [S3, S5, S6]. Đây là thức ăn tự nhiên, không phải danh sách mồi đã kiểm chứng hiệu quả câu.
- Cú đớp rất nhanh: bứt tốc ngắn tới 75 km/h [S4].

## Răng và leader

Răng tam giác, dẹt, có răng cưa và dùng để cắt mồi [S3, S5]: leader mềm dễ bị cắt là rủi ro có cơ sở. Leader thép/cáp và trolling tốc độ cao chỉ thấy ở nguồn cấp D/E [S12], số liệu mâu thuẫn; module không ghi sức chịu lực dây, cỡ móc hay cỡ leader. Chọn cấu hình chung theo [dụng cụ Mỹ](../us-angling-tackle.md) và ghi là giả định dàn cảnh.

## Quy định (đọc 2026-10-25, có thể đổi)

| Nội dung | Giá trị | Phạm vi | Nguồn |
|---|---|---|---|
| Giới hạn giữ | 2 | Câu giải trí NC, SC, GA, FL | S6 |
| Cỡ tối thiểu | Không có | Như trên | S6 |
| Khi cập bến | Còn nguyên đầu và vây | Như trên | S6 |

## Lỗi cần tránh

- Vạch xanh tắt nhanh sau khi chết [S5]: cá còn sống giữ vạch rõ, cá nằm lâu trên boong thì nhạt.
- Không vẽ cả đàn wahoo đuổi theo mồi câu; loài này đơn lẻ hoặc nhóm lỏng [S3, S5].
- Không tự thêm dụng cụ khi cảnh là săn mồi tự nhiên.

## Mồi có nguồn (bổ sung 2026-10-25)

- Wahoo chủ yếu bị câu bằng trolling, giống cách câu dolphin [S13]. Câu giải trí tập trung ngoài North Carolina và bờ đông Florida [S13].
- Ngoài khơi Maryland, wahoo nằm trong mẻ của đội tàu trolling, đông vào giữa tháng 8 [S14]. Có ngày tàu ra điểm từ rạng sáng và câu được wahoo lớn trong dàn mồi giả trộn ballyhoo rig [S15].
- Nghề kéo dolphin–wahoo chạy 4–10 knot quanh weedline [S13]. Kéo tốc độ cao (trên 10 knot), skirted lure nặng đầu, diving plug và leader thép chỉ có nguồn E [S12, S16]: ghi là giả định dàn cảnh, không ghi số.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species wahoo`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-LURE-OFFSHORE-TROLLING",
   "when": "trolling ngoài khơi, đông cá giữa T8 (Maryland)",
   "source": "S13, S14"
  }
 ]
}
```
