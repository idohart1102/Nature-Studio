---
name: na-combo
description: Chạy trọn một lượt sản xuất Nature Studio khi gọi /na-combo — N bộ nội dung qua /na-chayvideo (QA tối đa 5 vòng bằng reviewer độc lập), first frame qua /na-taoanh, upload Drive, ghi sheet cố định (tab 50 mã video + tab Bài học), xóa ảnh local và tổng kết bài học. Mọi kết quả phải qua bảng bài học. Không kích hoạt từ câu hỏi, trích dẫn hoặc sửa skill.
---

# /na-combo

Version: 1.2 | Updated: 2026-10-25 | UF-D026; v1.1: phân việc theo loài, bài học lọc theo loài/task, reviewer giữ qua vòng; v1.2: phân bổ + lên ý tưởng theo loài, reviewer theo nhóm loài, QA 2 mức, kiểm hình học bằng script

Quy ước trong chat. Workspace gốc đi lên ba cấp từ thư mục skill. Tổng kết tiếng Việt. Skill này **điều phối**: nội dung theo [/na-chayvideo](../na-chayvideo/SKILL.md), ảnh theo [/na-taoanh](../na-taoanh/SKILL.md), bài học theo [memory-policy v2.2](../../../00-Standards/memory-policy.md#kênh-duyệt-sheet-và-bài-học-làm-cổng-qa--v22-2026-10-25); không chép lại hay nới lỏng quy tắc của chúng. Không render video, đăng bài, commit hoặc push.

## Tham số lượt chạy

Đọc từ lời gọi: Project (tự nhận theo metadata như /na-chayvideo), số bộ N, **hướng chủ đề** (ví dụ câu bằng mồi, săn mồi tự nhiên, một loài/vùng; không có thì AI tự chọn đa dạng trong phạm vi Project), cách chọn loài (chỉ định/ngẫu nhiên). Thiếu thông tin thật sự quyết định thì hỏi một lần; còn lại dùng mặc định: QA văn bản tối đa 5 vòng, ảnh tối đa 5 lượt/ảnh, ảnh mẫu khi phù hợp, upload rồi xóa ảnh local. Hướng chủ đề là của lượt này, không thành mặc định Project.

## 0. Chuẩn bị (không tốn lượt)

- `python scripts/combo.py init ...` chỉ khi chưa có `.nature-studio/combo/config.json` (Project, prefix, remote rclone, folder Drive, tên sheet, `--sheet-file-id` nếu đã có). Sheet và folder **cố định**; không tạo sheet mới mỗi lượt.
- `python scripts/image_9router.py check` khi môi trường không có image_gen; `rclone lsf <remote>: --drive-root-folder-id <folder>` để chắc Drive ghi được. Hỏng thì báo và dừng trước khi tiêu lượt.

## 1. Đồng bộ bài học đầu lượt — bắt buộc trước mọi kết quả

1. `python scripts/combo.py pull`: tải sheet, so với lần đẩy trước để biết đúng ô người dùng đã sửa; lưu snapshot + biên nhận `approvals/`.
2. `python scripts/combo.py apply-user`: áp trạng thái/nội dung/ý kiến người dùng vào 05-Memory (Đã duyệt = kích hoạt user chính thức).
3. Dòng bài học người dùng tự thêm (`new_lessons`): so nghĩa với **mọi** bài (`combo.py lessons`, kể cả retired) theo hành động + phạm vi. Trùng → `lesson-confirm` và ghi chú; mới → `lesson-new` với `author: "Bạn"`, giữ trạng thái người dùng chọn (để trống = Đã duyệt vì người dùng chủ động thêm), evidence là biên nhận approvals.
4. Đọc `video_feedback` (Bạn chấm Dùng/Sửa/Bỏ + ghi chú) của các lượt trước làm phản hồi biên tập cho độ hay.
5. Dựng **bảng bài học theo từng bộ**, không dùng chung một bảng cho cả lượt: `memory_retrieval.py query <slug> --task <task> --entity <loài> [--interaction ...] --candidates`, đọc mọi trang và mở bản gốc kết quả; mỗi bài ghi loại (Ràng buộc/Định hướng sáng tạo), trạng thái và cách kiểm. `combo.py lessons` (trả mọi bài, kể cả của loài khác) chỉ dùng cho đồng bộ ở bước này và chống trùng ở bước 5.

## Phân việc và ngữ cảnh — v1.2

Giao việc cho agent theo [brief chuẩn](references/agent-briefs.md). Nguyên tắc: **đọc dữ liệu một loài một lần, làm nhiều bộ**; chất lượng mỗi bộ giữ nguyên chuẩn và quy trình kiểm như trước.

- **Bước 0 — phân bổ:** orchestrator chia N bộ theo loài/suất (`ALLOCATION.md`), mỗi loài thành nhóm ≤5 bộ.
- **Bước 1 — lên ý tưởng theo loài:** writer nhóm đầu của mỗi loài đọc nguồn một lần, viết `CONCEPTS-<loài>.md` với gấp đôi số suất rồi dừng; một agent chấm ý tưởng độc lập (chỉ đọc concept + ledger) loại ý gần trùng lịch sử/chéo loài và chọn mỗi suất ý tốt nhất (`CONCEPTS-REVIEW.md`) trước khi viết bộ đầy đủ.
- Writer/agent ảnh chỉ làm các bộ **cùng một loài** (tối đa 5); packet dựng bằng `--species <loài>` và `--interaction` đúng bộ. Agent ảnh đọc hồ sơ loài qua `species_profiles.py section <loài> 1,2,7`.
- **Hình học:** writer ghi `geometry.json`, `scripts/combo_geometry.py render` kiểm số học (khung, tầm nước, độ dài dây, tốc độ) và sinh `geometry.md`; reviewer dùng script thay cho tự tính.
- **Reviewer theo nhóm:** một reviewer độc lập cho một nhóm writer (≤5 bộ cùng loài), giữ qua các vòng; đọc nguồn một lần nhưng chấm và ghi review riêng từng bộ. **QA 2 mức:** vòng 1–3 đầy đủ, vòng 4–5 chỉ lỗi còn mở và phần đã đổi.
- Độ mới đọc theo tầng: history + ledger/fingerprint + `MECHANISMS-*.md`; chỉ mở bản gốc các bộ gần trùng.
- ≤8 agent chạy cùng lúc; agent dừng giữa chừng thì nhắn tiếp, không tạo agent mới. File tạm của mỗi agent ở thư mục riêng trong `.nature-studio/combo/drafts/<RUN>/`. `TRACKER.md` ghi số vòng và nhóm lỗi từng bộ để so hiệu quả giữa các lượt.

## 2. Nội dung — /na-chayvideo

Chạy đúng skill /na-chayvideo cho N bộ (preflight, đọc đủ nguồn, rà lịch sử, idea-bank, suất Khám phá/Thử nghiệm theo creativity.md, nghiên cứu loài/vùng/dụng cụ, helper check). QA tối đa 5 vòng bằng reviewer độc lập theo bảng bài học + độ mới + độ hay; nhiều bộ có thể review song song, mỗi bộ bảng tiêu chí riêng. Chỉ cấp mã và `save` bộ đã đạt hoặc đã hết 5 vòng (ghi CHƯA ĐẠT). Ghi INPUTS: bài học applied/not_applicable/trial, suất, số vòng QA.

## 3. First frame — /na-taoanh

Theo đúng /na-taoanh: budget 5 lượt/ảnh, ảnh mẫu thư viện từ lượt đầu khi phù hợp, QA ảnh theo first-frame.md + Project + bài học task ảnh, handoff cho ảnh đạt. Các ảnh độc lập có thể chạy song song. Hết 5 lượt chưa đạt: không gọi lượt 6, giữ bản tốt nhất ghi CHƯA ĐẠT và đề xuất số lượt thêm ở báo cáo cuối; không chặn các ảnh khác.

## 4. Bàn giao Drive + sheet

1. `python scripts/combo.py media <items.json>` (mỗi mục `{id, attempt, status, calls}`): upload ảnh tốt nhất của từng video, `rclone check`, ghi `media.json` + `MEDIA-LOCATION.md`, rồi **xóa mọi ảnh sinh ra trong production**. Hồ sơ văn bản, hash, review, handoff giữ lại.
2. `python scripts/combo.py row <ID> <fields.json>` cho từng video: `date`, `slot`, `species`, `setting`, `direction`, `gear`, `qa_text` (ví dụ `ĐẠT (vòng 2/5)` hoặc `CHƯA ĐẠT (5/5): ...`), `qa_image`, `qa_notes`, `lessons_applied`. Ý tưởng, prompt, caption, mốc giây và link ảnh được lấy tự động từ hồ sơ.
3. `python scripts/combo.py push`: dựng lại sheet: tab theo khối 50 mã (`UW-0001 – UW-0050`, `UW-0051 – UW-0100`...) gồm mọi video của Project, cột Bạn chấm/Ghi chú giữ nguyên; dòng có `CHƯA ĐẠT` tự tô đỏ; tab **Bài học** có ô chọn trạng thái (Đã duyệt/Chờ duyệt/Không duyệt/Ngừng áp dụng) và loại, Chờ duyệt tô vàng. Upload đè giữ nguyên ID sheet; ID đổi thì dừng và báo.

## 5. Tổng kết bài học cuối lượt

Theo quy trình /na-dongvideo cho phạm vi lượt combo: gom lỗi từ các vòng QA văn bản/ảnh, cách sửa đã hiệu quả và phản hồi người dùng; tách quan sát một lần (ở lại production) khỏi bài học tái dùng. Với mỗi bài học ứng viên:

- So trùng với mọi bài; trùng → `lesson-confirm --source <ID>`; khác → `lesson-new` (loại, nhóm, áp dụng cho, hành động cụ thể, căn cứ, video nguồn).
- Trạng thái: **Đã duyệt** chỉ khi đủ gate AI tự duyệt của memory-policy v2.2 (Ràng buộc, bằng chứng khách quan lặp lại hoặc nguồn chính thức, có record 06-Evaluation/results); còn lại **Chờ duyệt**. Định hướng sáng tạo luôn Chờ duyệt.
- Ghi tiền đề tốt chưa dùng vào idea-bank. Chạy `python scripts/validate_memory.py`, rồi `combo.py push` lần cuối để tab Bài học khớp.

## Báo cáo

Trả link sheet + folder, bảng ngắn mã/loài/cơ chế/kết quả, số vòng QA và lượt ảnh đã dùng, các video CHƯA ĐẠT kèm đề xuất số lượt thêm (chờ người dùng đồng ý thật mới `grant`), bài học mới/xác nhận lại và bài đang Chờ duyệt để người dùng duyệt trong sheet. Nêu giới hạn: model ảnh chưa xác minh, QA là AI QA, chưa có render/số liệu đăng.
