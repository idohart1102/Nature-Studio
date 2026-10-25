# Module câu — mahi-mahi

Module `angling` của [K-SP-MAHI-MAHI-001](../../species/mahi-mahi.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn mahi-mahi](../../sources/species/mahi-mahi.md). Version: 1.0 | Updated: 2026-10-25 | Module mới.

## Cách câu có căn cứ

- Cá bị câu bằng trolling và longline cá ngừ; đôi khi lưới trôi [S3]. Nghề cá thương mại Mỹ dùng hook-and-line (câu tay, longline) [S5].
- Mahi bị thu hút bởi vật trôi; ngư dân thả bó tre hoặc ván nổi để gom cá trước khi đánh bắt [S3, S4]. Cảnh câu hợp lý đặt quanh bè Sargassum, vật trôi hoặc rìa dòng nơi rong tụ [S4, S6].
- Mồi tự nhiên hợp sinh học: cá chuồn, cá nhỏ, mực, cua/tôm trong Sargassum [S3, S4, S6]. Đây là thức ăn tự nhiên, không phải danh sách mồi đã kiểm chứng hiệu quả câu.
- Cá nhỏ đi đàn quanh vật trôi, cá đực lớn hay ở biển khơi [S4, S5]: cảnh "cả đàn theo con cá mắc câu" chỉ hợp với cá cỡ đàn.

## Quy định (đọc 2026-10-25, có thể đổi)

| Nội dung | Giá trị | Phạm vi | Nguồn |
|---|---|---|---|
| Giới hạn giữ mỗi người/ngày | 10 | Câu giải trí, South Atlantic | S6 |
| Giới hạn mỗi tàu | 54 | Trừ headboat | S6 |
| Cỡ tối thiểu | 20 in FL | Ngoài khơi FL, GA, SC | S6 |

## Dây, móc, lure

Chưa có nguồn cấp A–D đã mở cho sức chịu lực dây, cỡ móc hay loại lure riêng cho mahi; không ghi số. Chọn cấu hình chung theo [dụng cụ Mỹ](../us-angling-tackle.md) và ghi là giả định dàn cảnh.

## Lỗi cần tránh

- Cá vừa lên khỏi nước vẫn còn màu; màu tắt rất nhanh sau khi chết [S5, S6]. Không để cá đang giãy trên boong đã xám bạc, cũng không để cá nằm lâu vẫn rực như dưới nước.
- Không gắn trán vuông cho mọi cá mắc câu; đúng giới theo brief [S5].
- Không tự thêm dụng cụ khi cảnh là săn mồi tự nhiên.

## Mồi có nguồn (bổ sung 2026-10-25)

- Mahi chủ yếu bị câu bằng kéo mồi sống hoặc mồi giả quanh vật trôi, bè rong hoặc weedline [S11]. Ngoài Maryland, cá tụ dọc weedline và phao bẫy tôm hùm [S14].
- Ballyhoo (cá kìm) thường là mồi ưa dùng khi câu dolphin [S15]. Ngoài khơi Maryland, dolphin ăn dàn mồi giả trộn ballyhoo rig [S12].
- Khi gặp đàn, người câu giữ một con đã mắc câu dưới nước để giữ đàn, ném khúc mồi xuống rồi câu những con nổi lên ăn, hoặc quăng mồi vào giữa đàn [S11]. Mahi nhỏ ("chicken") tụ dưới bóng tàu, câu bằng cách thả trôi mồi [S13].
- Tốc độ kéo: tàu charter khoảng 4,5–6 knot; nghề kéo chung 4–10 knot quanh weedline [S11]. Giữ tàu chạy và có vệt sóng khi cảnh là trolling.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species mahi-mahi`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-BALLYHOO",
   "variants": [
    "rigged-trolling",
    "skirted-ballyhoo"
   ],
   "when": "kéo quanh weedline/vật trôi mùa hè",
   "source": "S12, S15"
  },
  {
   "id": "EQP-LURE-OFFSHORE-TROLLING",
   "when": "kéo quanh weedline, 4–10 knot",
   "source": "S11, S12"
  }
 ]
}
```
