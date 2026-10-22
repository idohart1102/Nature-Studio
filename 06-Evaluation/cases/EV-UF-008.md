# EV-UF-008 — Hook 3 giây đầu không đưa key lên sớm

Status: not run
Created: 2026-10-22
Level: prompt-only, sau đó render
Input: Bộ mới Walleye ở hồ đá, jig-and-minnow, key là cú đớp hụt rồi quay lại ăn.
Expected: Frame đầu thấy rõ jig-and-minnow gần camera và đang chuyển động theo lực kéo; trước 3.0s có một tín hiệu mới (bóng walleye lộ ở mép đá) nhưng không tấn công; `checks.hook_signal` ≤3.0, beat đầu kết thúc ≤3.0s, 5–10 beat; key onset >5.0s; caption/hook_text bám điều thấy trong 3 giây đầu. Trên render: chuyển động của cảnh và âm có từ 0.0s.
Fail cases: mở bằng cú đớp; frame đầu tĩnh hoặc đối tượng quá nhỏ; tín hiệu đầu ở 4s; hook_text hứa điều không có trong hình.
Actual output: chưa có
Result: not checked
Evidence: chưa có
