# Dấu hiệu văn máy trong tiếng Việt và cách sửa

Danh sách để rà bản nháp. `scripts/check_ai_tells.py` bắt được phần lớn mục A, B, D, E và phần "gọi tên cảm xúc" của mục C; phần còn lại của C và mục F phải tự đọc. Ví dụ thật người dùng đã bắt lỗi nằm ở `mau-da-duyet.md`.

## Mục lục

- [A. Nhịp và cấu trúc](#a-nhịp-và-cấu-trúc)
- [B. Từ ngữ sáo](#b-từ-ngữ-sáo)
- [C. Nội dung và cảm xúc](#c-nội-dung-và-cảm-xúc)
- [D. Dấu vết dịch máy](#d-dấu-vết-dịch-máy)
- [E. Vỏ bọc trợ lý](#e-vỏ-bọc-trợ-lý)
- [F. Sửa quá tay](#f-sửa-quá-tay)

## A. Nhịp và cấu trúc

| Dấu hiệu | Vì sao lộ | Sửa |
| :--- | :--- | :--- |
| Câu dài gần bằng nhau, nối nhau đều đặn | Người viết thật có CV độ dài câu 0,5–0,7 (xem `van-phong-tac-gia.md`); máy thường dưới 0,4 | Gộp hai câu thành một câu dài; tách một ý thành câu 2–5 chữ; để một câu đứng riêng thành đoạn |
| Mệnh đề trong câu ngắn bằng nhau, cách nhau bằng dấu phẩy, như gõ nhịp | Nhịp "tạch, tạch, tạch" của văn quảng cáo máy | Cho một vế dài hẳn ra, một vế cụt; bỏ bớt một vế |
| Bộ ba: "X, Y và Z", "có A, có B, có C" | Máy thích số ba cân đối | Giữ hai, hoặc bốn mà một cái lạc tông; hoặc hai vế lệch kết bằng phủ định ngắn ("Họ có nhà để về, chúng tôi thì không.") |
| "Không chỉ… mà còn…" | Cặp đối xứng quen tay | Nói thẳng một ý; ý phụ để câu sau, ngắn |
| Mở bài khái quát: "Trong thời đại…", "Ngày nay…", "Trong cuộc sống…" | Mở bằng bối cảnh chung thay vì sự việc | Mở bằng việc đang xảy ra, một người cụ thể, một con số |
| Câu chốt cuối như khẩu hiệu, hoặc "Tóm lại…", "Hãy…" | Máy luôn khép bài gọn gàng | Kết bằng hình ảnh, câu hỏi bỏ ngỏ, nhận xét lơ đãng; quảng cáo thì kết bằng việc cụ thể cần làm. Câu cuối ngắn đứng riêng sau câu dài: thử bỏ nó, bài vẫn đứng được thì bỏ |
| Hỏi rồi tự đáp: "Bạn có biết…? Đó chính là…" | Công thức gây tò mò | Bỏ câu hỏi, nói luôn; hoặc hỏi mà không trả lời |
| Đoạn nào cũng 3–4 câu | Đều như xếp gạch | Có đoạn một câu, có đoạn dài |
| Liên từ khung: "Bên cạnh đó", "Ngoài ra", "Hơn nữa", "Tuy nhiên", "Đặc biệt" | Văn nghị luận học trò, văn máy | "Mà", "rồi", "còn", "nhưng", hoặc không cần nối |
| Gạch ngang dài (—) chen giữa câu, nhiều lần | Thói quen văn máy tiếng Anh | Dùng dấu phẩy, ngoặc đơn, hoặc tách câu |
| Mọi thứ rõ ràng, chắc nịch, không một chữ thừa | Người thật có ngập ngừng, có chữ đệm | Thêm chỗ do dự thật ("hình như", "cũng tạm", "à mà"), có giới hạn |
| Ba câu liền nhau mở cùng một chữ ("Bạn…", "Bạn…", "Bạn…") | Khuôn câu lặp | Đổi cách mở, gộp hai câu, hoặc bỏ chủ ngữ |
| Kịch bản đọc có câu dài quá một hơi (trên 25 chữ) | Viết cho mắt, không cho miệng | Tách câu, đặt chỗ ngắt nghỉ tự nhiên |

Bài học từ các lần bị chê (`mau-da-duyet.md`): sửa chữ không đủ, phải đổi **khung** (nhịp, số vế, cách kết), và chi tiết phải là chi tiết thật người dùng đưa.

## B. Từ ngữ sáo

Danh sách đầy đủ, chia theo mục, nằm ở `scripts/phrases.txt` (checker đọc file này; thêm cụm mới vô đó). Vài ví dụ:

- **Gần như luôn lộ:** trong thời đại, đóng vai trò quan trọng, không thể phủ nhận, hành trình, nâng tầm, chạm đến trái tim, tóm lại.
- **Văn quảng cáo máy:** từ A đến Z, chỉ với một cú click, đừng bỏ lỡ, còn chần chừ gì nữa, giải pháp toàn diện, tối ưu, hoàn chỉnh. Thêm công thức mở câu "Chỉ cần… là…".
- **Dùng nhiều thì lộ:** mang lại, thực sự, vô cùng, tuyệt vời, một cách + tính từ.
- **Gọi tên cảm xúc:** vô cùng xúc động, hạnh phúc, nỗi buồn, trào dâng, bồi hồi (xem mục C).

Cách sửa chung: thay từ sáo bằng chuyện cụ thể. "Giải pháp tối ưu giúp tiết kiệm thời gian" → nói nó tiết kiệm cái gì, bao lâu, cho ai. Không có chuyện cụ thể thì hỏi người dùng.

## C. Nội dung và cảm xúc

- **Gọi tên cảm xúc** ("vô cùng xúc động", "nỗi buồn sâu sắc"): giao cho cơ thể và đồ vật (mắt rơm rớm, tay giấu tờ giấy, chén cơm chan nước).
- **Khen không có chi tiết**: câu khen nào dán sang sản phẩm khác vẫn đúng thì bỏ.
- **Không có giới hạn nào**: thêm một hạn chế có thật (phải sửa tay chỗ nào, chậm lúc nào). Người đọc tin hơn.
- **Chi tiết được chọn cho đẹp**: chi tiết thật thường hơi xấu, hơi lạc, hơi tầm thường.
- **Giải thích sau khi tả** ("điều đó cho thấy…"): bỏ câu giải thích, để chi tiết tự nói.
- **Ai cũng nói năng chuẩn mực**: cho nhân vật nói cụt, đáp lệch, chêm.
- **Không lạc đề lần nào**: người thật có lúc rẽ ngang một câu rồi quay lại.

## D. Dấu vết dịch máy

- "Nó" làm chủ ngữ giả (dịch "It is…"): "Nó là một công cụ…" → "Công cụ này…" hoặc bỏ chủ ngữ.
- Bị động "được" thừa: "được thiết kế để giúp bạn" → "làm ra để…" hoặc nói chủ động.
- Danh hóa "việc + động từ": "Việc sử dụng ứng dụng giúp…" → "Dùng ứng dụng thì…".
- "Bạn" ở đầu mọi câu; "chúng ta" tràn lan.
- "Một trong những … nhất", "rất nhiều các", "các" và "những" thừa.
- Chuỗi "của": "chất lượng của sản phẩm của công ty" → "hàng của công ty".
- Thiếu "thì, mà, là" chỗ người Việt hay nói: "Nếu trời mưa, chúng ta ở nhà" → "Mưa thì ở nhà".

## E. Vỏ bọc trợ lý

Bỏ hết khi giao bài: "Dưới đây là…", "Đây là phiên bản…", "Hy vọng…", "Chúc bạn…", "Nếu bạn cần thêm…", "Tôi rất sẵn lòng…". Tiêu đề in đậm và gạch đầu dòng trong văn xuôi, emoji đầu dòng, hashtag xếp hàng: chỉ dùng khi người dùng muốn hoặc thể loại cần.

## F. Sửa quá tay

Sửa máy thành người không có nghĩa là làm bẩn văn:

- **Không bịa chi tiết.** Con số, trải nghiệm, lời khách, lỗi "cho thật" mà người dùng không đưa thì không được viết vô. Thiếu thì hỏi, hoặc để `[chỗ trống]`.
- Không cố ý sai chính tả, không viết tắt kiểu chat khi thể loại không cần.
- Không nhồi tiếng lóng, khẩu ngữ, tiểu từ; mỗi đoạn vài chỗ là đủ.
- Không rải câu cụt khắp nơi; câu cụt chỉ mạnh khi đứng cạnh câu dài. Checker cảnh báo khi CV riêng lời kể (bỏ lời thoại) vượt 0,9, tức vụn hơn mọi nhà văn đã đo.
- Không tự thêm giọng địa phương khi người dùng không yêu cầu.
- Sửa xong đọc lại tìm thói cũ mọc lại chỗ khác: bộ ba mới, câu chốt mới.
