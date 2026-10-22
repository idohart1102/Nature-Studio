# Kiểm media thực và hậu kỳ mức âm

Version: 1.1 | Updated: 2026-10-22 | Nature Studio v2.2.0

## Kiểm khả năng trước khi nhận mẫu

`python scripts/media_review.py capabilities` phát hiện executable local, không chứng nhận AI hiểu video/âm. Đối chiếu thêm công cụ thực sự có trong phiên: video liên tục, nghe âm môi trường, frame, metadata, ASR là các khả năng riêng. Báo phần thiếu ngay trước phân tích. File upload không tự mở khả năng mới. Với adapter thật, ghi tên phương pháp, khoảng thời gian đã tiếp cận và evidence. Không tự cài dịch vụ, truyền media sang nhà cung cấp khác hoặc tiêu tiền. Chỉ frame/ASR thì partial; nhận draft có giới hạn cần chấp thuận như clonevideo hiện hành.

## Đo file, không suy từ prompt

```text
python scripts/media_review.py inspect <file> --expected-duration 10 --target-lufs -16 --peak-dbtp -1
python scripts/media_review.py aspect 941 1672
```

Các số âm ở ví dụ là mục tiêu một brief, không phải mặc định toàn hệ thống. Bỏ cờ target nếu brief chưa có. Helper chỉ đọc: hash nguồn, stream duration, container duration, raster, LUFS-I/true peak toàn âm và các cửa sổ đầu–giữa–cuối tối đa 3s. Kết quả JSON chứa đường dẫn riêng, chỉ lưu vào production hoặc `.nature-studio`, không vào repo public. Với clip ngắn, cửa sổ có thể chồng nhau; loudness cửa sổ không phải phép đo toàn bộ dynamics.

Thời lượng video lấy từ stream; đuôi audio/container không làm video 8s đạt yêu cầu 10s. Thiếu stream duration ghi not_checked; có thể kiểm timestamp/frame thực để bổ sung. Dung sai là tối đa 0.05s hoặc một frame theo FPS, phải ghi rõ khi nguồn VFR/metadata không tin cậy. Raster chỉ là pixel mã hóa: kiểm rotation, SAR/DAR và ảnh hiển thị trước chốt tỷ lệ. Actual model/interface giữ unknown nếu không có generation/settings evidence; tên file và prompt không chứng minh backend hoặc thông số thật.

Meter không nghe được texture, noise, nguồn âm hay sync. Silent/unmeasurable, không có audio, peak vượt, mức lệch và đã trong mục tiêu được phân biệt; noise vẫn not_checked cho đến khi nghe thực. So cả head/middle/tail với ý định âm trong brief, không tự coi cảnh cố ý yên lặng là lỗi. Nếu nhiều audio stream, chọn rõ stream trước xử lý; helper hiện đo/xử lý stream audio đầu tiên.

## Tuyến finishing khi được giao xử lý file

Sai mức mix nhưng hình đã dùng được: đề xuất chuẩn hóa âm thay vì tiếp tục render lại hình. Chỉ xử lý khi người dùng đã giao chỉnh media, có mục tiêu cụ thể và đã đánh giá nguồn/noise bằng nghe thực; thiếu khả năng nghe thì báo và xin phần đánh giá còn thiếu. File bằng chứng không tự cấp quyền. Không tăng gain cho nguồn mất/sai âm, noise chưa giải quyết hoặc tín hiệu silent.

```text
python scripts/media_review.py normalize <input.mp4> <new-v002.mp4> --target-lufs -16 --peak-dbtp -1 --authorization <local-approval.md> --listening-review <local-listening-review.md>
```

