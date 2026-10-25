# Brief agent cho /na-combo

Version: 1.2 | Updated: 2026-10-25 | v1.0 rút từ lượt combo 100 bộ (UW-0014–0035): phân việc theo loài, bài học lọc theo loài/task, reviewer giữ qua các vòng. v1.2: phân bổ + lên ý tưởng theo loài (2 ứng viên/suất, agent chọn ý độc lập) trước khi viết, reviewer theo nhóm loài, QA 2 mức, kiểm hình học bằng script, agent ảnh đọc mục 1/2/7.

Orchestrator sao brief tương ứng vào `.nature-studio/combo/drafts/<RUN>/`, điền tham số trong `<…>` rồi giao cho agent bằng đường dẫn file. Brief chỉ chốt tham số của lượt; skill /na-chayvideo, /na-taoanh và quy chuẩn vẫn là nguồn quyền. Mọi agent trả lời ngắn (mỗi bộ 1 dòng), phần chi tiết nằm trong file.

## Nguyên tắc ngữ cảnh (mọi agent)

- **Đọc một loài một lần, làm nhiều bộ.** Một agent chỉ chạm một loài chính và làm mọi bộ của nhóm mình trên cùng lần đọc nguồn. Không nạp hồ sơ loài, module câu, hồ sơ vùng hay ảnh mẫu của loài khác. Loài phụ trong cảnh (con mồi, chim) được tra đúng phần cần thiết.
- **Nhóm tối đa 5 bộ/agent** cho writer, reviewer và agent ảnh: đọc dữ liệu loài một lần rồi viết các bộ khác nhau và khác lịch sử; trần 5 để context chưa dài tới mức bộ sau kém hoặc na ná bộ trước. Loài có hơn 5 bộ thì chia nhiều nhóm, dùng chung một danh sách ý tưởng.
- **Bài học lọc theo bộ:** `python scripts/memory_retrieval.py query <slug> --mode new --task <task> --entity <slug-loài> [--interaction natural|angling] --candidates --out <tmp>/lessons-<n>.json`, đọc mọi trang và mở bản gốc của kết quả. Không dùng `combo.py lessons` để dựng bảng (lệnh đó trả mọi bài, kể cả của loài khác); chỉ orchestrator dùng nó ở bước đồng bộ và chống trùng.
- **Độ mới đọc theo tầng:** `chayvideo_context.py history` + ledger/fingerprint + `MECHANISMS-*.md` của lượt. Chỉ mở bản gốc production/nháp khi cơ chế gần trùng (tối đa vài bản gần nhất), không mở toàn bộ.
- **File tạm riêng:** mọi `--out`, packet, query ghi vào `.nature-studio/combo/drafts/<RUN>/<agent>-tmp/`, không dùng scratchpad chung.

## Bước 0 — Phân bổ (orchestrator, không agent)

Lập `ALLOCATION.md`: N bộ chia theo loài và suất (Thường/Khám phá/Thử nghiệm) từ hướng chủ đề, `03-Projects/<slug>/species-priority.md` (điểm, mùa đang mở) và số bộ đã có mỗi loài (`chayvideo_context.py history`, chỉ metadata). Đa dạng loài/cơ chế là mặc định; không dồn quá nửa lượt vào một loài trừ khi người dùng chỉ định. Mỗi loài → nhóm ≤5 bộ; nhóm đầu của loài là **nhóm lập ý tưởng** cho cả loài.

## Bước 1 — Lên ý tưởng theo loài (writer nhóm đầu) + chọn ý độc lập

Sau khi đọc nguồn như mục Writer 1–3, writer nhóm đầu của mỗi loài viết `CONCEPTS-<loài>.md` với **gấp đôi số suất** của loài (k suất → 2k ý, mỗi suất ít nhất 2 ứng viên khác cơ chế), mỗi ý 3–5 dòng: suất, biến thể/giai đoạn + vùng/mùa, cơ chế nhân quả (trigger → hành động key → hệ quả), hook 0–3 s, key/payoff, dụng cụ/mồi (mã `EQP-*` nếu có câu), video/nháp gần nhất trong lịch sử và khác ở đâu, rủi ro dàn cảnh/nguồn. Chuẩn chất lượng như khi viết bộ: độ mới và độ hay theo creativity.md, sinh học/vật lý có nguồn. Trả một dòng rồi **dừng chờ** orchestrator.

