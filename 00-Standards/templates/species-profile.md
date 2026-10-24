# <Common name>

```json
{
 "id": "<ID>",
 "slug": "<slug>",
 "scientific_name": "<Scientific name>",
 "taxonomy": {"authority": "unknown", "order": "unknown", "family": "unknown", "checked_with": "S1"},
 "common_names": {"en": ["<Common name>"]},
 "group": "<group>",
 "stages": ["adult"],
 "look_alikes": [],
 "modules": {},
 "status": "draft",
 "version": "1.0",
 "updated": "<YYYY-MM-DD>",
 "review_due": "<YYYY-MM-DD>",
 "sources_file": "01-Knowledge/sources/species/<slug>.md"
}
```

Chuẩn: [species-profile-standard](../../00-Standards/species-profile-standard.md). Nguồn: [sổ nguồn](../sources/species/<slug>.md). Dữ kiện ghi mã nguồn `[S1]`; giả định dàn cảnh không ghi mã nguồn.

## 1. Nhận dạng

Dấu nhận dạng chắc chắn, biến thiên thật (màu, hoa văn, giới tính, vùng) và bảng loài dễ nhầm: dấu phân biệt → lỗi hình hay gặp. [S1]

## 2. Kích cỡ và giai đoạn

| Thông số | Giá trị | Đơn vị | Phạm vi | Loại | Nguồn |
|---|---|---|---|---|---|
| Tổng chiều dài | unknown | cm | adult | typical | S1 |

Loại chỉ dùng `typical`, `large`, `record`, `estimate`. Không suy chiều dài từ cân nặng; cực trị không là cỡ mặc định. Ghi stage nào có trong `stages` và dấu hiệu nhìn thấy của từng stage.

## 3. Sinh cảnh và phân bố

Môi trường, độ sâu/độ mặn/nhiệt độ khi có nguồn; khác biệt theo stage; trỏ tới descriptor vùng nếu có. [S1]

## 4. Hành vi

Mỗi hành vi kèm điều kiện (mùa, giờ, stage, môi trường) và nguồn. [S1]

## 5. Tương tác

Con mồi theo stage, kẻ săn, phản ứng với con người/vật thể. Thông số dụng cụ đặt trong module, không chép vào đây.

## 6. Điểm đáng xem

| Đặc điểm có căn cứ | Hướng phát triển, không là kịch bản mặc định |
|---|---|

## 7. Checklist hình ảnh

- Dấu nhận dạng bắt buộc phải thấy.
- Lỗi lẫn loài cần chặn.
- Tỷ lệ/anatomy dễ sai.

## 8. Chưa biết và giới hạn

Điều chưa có nguồn, nguồn chỉ đọc qua index, số liệu chưa kiểm lại; ref ảnh còn thiếu theo stage/role.
