# Mã Project và video

Version: 2.0 | Updated: 2026-10-17 | Nature Studio v2.0.0

Video mới dùng `XX-YYYY`: hai chữ ASCII A–Z viết hoa và bốn chữ số ASCII từ **0001 đến 9999**. Ví dụ `AB-0001` chỉ minh họa, không là prefix mặc định. Prefix cấp riêng từng Project local; **UF dành riêng cho legacy**, không cấp mới. Có tối đa 675 prefix khả dụng trước các prefix đã dùng/nhập. UUID phân biệt danh tính giữa các workspace; mã ngắn không bảo đảm duy nhất toàn cầu.

Revision giữ mã và tạo attempt A01, A02… Hủy/xóa không giải phóng số. Đạt 9999 hoặc hết prefix thì dừng để quyết định mở rộng chuẩn, không quay vòng hay tự đổi prefix.

## Cấp mã

Đọc Slug và ID ổn định trong PROJECT.md; không suy từ tên hiển thị. Xem trạng thái bằng lệnh chỉ đọc, không tạo registry hoặc migration:

```text
python scripts/video_ids.py status underwater
```

Khi thực sự thiết lập Project hoặc chuẩn bị video mới:

```text
python scripts/video_ids.py init underwater
python scripts/video_ids.py reserve underwater
```

`init` không tạo video; tùy chọn `--prefix AB` chỉ nhận hai chữ chưa dùng, khác UF. Khi đã có namespace v2, init trả cấu hình hiện hành, cấm đổi prefix. `reserve` tự init nếu cần, commit số bằng transaction SQLite rồi tạo `04-Productions/<slug>/<video-id>/IDENTITY.json` schema2 với id_format, mã và UUID video/Project. Ghi file lỗi vẫn tiêu hao số đã commit; khoảng trống hợp lệ. Không reserve khi hỏi kiến thức, sửa skill, nâng hệ thống hoặc sửa/tổng kết video cũ. Không tự đoán mã bằng chat. Công cụ lỗi phải xử lý trước khi cấp mã.

Kiểm prefix trong registry, series lịch sử, videos, thư mục production, ledger và IDENTITY toàn workspace. Số tiếp theo vượt high-water registry/videos và mã cùng prefix đã quan sát. Nhiều phiên cùng local dùng chung registry. Dữ liệu identity hỏng phải sửa/khôi phục, không bỏ qua để cấp tiếp.

## Chuyển từ v1.x

Mã `XXX-YYYYY` và `UF-0001` giữ nguyên thư mục, identity, attempt, ledger và tham chiếu. Không rút ngắn mã cũ hoặc gán UUID giả. /na-chayvideo, /na-clonevideo, /na-dongvideo và /na-taoanh tiếp tục dùng lịch sử cũ.

Registry cũ chỉ chuyển khi **init/reserve thật**: lưu prefix/bộ đếm ba chữ vào bảng series, cấp namespace hai chữ bắt đầu 0001 và giữ nguyên Project UUID. Migration atomic; lỗi thì rollback. Không sửa các hàng video cũ. Registry v2 có guard chặn allocator cũ ghi sai định dạng. Không dùng script v1.x với registry đã chuyển; rollback phải khôi phục mã nguồn và backup registry tương ứng trong lúc không có phiên ghi, đồng thời bảo toàn mọi reservation/video phát sinh sau backup.

## Backup và gộp dữ liệu

`.nature-studio/video-ids.sqlite3` là dữ liệu local, không nằm trong Git/gói mẫu; luôn giữ khi nâng cấp. Di chuyển cùng Project phải sao lưu registry nhất quán (SQLite backup hoặc không có phiên ghi), production và ledger. Đổi tên Project không đổi ID/UUID/prefix.

Mất registry: khôi phục backup trước khi tiếp tục cùng danh tính; không nhận đã khôi phục UUID/bộ đếm từ tên thư mục. Project độc lập từ mẫu dùng ID Project mới, không chép registry/IDENTITY mẫu. Trước gộp hai workspace, so cả ID, UUID và mã; xử lý xung đột trước, không ghi đè hoặc đổi mã lịch sử tự động. Xem [UPDATE](../UPDATE.md).