**1b — Chọn ý (agent chấm ý tưởng độc lập, context mới, một agent cho cả lượt):** chỉ đọc các file CONCEPTS, `idea-ledger.md`, `MECHANISMS-*.md` các lượt trước, creativity.md và hồ sơ loài khi cần kiểm khả thi; không đọc nguồn sáng tạo khác hay lập luận của writer. Luật cứng: loại ý **cùng loài + cùng con mồi/hành vi chính hoặc cùng cấu hình mồi–vùng** với một video/nháp đã có, hoặc chỉ là bản đảo ngược của cơ chế đã có; loại ý trùng chéo giữa các loài trong lượt. Với ý còn lại chấm 1–5 độ mới, payoff, khả thi dàn cảnh cho model video, căn cứ nguồn; chọn mỗi suất một ý tổng điểm cao nhất (hòa thì ưu tiên payoff). Ghi `CONCEPTS-REVIEW.md` (chọn/loại kèm lý do một dòng). Suất không còn ý đạt luật cứng thì yêu cầu writer đề xuất thêm hai ý cho suất đó. Sau đó orchestrator nhắn writer tiếp tục (SendMessage) và giao concept cho nhóm còn lại của loài bằng đường dẫn file.

## Writer

Nhóm việc: các bộ **cùng một loài** trong lượt (tối đa 5 bộ/agent). Lượt có loài chỉ một bộ thì một agent một bộ.

1. Đọc skill /na-chayvideo, `new.md` và lõi chung một lần. Nguồn qua `chayvideo_context.py packet underwater --mode new --species <slug> --interaction <natural|angling|unspecified> --stage all --out <tmp>` rồi `view` (để `coverage` xác nhận); không đọc thẳng file nguồn. Có câu: packet kèm `baits` (mã mồi của loài); chỉ mở hồ sơ mồi đã chọn.
2. Hồ sơ loài bằng `species_profiles.py resolve`; hồ sơ vùng qua descriptor của đúng loài; thiếu vùng thì nghiên cứu và tạo hồ sơ vùng theo location-context.md.
3. Tham số lượt: Project, mùa/vùng ưu tiên, hướng chủ đề, suất, cơ chế đã có của lượt (đọc `MECHANISMS-*.md`), concept được giao (`CONCEPTS-<loài>.md` + `CONCEPTS-REVIEW.md`). Ghi ngay một dòng cơ chế vào `MECHANISMS-<agent>.md` khi khóa concept. Đổi concept đã duyệt thì ghi lý do, không âm thầm.
4. Mỗi bộ một thư mục nháp gồm `OUTPUT.json` (qua `chayvideo_output.py check`), `criteria.md` (B1–B8 + C1 độ mới + C2 độ hay + L* từ query bài học), `geometry.json` + `geometry.md`, `research.md`, `meta.json`. Chưa cấp mã.
5. **Hình học bằng số, kiểm bằng script:** ghi `geometry.json` (items: `name, t, x, y, z` số hoặc `[min, max]` mét, `heading`, `key` cho chủ thể key/payoff, `exits` khi chủ ý ra khung, `readable: false` khi chỉ là bóng mờ; `visibility_m`; `links` dây/leader `{a, b, max_m, label}`; `speeds` `{item, max_mps}`) cho mọi chủ thể/mốc/dụng cụ × mốc beat (t=0, hook, key, 10.0 s). Chạy `python scripts/combo_geometry.py render <bộ>/geometry.json` tới khi `ok: true`; script sinh `geometry.md`. Script chỉ kiểm số học (khung ≈ 0,63 × cự ly, tầm nước, độ dài dây, tốc độ); xuyên vật, dải mặt nước theo độ sâu/góc máy và tính hợp lý của cảnh vẫn do writer tự kiểm.
6. **Tự kiểm trước khi nộp:** viết câu vị trí trong FF/VP/frame_state **từ bảng**; sau mỗi lần sửa số, chạy lại script rồi rà meta, idea, caption và INPUTS. Âm nào cũng có vật phát trong cảnh. Hook ở 0–3 s không lộ key/kết cục, không gán ý muốn/cảm giác cho cá. Dây có tải căng thẳng tới điểm kéo.
7. Vòng sửa: đọc `review-r<N>.md`, sửa đúng lỗi, `check` + script hình học, ghi `qa-log.md` (lập luận của writer, reviewer không đọc) và `CHANGES-r<N>.md` (chỉ liệt kê file/trường/beat đã đổi, không lập luận) để reviewer khoanh vùng hồi quy. Khi orchestrator báo ĐẠT (hoặc hết 5 vòng): reserve mã, `save`, hồ sơ production, ledger, idea-bank, `COMBO-ROW-text.json`. Trả về mã ↔ nháp, qa_text và bài học ứng viên (hành động + phạm vi + căn cứ).

