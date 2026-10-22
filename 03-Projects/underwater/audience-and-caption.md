# Khán giả và giọng — v1.9

Updated: 2026-10-22 | Origin: approved guide v1.9 + /na-chayvideo

**Chế độ skill /na-chayvideo (kể cả nhận diện theo đặc trưng):** theo [output-contract.md](output-contract.md), mặc định ba lựa chọn Chuẩn/Hài hước/Tò mò, tiếng Anh Mỹ tự nhiên cho người câu cá Mỹ; mỗi caption một đoạn có 3–5 hashtag đúng cảnh, kèm lược dịch caption rồi hook text và lược dịch hook; ý tưởng tiếng Việt, FIRST FRAME PROMPT và VIDEO PROMPT tiếng Anh, mỗi prompt một đoạn. Yêu cầu mới này thay ngoại lệ caption tiếng Việt ở v1.1. Các tiêu chí giọng/cấu trúc bên dưới tiếp tục áp dụng. Lý do: điều chỉnh người dùng 2026-10-16.

Khán giả Mỹ thích câu cá; ngôn ngữ đầu ra tiếng Anh Mỹ, gợi tò mò bằng chi tiết thật trong clip. Không tự nhận giọng native bảo đảm performance.

### Mỗi lựa chọn: caption đăng tải hoàn chỉnh có 3–5 hashtag

**Phong cách đã chốt — UF-D015:** học cách viết Underfishing qua benchmark 40 caption: ít chữ, trực tiếp, như một người câu cá phản ứng hoặc trao đổi ngay khi nhìn footage. Caption chọn **một chi tiết/hành động/phán đoán đáng chú ý**, không tóm tắt toàn bộ kịch bản hoặc viết lời quảng cáo. Dùng câu chữ nguyên bản và tiếng Anh Mỹ tự nhiên; học cơ chế giao tiếp, không chép caption, lỗi ngữ pháp hay jargon không đúng cảnh.

**Độ dài:** ưu tiên một câu hoặc cụm ngắn, thường 1–8 từ trước hashtag; 1–2 từ được phép khi hình đủ ngữ cảnh, dài hơn khi câu hỏi/chi tiết cần để tự nhiên và rõ nghĩa. Đây là ưu tiên biên tập, không quota hoặc giới hạn cứng. Không cố kéo câu ngắn thành 3 từ, không rút câu dài làm mất ý, không bắt chước caption chỉ có dấu hỏi vì thiếu ý tưởng.

**Kiểu viết:** linh hoạt câu hỏi, nhận xét, phản ứng ngắn, lời chỉ dẫn quan sát hoặc mời đánh giá một lựa chọn cụ thể. Chọn theo footage, không ép mọi caption là câu hỏi, không đặt tỷ lệ và không quay vòng các nhóm như danh mục đóng. Tò mò có thể đến từ vì sao, lúc nào, vật gì, quyết định nào hoặc điều bất ngờ; có thể nhắc kết quả đã thấy để người xem xem xét nguyên nhân, không bắt buộc giấu kết cục. Giọng gần gũi, ít lời, không hô hào “watch till the end”, không câu tương tác rỗng bằng “Comment YES”/tag bạn bè.

**Đúng cảnh và đúng khán giả:** không ép mọi video vào cú hụt/thoát móc/tranh mồi. Cá săn mồi tự nhiên không cần rig/lure; chỉ dùng *follow, short strike, commit, spit the bait, hookset, rig, lure, jig* khi hình hỗ trợ và đúng cách nói người câu cá Mỹ. Phân biệt bait/lure, tiếp cận/ăn/mắc câu; không tuyên bố hooked/caught/swallowed khi chưa thấy. Không nhập thuật ngữ carp như chod/boilies/tigers chỉ để giống đối thủ. Ở giai đoạn prompt, bám concept dự kiến và kiểm lại theo video thật; không coi concept là bằng chứng đã diễn ra.

**Trước khi giao:** xem caption có chọn đúng một điểm đáng xem, nghe như câu nói tự nhiên và có lặp cách mở/cấu trúc trong lịch sử Project không; sửa câu gượng hoặc chung chung. Ví dụ tự viết: `Not buying that lure.` khi cá thể hiện từ chối lure; `Watch that last-second turn.` khi có cú quay cuối rõ; `Would you change the retrieve?` khi footage có retrieve phù hợp. Đây là ví dụ có điều kiện, không phải khuôn phải lặp hoặc kết luận hiệu quả.

