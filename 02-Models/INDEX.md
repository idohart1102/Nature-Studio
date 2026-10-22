# Model và công cụ

- [Omni Flash](model-profiles/omni-flash.md): model người dùng chỉ định, chưa kiểm khả năng/giao diện trong lần khởi tạo.

Mỗi profile cần provider/model ID, interface, ngày kiểm, nguồn, điều đã test, điều chỉ được mô tả và giới hạn chưa biết. Không dùng yêu cầu 10s/9:16 làm bằng chứng giao diện thật có hỗ trợ.

- [Sunburst qua image_gen](model-profiles/sunburst-imagegen.md): model yêu cầu cho /na-taoanh; ưu tiên Sunburst nếu chọn được; nếu không có selector thì dùng model mặc định không hỏi lại, ghi backend unknown khi không được công bố. Danh tính model không chặn QA.