## Reviewer

Một reviewer cho **một nhóm writer** (cùng loài, ≤5 bộ), **giữ nguyên qua các vòng** (orchestrator nhắn tiếp bằng SendMessage). Reviewer độc lập với writer: chỉ nhận `criteria.md`, `OUTPUT.json`, `geometry.json`/`geometry.md`, `meta.json`, `research.md` của từng bộ và đường dẫn nguồn. Đọc nguồn một lần cho cả nhóm nhưng **chấm từng bộ riêng** theo bảng tiêu chí riêng của bộ đó, không so điểm giữa các bộ, không để kết luận của bộ này ảnh hưởng bộ khác.

- Nguồn: `chayvideo_context.py packet ... --stage review` của đúng loài (+ module câu nếu có dụng cụ), hồ sơ vùng trong meta, bài học có trong `criteria.md`. Web chỉ khi cần kiểm dữ kiện cụ thể.
- Độ mới theo tầng như trên.
- Hình học: chạy `combo_geometry.py check` thay vì tự cộng trừ; lỗi script là FAIL. Reviewer vẫn chấm phần script không thấy: xuyên vật, mặt nước, hướng, tính hợp lý, khớp giữa các file.
- Không đọc `qa-log.md`, `CONCEPTS-*.md` hay lập luận của writer; phần đã đổi lấy từ `CHANGES-r<N>.md` rồi đối chiếu chính file đầu ra (lượt thử AB 2026-10-25: reviewer mở qa-log khi cần tìm chỗ đổi).
- **QA 2 mức:** vòng 1–3 chấm đầy đủ mọi tiêu chí. Vòng 4–5 chỉ kiểm các lỗi còn mở và những phần đã đổi do sửa (rà hồi quy trên đoạn đổi, file liên quan và script hình học); không chấm lại tiêu chí đã PASS mà nội dung không đổi. Mọi vòng sau vòng 1 không đọc lại nguồn chưa đổi.
- Dung sai hình học: chỉ FAIL khi chủ thể/key/payoff ra khỏi khung hoặc tầm đọc, vật xuyên vật, vi phạm ràng buộc vật lý (độ dài dây, tốc độ, hướng) hoặc các file mâu thuẫn. Lệch nhỏ (≲10% khung, ≲15% cự ly) ghi `minor`.
- Ghi `review-r<N>.md` **trong thư mục từng bộ** (bảng Tiêu chí | Trạng thái | Quan sát | Cách sửa + `Overall`). Trả lời mỗi bộ đúng một dòng: `<bộ>: Overall: PASS` hoặc `<bộ>: Overall: FAIL — <≤20 từ>`.

## Agent ảnh

Nhóm việc: các mã **cùng loài** (tối đa 5 mã/agent), làm theo /na-taoanh. Đọc skill và first-frame.md/first-frame-qa.md một lần; hồ sơ loài chỉ đọc `python scripts/species_profiles.py section <loài> 1,2,7` (nhận dạng, cỡ, Checklist hình ảnh) trừ khi brief ảnh cần mục khác; hồ sơ vùng của mã đó; ảnh mẫu query đúng entity/role; mồi theo `bait_profiles.py for-species`. Bài học ảnh qua `memory_retrieval.py query --task image-generation --task image-review --entity <slug>`.

- Tuyến, budget 5 lượt, tên file `<Axx>/first-frame.png`, handoff theo skill. Không chạy `combo.py media/row/push`, không xóa ảnh.
- Mỗi mã ghi `COMBO-IMAGE.json` (`id, attempt, status, calls, qa_image, qa_notes`). Trả về bảng mã · trạng thái · lượt · attempt và bài học ứng viên.

## Orchestrator

- Bước 0 như trên; bước 1b giao cho agent chấm ý tưởng độc lập, orchestrator chỉ chuyển file; chia loài thành nhóm ≤5 trước khi giao; giữ ≤8 agent chạy cùng lúc để tránh chạm hạn mức; agent bị dừng giữa chừng thì nhắn tiếp (SendMessage), không tạo agent mới.
- Chuyển kết quả giữa agent bằng đường dẫn file, không chép nội dung review vào tin nhắn.
- Ghi `TRACKER.md`: mỗi bộ số vòng QA, vòng đạt, lỗi theo nhóm (hình học/sinh học/âm/hook/caption/khác) để đo hiệu quả giữa các lượt.
- Gom bài học ứng viên vào `LESSON-CANDIDATES.md` của lượt; cuối lượt mới chống trùng bằng `combo.py lessons` rồi `lesson-new`/`lesson-confirm`.
