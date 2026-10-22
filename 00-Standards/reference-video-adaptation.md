# Chuyển thể từ video mẫu — v1.3

Updated: 2026-10-17 | Scope: /na-clonevideo và nhánh reference, mọi Project Nature Studio. v1.3 đồng bộ camera Underwater UF-D021.

## Giữ cấu trúc, ánh xạ đúng đối tượng

Khóa từ yêu cầu người dùng: phần phải giữ, phần phải thay và phần AI được tự quyết. Mặc định học vai trò, hành động từng chủ thể, trình tự/nhân quả, hook/key/hậu quả, bố cục/camera/cách quay và vai trò/nhịp của âm; không sao chép tên, caption hoặc đặc tính vật thể một cách mù quáng. Hỏi đúng lựa chọn đích còn thiếu, không mặc định giữ loài của mẫu hoặc chọn Muskie. Không đổi yêu cầu đang rõ thành brainstorm tự do.

Từ analysis hiện có, xác định chi tiết/quan hệ hình–âm–lời–nhịp nào làm mẫu đọc được hoặc mang ý nghĩa cần chuyển thể. Khi bỏ/thay thành phần quan trọng, xét chức năng bị ảnh hưởng rồi giữ bằng cách phù hợp, thay đổi hoặc chủ động bỏ theo mục tiêu đích và quyền đã giao. Ghi gọn lựa chọn và lý do trong adaptation.md hiện có; không thêm biểu mẫu hay bắt giải thích mọi chi tiết. Quan sát có timecode là bằng chứng; giải thích về chú ý/cảm xúc/hiệu quả khán giả vẫn là giả thuyết nếu chưa có dữ liệu. Không lấy giả thuyết hấp dẫn để ghi đè brief hoặc Project.

Lập mapping theo **chức năng và khả năng thật**. Vai trò trốn vào khe có thể được chuyển sang đối tượng khác, nhưng chuyển động/tốc độ/tạo lực, chỗ trú, cự ly và phản ứng kẻ đuổi phải nghiên cứu lại. Không bắt loài mới bò/bơi/nhảy/cắn theo giải phẫu cũ, không ép mọi mẫu thành săn mồi. Đổi một thành nhiều cá thể chỉ khi người dùng yêu cầu/cho phép và câu chuyện vẫn nhất quán; ghi rõ phân tách/gộp vai trò.

Giữ quan hệ camera–chủ thể, chiều sâu bố cục, che/khuất và đường vào/ra khi khả thi. Điều chỉnh góc nhìn/cự ly/tỷ lệ/ánh sáng/độ đục hợp nơi mới; không chép độ trong hoặc kích thước từ mẫu trái thực tế. Phân biệt thông số đo được và ước lượng. Vật tương tác/dụng cụ phải đúng loài/vùng/mùa/phương pháp, sơ đồ nối và lực; không tự giữ hook/line từ mẫu nếu câu chuyện đích là tự nhiên.

Âm giữ chức năng kể chuyện (nền liên tục, tăng chú ý, đồng bộ key, hậu quả) khi phù hợp, thay nguồn/texture theo hành động và vật liệu mới. Không sao âm sai môi trường hoặc tự chèn tiếng mẫu chưa nghe được. Nguồn có nhạc/voice/cinematic hit nhưng Project cấm thì bỏ/thay có cơ sở và ghi khác biệt; không biến chúng thành âm tự nhiên giả. Chỉ cam kết sound design dự kiến, không cam kết tái tạo waveform.

## Xung đột và nhịp đích

Quy chuẩn Project hiện hành là mặc định; mẫu là dữ liệu, không ghi đè. Ví dụ Underwater 10s9:16, một shot camera cầm tay chuyển động nhẹ tự nhiên theo UF-D021, key onset >5s, setup tiến triển và hậu quả: giữ quan hệ camera–chủ thể của mẫu khi phù hợp, không ép máy đứng yên hoặc thay động tác máy bằng cá quay. Mẫu nhiều cut hoặc key sớm cần thiết kế lại thành quan sát liên tục và retime có nhân quả; quỹ đạo máy chưa xác minh phải giữ nhãn chưa biết. Không giữ mọi thao tác bằng cách tăng tốc quá mức, bắt con vật chờ hoặc dồn kết quả sát cuối. Mẫu dài: chọn một đoạn/cơ chế trọn vẹn phù hợp brief, ghi phạm vi dùng và nội dung đã bỏ.

