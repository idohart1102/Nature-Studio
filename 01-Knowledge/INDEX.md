# Chỉ mục kiến thức

Các hồ sơ ban đầu là inherited-reference từ hướng dẫn đã chốt. Ba hồ sơ loài đã được bổ sung nguồn văn bản ngày 2026-10-18; các tài liệu khác giữ trạng thái tại nguồn. Knowledge không là active lesson hoặc chứng nhận ảnh/video đã đúng.

| ID | Chủ đề / thẻ | File |
|---|---|---|
| Loài | Mọi nhóm sinh vật, chuẩn v3 | [Chỉ mục loài](species/INDEX.md) (sinh tự động) |
| K-HAB-UNDERWATER-001 | water, optics, habitat, sediment | [Môi trường dưới nước](habitats/underwater-realism.md) |
| K-EQP-US-ANGLING-001 | bait, lure, hook, line, rig, trap | [Dụng cụ Mỹ](equipment/us-angling-tackle.md) |
| K-INT-FISH-001 | predation, prey, lure, force | [Tương tác](interactions/fish-prey-and-lure.md) |

[Danh mục nguồn](sources/INDEX.md). Với loài/chủ đề mới, tạo hồ sơ có nguồn, không thay tên trong hồ sơ cũ. Chỉ mục có thể xây lại từ ID/thẻ trong file; không coi việc thiếu chỉ mục là thiếu dữ liệu.

## Benchmark đã nghiên cứu

- [K-BM-UF-CAP-20261016: 40 caption Underfishing](benchmarks/underfishing-captions-2026-10-16/REPORT.md): quan sát 2026-10-16, mẫu >1 triệu view hiển thị; không là bằng chứng nhân quả viral hoặc quy chuẩn đã kích hoạt.

## Profile phục vụ sáng tạo — v2.1.0

Ba hồ sơ trên đã được bổ sung văn bản có nguồn ngày 2026-10-18, giữ ID: ngoại hình, cỡ/biến thể, hành vi, điểm đáng xem, điều kiện và nguồn/asset. Nhãn researched-reference không là QA ảnh/video hoặc active lesson. Khả năng đặc biệt cần đúng scope; không coi một cỡ lớn là phổ biến. [Cách duy trì và tra asset](../00-Standards/knowledge-routing.md); [mẫu loài](../00-Standards/templates/species-profile.md).

## Vùng bối cảnh Mỹ — 2026-10-19

15 hồ sơ văn bản có nguồn chính thức, không phải ảnh đã QA: [Redfish](locations/redfish/INDEX.md), [Muskie](locations/muskie/INDEX.md), [Walleye](locations/walleye/INDEX.md). Tra descriptor đúng loài rồi đọc vùng được chọn theo [chuẩn địa điểm](../00-Standards/location-context.md); không nạp toàn bộ các vùng mỗi lượt.

## Hồ sơ loài v3 — 2026-10-25

Ba hồ sơ Redfish/Muskie/Walleye nâng lên v3.0 theo [chuẩn hồ sơ loài](../00-Standards/species-profile-standard.md), giữ ID: metadata JSON, bảng cỡ có Loại/Nguồn, Checklist hình ảnh, [sổ nguồn](sources/species/) có cấp A–E và trạng thái truy cập, module câu tách tại `equipment/species/`. Thêm loài bằng `scripts/species_profiles.py new`; tra tên bằng `resolve`, không đọc chỉ mục vào context.
