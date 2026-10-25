# Module câu — blue catfish

Module `angling` của [K-SP-BLUE-CATFISH-001](../../species/blue-catfish.md); chỉ nạp khi cảnh có câu cá. Cơ chế chung (rig, nhận lực, quy định) ở [dụng cụ Mỹ](../us-angling-tackle.md). Nguồn S-ID theo [sổ nguồn blue catfish](../../sources/species/blue-catfish.md). Version: 1.0 | Updated: 2026-10-25

## Mồi và cách câu

- Mồi ưa dùng: gizzard shad, skipjack herring [S7]; cut bait hoặc mồi có mùi chế sẵn [S10]. Cá lớn chủ yếu ăn cá [S10] nên mồi cá cắt là hướng có cơ sở.
- Rig đáy: Carolina rig (fish finder rig), chì 3/4–1 1/2 oz thường đủ giữ mồi ở vùng ăn trên sông triều Virginia [S10].
- Phương pháp: trotline và jug line mồi cá phổ biến nhất trên Mississippi/Missouri [S7]; trotliner bắt được cá lớn nhất ở Texas [S5]. Một số đoạn (dưới đập Truman, sông Osage) chỉ cho cần và dây [S7]. Trotline/jug không có người cầm cần trong khung.
- Vị trí theo mùa: sau đẻ tìm hố sâu, mép dốc, khúc cua lạch có cấu trúc; lúc di cư đẻ thử cửa lạch [S11]. Mùa khô VA DWR khuyên câu xa hơn về thượng lưu vì cá ưa nước ngọt [S11].
- Bắt tay (handfishing/noodling): MDC mô tả là thò tay vào hốc tổ khi blue và flathead canh tổ (T6–T7); **cấm ở Missouri**, một số bang khác cho phép — hợp pháp tùy bang, phải kiểm quy định bang cụ thể trước khi dựng cảnh [S12]. Cá bị bắt khỏi tổ thì trứng chết nhanh [S12].

## Dây và móc

Chưa có nguồn A/B nêu sức chịu lực dây hay cỡ móc cho blue catfish: không tự ghi số. Nếu cảnh cần, tra nguồn cơ quan bang hoặc nhà sản xuất (cấp D, chỉ cho dụng cụ) và thêm vào sổ nguồn trước. lb-test là sức chịu lực danh định, không phải cân nặng cá.

## Lỗi cần tránh

- Không dùng kỷ lục 143 lb [S10] làm cỡ mặc định của cá mắc câu.
- Virginia khuyến khích thu hoạch blue cỡ nhỏ, theo khuyến cáo tiêu thụ của Sở Y tế [S10]; giới hạn bag/size khác nhau theo bang và thủy vực, tra quy định hiện hành.
- Không gộp trotline, jug, cần máy và bắt tay trong cùng một cảnh; không gắn noodling cho bang cấm.

## Mã mồi

Mã trong [thư viện mồi](../baits/INDEX.md); tra nhanh bằng `python scripts/bait_profiles.py for-species blue-catfish`. Chỉ liệt kê mồi đã có nguồn trong module này; chọn một mồi/biến thể cho cảnh.

```json
{
 "baits": [
  {
   "id": "EQP-BAIT-SHAD-HERRING",
   "when": "không gắn mùa",
   "source": "S7"
  }
 ]
}
```