Helper đo pass 1, dùng measured parameters cho pass 2 của [FFmpeg loudnorm](https://ffmpeg.org/ffmpeg-filters.html#loudnorm), copy video, mã hóa audio đầu tiên AAC 48kHz và tạo sidecar before/after/hash. Không ghi đè file gốc/output cũ; không hứa giữ mọi stream/subtitle/metadata. Chỉ dùng tuyến này cho bản video phân phối có một audio stream; master đa track cần quy trình conform riêng. Đo lại peak sau AAC; output tạo xong không tự đạt mục tiêu hoặc được duyệt. Kiểm nghe lại noise, dynamics, clipping, đầu/giữa/đuôi, đồng bộ và duration trước giao. Lỗi giữa chừng giữ file chẩn đoán, lần sau dùng tên mới. Không tự chạy normalization trên video người dùng chỉ vì họ đồng ý nâng hệ thống.

## Mở đầu 3 giây

Khi Project có gate hook (Underwater UF-D025), xem 0–3s theo bước khoảng 0.1s: frame đầu tiên có chuyển động của cảnh, thời điểm tín hiệu mới thật, âm có từ 0.0s và không có biến cố quyết định sớm. Ghi vào QA miền hình/âm; không đạt thì ghi fail với lý do “hook 0–3s”. `checks.hook_signal` là dự định, không thay xem render.

## Phần chưa xuất hiện và trạng thái hiện hành

Ảnh t=0 chỉ kiểm phần nhìn thấy. Với bộ phận nhận dạng sẽ lộ sau, lập điểm kiểm lúc reveal và ending: mắt/mõm/hàm/vây/hoa văn đúng loài và liên tục. Không ép lộ toàn thân ở opening. Nếu có nguồn/quyền và giao diện hỗ trợ, có thể thử reference nhận dạng bổ sung đúng loài; chưa có thử nghiệm thì không hứa sửa được lỗi, không tự render/tăng budget.

Trong SUMMARY giữ riêng text hiện hành, render được chọn, nguồn prompt/ảnh thực đã dùng, QA từng miền và approval none/provisional/final. Current text mới không chứng minh render cũ đã dùng nó. Dùng resolver/hash hiện có và settings để xác minh actual inputs, giữ unknown nếu chưa biết. Có thể lưu `CURRENT-STATE.json` theo [mẫu](templates/current-state.json) và kiểm bằng `python scripts/production_state.py <production/CURRENT-STATE.json>`. Path/hash binding chỉ kiểm tính toàn vẹn, không chứng minh render sử dụng nguồn đó; lưu provenance actual inputs trong settings. Tạm duyệt không tự thành final hoặc QA pass; bản final có thể còn QA fail và phải báo rõ. Không backfill hoặc sửa attempt lịch sử để giả trạng thái mới.

## CURRENT-STATE schema2 — v2.1.0

Dùng [mẫu hiện hành](templates/current-state.json); không backfill lịch sử. `current_text`, `first_frame`/handoff, `reviewed_render`, `selected_render` và `actual_inputs_evidence` là path/hash riêng. QA gắn reviewed_render; approval gắn selected_render. Có thể là hai file khác nhau, không coi newest là selected. `qa_evidence` trỏ báo cáo thật; `qa_coverage` theo miền có `status: complete|partial|not_checked` và `method` mô tả cách tiếp cận. Ví dụ `visual: {"status":"partial","method":"event frame samples"}`; frame sample không tự thành full continuous review. Từng miền pass/fail/not_checked/not_applicable phải đúng vật thực đã xem/nghe; helper chỉ kiểm khai báo/binding, không kiểm thay perception.

qa_pass chỉ ở schema2 khi state hợp lệ, mọi miền bắt buộc pass/not_applicable, có ít nhất một pass, reviewed_render và evidence/hash khớp, coverage miền pass đầy đủ. Partial có thể ghi tiến bộ nhưng không full QA pass. Schema1 vẫn đọc được và ghi unverified, không tự chứng nhận QA từ những cờ cũ. Null/kiểu sai trả errors. Approval none/provisional/final độc lập; schema2 cần approval_evidence path/hash khi provisional/final, agent đối chiếu lời người dùng thật. Hash không chứng minh authorship hoặc actual input; không tự nâng “có vẻ ổn” thành final.
