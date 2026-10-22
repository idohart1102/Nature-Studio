# Asset tham chiếu dùng trên nhiều máy

64 ảnh AI đã chọn và QA tĩnh, nền trắng có nhãn kích thước: 27 ảnh cá Redfish/Muskie/Walleye, 12 lưỡi câu, 8 cần, 3 máy câu, 4 dây/leader, 5 mồi thật, 2 mồi giả và 3 rig. Tổng ảnh khoảng 106 MB; từng PNG dưới 3 MB. Đây là tài sản tham chiếu đã được người dùng cho xuất bản, không phải hồ sơ production.

## Dùng sau khi clone hoặc tải ZIP

Tại gốc Nature-Studio chạy một lần:

```text
python scripts/asset_catalog.py import-bundle 08-Assets/reference-library.json
```

Lệnh kiểm hash file/review và dependency rồi tạo/cập nhật catalog local cho các ID chưa có. Không tải từ dịch vụ ngoài, không copy 64 ảnh thêm lần nữa, không gọi model và không cấp mã/quota. Chạy lại giữ nguyên mục local tương đương; gặp cùng ID khác dữ liệu thì dừng, không ghi đè. Dữ liệu riêng và metadata local được giữ.

Sau đó /na-chayvideo và /na-taoanh tra catalog như bình thường. Khi tra lần đầu mà catalog chưa có hoặc thiếu bộ ref đi kèm, AI tự chạy lệnh nhập trên trước khi kết luận thiếu ảnh. Không đọc toàn bộ manifest này vào context mỗi lần; helper xử lý file và trả tóm tắt. Chỉ mở metadata/ảnh phù hợp yêu cầu.

## Quy ước

- `reference-library.json`: manifest công khai, ID và hash; `images/`: 64 PNG final; `reviews/`: review được làm sạch.
- 61 ảnh dùng chung phù hợp, 3 rig giới hạn Project Underwater. Life stage/cỡ là trường riêng; 4 mồi nguyên con chưa xác định stage, không tự adult.
- Nhãn kích thước AI là mục tiêu thiết kế, không chứng minh số đo thật hoặc SKU. Nền trắng/chữ/tư thế trưng bày không tự đưa vào cảnh.
- Nguồn ngoài trong metadata là nguồn nghiên cứu, không phải ảnh đã tải/repub hoặc giấy phép ảnh ngoài. Full generation/edit inputs và ảnh lỗi không phân phối; metadata nêu rõ giới hạn provenance.
- Thêm asset sau này chỉ xuất những bản đã chọn, kiểm quyền/phạm vi và làm sạch review; cập nhật manifest rồi import. Không xuất database runtime, prompt/attempt riêng hoặc con trỏ ổ đĩa máy.

Xem [quy trình tham chiếu](../00-Standards/first-frame-asset-references.md).