**Cấu trúc một caption đăng tải:** câu mở ngắn + một dấu cách + **3–5 hashtag khác nhau**, tất cả **viết liền thành một đoạn văn duy nhất, không xuống dòng trước hashtag, không tách hashtag thành dòng/đoạn riêng**. Ví dụ định dạng (setting Leech Lake): `What made him turn off? #Muskie #MuskyFishing #FreshwaterFishing #LeechLake`. Đây là **một trường caption** có thể sao chép đăng ngay; giao diện tự ngắt dòng theo chiều rộng màn hình không phải ký tự xuống dòng do AI chèn. **Không nhắc AI, việc tạo/sinh/mô phỏng video hoặc bất kỳ công nghệ tạo nội dung nào trong caption; không thêm dòng giải thích nguồn tạo. Không dùng hashtag về AI.** Tập trung hoàn toàn vào loài vật, hành động, câu hỏi và cảm giác tò mò như phong cách kênh tham chiếu. Không cần nhét địa danh vào câu hook nếu làm nó dài và gượng.

**Chọn hashtag — UF-D016:** không dùng `#Underwater` (không phân biệt hoa/thường); không biến tên Project thành tag mặc định. Giữ 3–5 tag khác đúng cảnh, không dùng biến thể chữ hoa/thường của tag đã loại để lách quy tắc. Ưu tiên một tag loài chính, một tag ngữ cảnh câu cá hợp loài, rồi tag phương pháp hoặc môi trường phù hợp; bộ mới/reference đã khóa setting có **đúng một tag địa điểm** trong tổng 3–5 theo [UF-D023](#hashtag-địa-điểm--uf-d023-2026-10-19), legacy/caption-only chưa có setting theo nhánh legacy ở mục đó. Không gắn cả ba loài nếu chỉ có một loài; không dùng một chuỗi tag cố định sai nội dung; không nhồi `#viral #fyp #trending`; loại mọi hashtag về AI hoặc công nghệ tạo video. Ví dụ nhóm hợp ngữ cảnh, tag địa điểm đổi theo vùng đã khóa: Redfish — `#Redfish #InshoreFishing #SaltwaterFishing #MosquitoLagoon`; Muskie — `#Muskie #MuskyFishing #FreshwaterFishing #LeechLake`; Walleye — `#Walleye #WalleyeFishing #FreshwaterFishing #LakeErie`.

**Quy tắc đầu ra:** gọi mục này là **CAPTION**, không phải TITLE. Mỗi bản có chuỗi caption EN gồm cả hashtag, không xuống dòng trong chuỗi và không trường hashtags riêng; hook_text riêng không thay câu mở caption. Bản ghi caption gốc giữ một chuỗi tương thích; ba lựa chọn và lược dịch nằm ở caption_variants theo contract. Caption/hook không phải lời thoại hoặc chữ phải tự vẽ vào video. Các con số 3–5 hashtag là yêu cầu biên tập của dự án mới, không phải nhận định rằng đối thủ dùng hashtag hoặc quy tắc bảo đảm reach.

## Ba lựa chọn và giọng người câu cá Mỹ — 2026-10-18

Mặc định **Chuẩn → Hài hước → Tò mò**, mỗi bản trả theo đúng thứ tự:

1. Caption: tiếng Anh Mỹ + 3–5 hashtag, sao chép đăng ngay.
2. Lược dịch caption: tiếng Việt tự nhiên, chỉ dịch ý phần câu; không dịch hashtag.
3. Hook text: tiếng Anh Mỹ, 1–9 từ, không hashtag.
4. Lược dịch hook: tiếng Việt giữ ý và sắc thái, không áp giới hạn từ tiếng Anh lên bản dịch.

**Viết Anh trước, dịch Việt sau.** Tưởng tượng một người Mỹ thích câu cá đang phản ứng hoặc nói chuyện về footage. Dùng cách nói thông dụng, contraction khi tự nhiên và đúng thuật ngữ cảnh; không viết tiếng Việt rồi chuyển từng chữ sang Anh, không nhồi slang/giọng địa phương để giả native. Đọc riêng phần Anh trước khi dịch; bỏ câu nghe như quảng cáo, lời thuyết minh giáo khoa, thành ngữ Việt được dịch sát hoặc lời đùa cố quá. Không tuyên bố native được chứng nhận hoặc chắc chắn giữ chân/viral từ kiểm văn bản.

- **Chuẩn (standard):** kế thừa giọng hiện tại: ít lời, một điểm đáng xem, nhận xét/phản ứng/câu hỏi đúng cảnh.
- **Hài hước (humor):** dí dỏm nhẹ từ tình huống, cách nói người câu cá Mỹ thực sự có thể dùng. Nhân hóa chỉ là câu đùa rõ nghĩa, không dùng để khẳng định sinh học/ý định/giới tính chưa biết. Không cố dựng một cú punchline hay slang cho mọi clip.
- **Tò mò (curiosity):** gợi chú ý chi tiết, quyết định hoặc nguyên nhân phù hợp clip; không hứa biến cố không có hoặc câu kéo “watch till the end”. Câu hỏi chỉ dùng khi tự nhiên.

Ba bản phải khác cách tiếp cận, không chỉ đổi dấu câu hoặc vài từ đồng nghĩa. Hook bổ trợ caption, không lặp nguyên câu; hướng người xem tới diễn biến/chi tiết có thật hoặc được chốt trong concept, ưu tiên điều thấy được trong 3 giây đầu (UF-D025). Không tự hứa “last second” nếu không có căn cứ thời điểm. Concept chỉ là dự kiến, phải đối chiếu lại khi có footage.

Hook dưới 10 từ là giới hạn cứng riêng; ưu tiên ngắn và tự nhiên, không kéo cho đủ 9 từ: helper đếm từ Anh gồm chữ/số, contractions như that's/don’t là một từ; từ nối bằng gạch nối/dash tính tách. Không nối bằng dấu gạch để lách hạn mức. Mọi bản vẫn giữ quy tắc hashtag/cảnh/khán giả bên trên; bộ tag có thể giống nhau khi đúng nội dung, không đổi tag chỉ để tạo khác biệt.

Chỉ được giao sửa một bản thì trả đúng bản đó và giữ các lựa chọn khác còn phù hợp với cùng clip. Khi chuyện thay đổi phải rà lại cả ba, không kế thừa caption cũ như đã đúng. Không thêm phương án chuyện/ảnh, không tra asset hay tạo media chỉ vì viết caption. QA bằng helper chỉ chứng nhận cấu trúc/đếm từ/tag; giọng Mỹ, humor và đúng footage phải tự đọc kiểm.

## Nghiên cứu tham chiếu — 2026-10-16

Phong cách đã duyệt ở trên là nguồn chạy mặc định. Mở báo cáo gốc khi nghiên cứu lại phong cách, cần ví dụ/đối chứng hoặc nguồn thay đổi; không bắt đọc lại mọi caption mỗi lần sửa một câu. Tham chiếu [benchmark 40 caption Underfishing](../../01-Knowledge/benchmarks/underfishing-captions-2026-10-16/REPORT.md). Nghiên cứu là quan sát, không chứng minh caption gây viral; phong cách được áp dụng theo **quyết định trực tiếp của người dùng UF-D015**, không phải tự nâng hypothesis thành active. Giữ **3–5 hashtag** dù mẫu đối thủ không thấy hashtag. Quyết định này cập nhật ưu tiên độ ngắn/kiểu câu; mọi giới hạn kỹ thuật video và ngôn ngữ vẫn giữ. Báo cáo nghiên cứu gốc giữ nguyên để truy vết các đề xuất trước quyết định.

## Hashtag địa điểm — UF-D023, 2026-10-19

Với bộ mới/reference đã khóa setting, mỗi bản Chuẩn/Hài hước/Tò mò có **đúng một hashtag địa điểm**, giống nhau giữa ba bản, nằm **trong tổng 3–5 tag** hiện hành. Dùng hashtag từ hồ sơ vùng đã chọn; tag phải đúng phạm vi, không thêm bang/thành phố/địa danh thứ hai. Các tag còn lại chọn loài/ngữ cảnh/phương pháp phù hợp; không cần thêm địa danh vào câu caption/hook nếu gượng. Ví dụ khi setting là Laguna Madre: `He spotted that shrimp. #Redfish #InshoreFishing #LagunaMadre` (chỉ dùng khi cảnh hỗ trợ hành động).

Caption-only đọc setting đã khóa từ INPUTS/frame_state và nguồn dẫn cần thiết. Nếu legacy chưa có địa điểm, không tự đoán hoặc gắn địa danh nổi tiếng: chỉ sửa chữ thì giữ phạm vi legacy và ghi thiếu setting trong hồ sơ; khi được giao bổ sung địa điểm thì xác minh tối thiểu và kiểm tương thích cảnh trước, không đổi prompt ngầm. Ví dụ cũ không có tag địa điểm chỉ minh họa giọng/định dạng hoặc legacy, không là ngoại lệ cho bộ mới đã khóa setting.

Tag là bối cảnh sáng tạo, không tự xác nhận footage được quay tại đó; không viết tuyên bố trải nghiệm/địa điểm quay thực tế khi chưa có bằng chứng. Không lấy sở thích câu cá làm điều kiện thay phân bố/sinh cảnh. Các quy tắc native US, lược dịch, hook 1–9 từ, không AI/#Underwater và không spam vẫn áp dụng. Helper hiện kiểm tổng tag và cấu trúc; AI phải kiểm bằng nghĩa đúng một tag địa điểm và khớp setting.