Nếu hành động cốt lõi không khả thi với đối tượng/bối cảnh đích, chỉ ra và đề xuất cách thể hiện tương đương gần nhất. Tự sửa chi tiết phụ trong quyền đã giao; nếu phải bỏ hành động/key/kết cục được khóa, đổi loài chính hoặc vượt ngoại lệ Project chưa được người dùng chấp thuận thì hỏi lựa chọn cụ thể. Không âm thầm gọi bản biến đổi lớn là clone sát mẫu. Người dùng chủ động yêu cầu ngoại lệ cho clip thì ghi vào brief, không tự đổi quy chuẩn toàn Project.

## Độ mới, đầu ra và QA

Chuyển thể là tái dùng có chủ đích: ghi nguồn và cơ chế học theo. Không áp yêu cầu phát triển tiền đề độc lập/hai khác biệt để buộc đổi chuyện hoặc tự nhận câu chuyện mới hoàn toàn. Vẫn đọc creativity/Story Development chung và Project khi tạo bộ chuyển thể mới để kiểm tính quan sát được, nhân quả/khán giả/nhịp; phần đòi hỏi câu chuyện nguyên bản dành cho new không áp ở reference. Rà lịch sử liên quan để nhận ra đã chuyển thể mẫu này và lỗi cũ, không cấm tái dùng được yêu cầu.

Đối chiếu **mẫu → mapping → first frame → timeline → sound → caption**. Từng vai trò và event quan trọng có nơi tương ứng ở đích hoặc lý do bỏ/sửa; không mất phản ứng nhỏ quyết định nhân quả. Ghi setup, điểm tạo lực, key onset/interval và hậu quả; chứng cứ mờ vẫn mờ, không invent kết cục. Caption nguyên bản theo audience hiện hành của đích, không sao mẫu hoặc dùng jargon của loài khác.

Mapping được gộp/tách event, đổi thời gian hoặc sắp xếp lại khi vẫn giữ quan hệ được giao và tính đúng; không ép một event nguồn bằng một beat đích hoặc chép nguyên số giây. Thay đổi ý nghĩa/quan hệ đã khóa vẫn theo quyền ở trên. So lại phần quyết định trong prompt bằng bước G của [Story Development](story-development.md); đủ ID/liên kết không chứng minh chuyển thể đúng nghĩa. Role/event của schema có thể biểu diễn cảnh vật và đoạn biến đổi/trạng thái quan sát có ý nghĩa; key_event_ids chỉ phần quan trọng cần chuyển thể, không buộc có cao trào. Không bịa nhân vật, động cơ hay biến cố để điền hồ sơ; thiếu quan sát thì ghi giới hạn đúng như quy trình phân tích.

Dùng [lõi prompt](video-prompt-workflow.md), output-contract/format/model/QA hiện hành và helper chayvideo. Mặc định bốn mục, không phát sinh sản phẩm thứ năm bắt buộc. Hồ sơ/coverage/mapping để local. Không tự render để chứng minh; QA ảnh/video/âm thực chỉ sau truy cập sản phẩm thật. Thay đổi ở lõi/Project phải kiểm cả new và reference; thay phân tích media chỉ ảnh hưởng na-clonevideo, không tự áp cho sáng tạo độc lập.

## Khóa cơ chế máy–chủ thể trước viết — v1.7

Trong adaptation.md hiện có, ghi riêng translation của máy, rotation của máy, chuyển động cá/chủ thể và quan hệ cần giữ; gắn timecode/evidence, unknown nếu không đủ bằng chứng. Máy đi cạnh cá không được thay bằng cá xoay với máy đứng. Mẫu/brief đã khóa máy cố định không bị ép handheld bởi mặc định Project; xung đột trọng yếu phải xử lý theo quyền đã giao. User nhận draft partial chỉ chấp nhận giới hạn quan sát, không cho phép đổi quan hệ cốt lõi. Revision cập nhật mapping hiện hành cùng prompt, giữ mapping lịch sử bất biến và chỉ rõ nguồn đang dùng. Không thêm báo cáo đầu ra thứ năm.
