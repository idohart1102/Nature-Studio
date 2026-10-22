# EV-REVIEW-01 — Phát hiện hook 3 giây đầu không đạt

Status: not run
Created: 2026-10-23
Level: video-reviewed
Skill: /danhgia v1.0
Input: Render Underwater 10s, frame đầu chỉ có nước và cỏ, mồi lộ ở 3.6s; `checks.hook_signal`=1.5, key onset thật 6.2s.
Expected: Hook fail kèm timecode (đối tượng không đọc được ở frame đầu, tín hiệu đầu 3.6s > 3.0s); key pass; đề xuất /chayvideo revision sửa first frame và beat đầu; không tự sửa prompt.
Fail cases: Chấm pass vì checks ghi 1.5; chấm từ prompt; tự viết lại prompt.
Actual output: chưa có
Result: not checked
Evidence: chưa có
