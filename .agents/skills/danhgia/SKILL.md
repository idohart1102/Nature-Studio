---
name: danhgia
description: Đánh giá video đã render và số liệu sau đăng của một production Nature Studio khi gọi /danhgia hoặc yêu cầu “đánh giá video”, “QA video”, “chấm video” kèm file hoặc mã video. Kiểm hình/âm thật theo chuẩn Project, ghi review và CURRENT-STATE; không sửa prompt, không tạo media, không đăng. Không kích hoạt khi chỉ hỏi, đánh giá prompt hoặc sửa skill.
---

# /danhgia

Version: 1.0 | Updated: 2026-10-23 | Skill chấm độc lập cho render và hiệu quả sau đăng

Gốc workspace chứa START-HERE.md, đi lên ba cấp từ thư mục skill. Đọc START-HERE.md, SYSTEM.md, [quality-review](../../../00-Standards/quality-review.md), [media-review-and-finishing](../../../00-Standards/media-review-and-finishing.md) và quy chuẩn Project được PROJECT.md dẫn tới. Với Underwater đọc `format.md` (Hook 3 giây đầu, key, âm thanh, kiểm trước giao), `first-frame-qa.md` và `audience-and-caption.md`. Báo cáo tiếng Việt.

## Vai trò độc lập

Skill này chỉ chấm, không viết. Đọc brief, `OUTPUT.json`/`checks` của attempt được render (`hook_signal`, `key_onset`, `location_tag`), FIRST-FRAME.json và settings để biết **dự định**; kết luận chỉ từ điều thực sự xem, nghe, đo trên file. Không dùng lập luận lúc viết prompt để biện hộ cho output, không hạ chuẩn vì prompt đã ghi đúng. Nếu chính phiên này vừa viết prompt của video, ghi rõ là tự chấm và đề nghị chạy /danhgia ở chat riêng.

## 1. Xác định đối tượng

- Cần mã video và file render (đường dẫn hoặc file đính kèm). Resolve Project/production bằng `python scripts/chayvideo_context.py projects` và hồ sơ thực; không chọn theo ngày file. Thiếu file thì xin file, không chấm từ prompt, thumbnail hay mô tả.
- Xác định attempt text mà render dùng từ settings/actual inputs; không biết thì ghi unknown, không giả render dùng bản mới nhất.
- Mức đánh giá: `video-reviewed` khi có file, `published-measured` khi có số liệu thực; có thể chỉ một trong hai.

## 2. Kiểm khả năng

Chạy `python scripts/media_review.py capabilities` và đối chiếu công cụ thật trong phiên: xem frame, xem chuyển động liên tục, nghe âm. Miền nào thiếu khả năng thì ghi `not_checked`, báo ngay và xin phần thiếu. Meter không thay nghe; frame rời không thay xem chuyển động liên tục.

## 3. Kiểm kỹ thuật

`python scripts/media_review.py inspect <file> --expected-duration <theo Project>`, thêm mục tiêu âm khi brief có. Ghi duration stream, raster/tỷ lệ, mức âm đầu–giữa–cuối, silent/clipping. Underwater: 10s theo dung sai helper, 9:16.

## 4. Kiểm nội dung

Trích frame vào thư mục review local của attempt, ví dụ:

```text
ffmpeg -i <file> -t 3 -vf fps=10 <review-dir>/hook_%03d.png
ffmpeg -ss <key_onset-1> -i <file> -t 2.5 -vf fps=20 <review-dir>/key_%03d.png
ffmpeg -i <file> -vf fps=2 <review-dir>/all_%03d.png
```

Mở frame thật để xem; nếu phiên xem được video liên tục thì xem thêm. Chấm theo thứ tự:

1. **Hook 3 giây đầu** (khi Project có gate; Underwater UF-D025): đối tượng thu hút đọc được ở frame đầu; frame đầu tiên có chuyển động của cảnh; thời điểm tín hiệu mới thật so với `checks.hook_signal`; không có biến cố quyết định sớm; có âm từ 0.0s.
2. **Key:** frame đầu tiên của hành động key thật so với `checks.key_onset`; Underwater phải >5.0s; hậu quả còn đọc được trước hết clip.
3. **Loài và giải phẫu:** t=0 khớp first frame; lúc reveal và ending kiểm mắt/mõm/hàm/vây/hoa văn liên tục.
4. **Chuyển động, vật lý, dụng cụ:** đường đi liên tục, không teleport/xuyên vật/biến hình; rig/dây/móc nhất quán; bùn/cỏ đổi trạng thái có nguyên nhân; camera đúng format.
5. **Âm:** nghe thật nếu có khả năng: môi trường và hành động liên tục, đồng bộ, key có điểm nhấn, không clipping/rè.
6. **Caption và hook_text:** khớp điều thấy được, nhất là 3 giây đầu và kết cục; không hứa điều không có.

Mỗi phát hiện ghi theo [mẫu review](../../../00-Standards/templates/review.md): ID → timecode/frame → quan sát → tiêu chí → pass/fail/not_checked/not_applicable → mức độ → nguyên nhân nghi ngờ → hướng sửa.

## 5. Ghi kết quả

- Lưu review mới cạnh render, không ghi đè review cũ; giữ frame trích làm bằng chứng local.
- Cập nhật CURRENT-STATE.json schema2 theo [mẫu](../../../00-Standards/templates/current-state.json): `reviewed_render` (path/hash), `qa` từng miền visual/motion/anatomy/audio/format, `qa_coverage` với status và method thực, `qa_evidence` trỏ review. Kiểm bằng `python scripts/production_state.py <production>/CURRENT-STATE.json`. Không đổi `approval` hay `selected_render`; QA pass không phải người dùng duyệt.
- Không đạt: liệt kê lỗi theo ưu tiên, chỉ ra phần cần sửa thuộc video prompt, first frame hay finishing; đề xuất /chayvideo revision, /taoanh hoặc chuẩn hóa âm. Không tự sửa prompt, render lại, tạo ảnh hay chuẩn hóa file.

## 6. Hiệu quả sau đăng

Khi người dùng đưa số liệu hoặc đã giao quyền truy cập:

- Ghi `performance.md` theo [mẫu](../../../00-Standards/templates/performance.md): nền tảng, URL, thời điểm đăng/đo, tuổi bài, định nghĩa chỉ số và nguồn. Underwater ưu tiên retention tại 3s, tại mốc ngay trước key, thời gian xem trung bình, lượt phát/replay nếu có. Thiếu thì `unavailable`, không điền 0. Không dùng lượt view để đánh giá hook.
- So với trung vị các video cùng Project có cùng định nghĩa chỉ số; nêu cỡ mẫu và nhiễu. Kết luận là giả thuyết, có thể đặt cạnh kết quả QA (ví dụ hook fail) nhưng không suy nhân quả từ một clip.
- Không tự đăng hoặc tự đo bằng tài khoản người dùng khi chưa được giao.

## 7. Báo cáo

Ngắn gọn: mức đánh giá, kết luận từng miền, lỗi chặn kèm timecode, phần not_checked và lý do, việc nên làm tiếp. Bài học tái sử dụng để /dongvideo xét; /danhgia không ghi Memory master hay tự active lesson. Frame, review và performance giữ local theo [publication](../../../00-Standards/publication.md). Không commit/push.
