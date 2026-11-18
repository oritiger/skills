---
name: vietnamese-natural-writing
description: "Write and rewrite Vietnamese deliverables so they read like a real person wrote them, not a machine: uneven sentence rhythm, concrete true detail, no AI stock phrases, tidy triplets or formula endings. Bundles techniques distilled from Nam Cao, Sơn Nam, Nguyễn Ngọc Tư and Nguyễn Nhật Ánh; writing types (truyện/tản văn, quảng cáo, trang trọng, lịch sự, kịch bản video/voiceover, tin nhắn/chat); paraphraser-style rewrite modes (Standard, Fluency, Humanize, Formal, Academic, Simple, Creative, Expand, Shorten, Custom, synonym level); a checker script; and a feedback log that learns from the user's approvals and rejections. Confirms the mode before writing. Use when the user asks to write, rewrite, paraphrase or humanize Vietnamese text, says it 'sounds like AI', 'văn máy', 'viết lại cho tự nhiên', 'đỡ giống AI', or asks for Vietnamese stories, ads, captions, video scripts, product copy, emails, announcements or messages to customers. Not for ordinary conversational replies to the user. Vietnamese only."
---

# Viết tiếng Việt tự nhiên

Mục tiêu: người đọc thấy một người thật viết. Skill này không hứa "qua mặt máy dò AI". Máy dò không đáng tin, chấm sai cả văn người thật. Người dùng hỏi về máy dò thì nói thẳng như vậy. Việc skill làm được là bỏ những dấu hiệu mà người đọc nhận ra.

## Phạm vi

Dùng cho **bài viết giao cho người dùng**: bài đăng, quảng cáo, kịch bản, truyện, email, thông báo, tin nhắn gửi khách… Không dùng cho câu trả lời trò chuyện thường ngày giữa trợ lý và người dùng; khi đó trả lời bình thường, không hỏi chế độ.

## Luật cứng

- **Không bịa.** Số liệu, trải nghiệm "tôi đã dùng", lời khách hàng, lỗi "cho có vẻ thật": người dùng không đưa thì không viết. Thiếu thì hỏi, hoặc để `[chỗ trống]`.
- Không chép câu chữ của nhà văn; chỉ học kỹ thuật.
- Chỉ tiếng Việt.
- Giọng Nam Bộ: không tự dùng, không hỏi. Chỉ khi người dùng yêu cầu giọng miền Nam / miền Tây mới dùng thêm skill `southern-mekong-vietnamese-dialect`; khi đó luật của skill đó thắng (không "ạ", "vâng").

## Quy trình

### 1. Xác nhận trước khi viết

Chốt với người dùng trước. Có công cụ AskUserQuestion thì dùng (tối đa 4 câu, mỗi câu 2–4 lựa chọn, lựa chọn đề xuất đứng đầu). Không có thì hỏi một danh sách ngắn kèm đề xuất sẵn, để người dùng chỉ cần trả lời "ok".

Cần chốt:
1. **Chế độ.**
   - Viết mới: Truyện / tản văn, Quảng cáo, Trang trọng, Lịch sự, Kịch bản video / lời đọc, Tin nhắn / chat.
   - Viết lại: Chuẩn, Trôi chảy, Tự nhiên hóa, Trang trọng, Học thuật, Đơn giản, Sáng tạo, Mở rộng, Rút gọn, Tùy chỉnh.
2. **Người đọc và xưng hô.**
3. **Độ dài.**
4. **Mức đổi từ** (chỉ khi viết lại): thấp / vừa / cao.

Với Quảng cáo và Mở rộng, hỏi thêm bằng lời những **chi tiết thật** còn thiếu: giá, thời gian, giới hạn, ai đang dùng.

Chỉ bỏ qua bước này khi người dùng đã nói đủ, hoặc bảo "khỏi hỏi", "viết luôn". Khi đó ghi một dòng đầu bài: chế độ và mặc định đã dùng.

### 2. Viết nháp

Đọc phần của chế độ đã chốt trong [references/che-do-viet.md](references/che-do-viet.md). Viết truyện, tản văn, quảng cáo, kể chuyện vùng miền thì đọc thêm [references/van-phong-tac-gia.md](references/van-phong-tac-gia.md) và chọn giọng gần nhất theo bảng "Chọn giọng theo việc".

[references/mau-da-duyet.md](references/mau-da-duyet.md) có mục cùng chế độ thì đọc trước: học khung của bài được duyệt, tránh khung của bài bị chê.

### 3. Sửa cho ra người

Rà theo [references/dau-hieu-ai.md](references/dau-hieu-ai.md). Tối thiểu, chế độ nào cũng làm:

- Bỏ mở bài khái quát ("Trong thời đại…"), câu chốt công thức ("Tóm lại…", "Hãy…"), vỏ bọc trợ lý ("Dưới đây là…").
- Thay từ sáo bằng chuyện cụ thể **có thật**.
- Phá bộ ba đều nhịp ("nhanh, gọn, rẻ"; "có X, có Y, có Z") và "không chỉ… mà còn".
- Lệch nhịp câu theo mức của chế độ (bảng cuối `che-do-viet.md`): gộp thành một câu thật dài, tách một ý thành câu thật ngắn, có đoạn chỉ một câu.
- Liên từ khung ("Bên cạnh đó", "Ngoài ra") đổi thành mà / rồi / còn / nhưng, hoặc bỏ.
- Truyện, quảng cáo: cảm xúc giao cho đồ vật và cơ thể, không gọi tên.
- Truyện, quảng cáo: thử bỏ câu cuối. Bài vẫn đứng được thì bỏ; câu chốt đắt giá là thói máy.
- Đọc lại tìm thói cũ mọc ra chỗ khác. Sửa chữ không đủ, phải đổi **khung**: nhịp, số vế, cách kết.

Đừng sửa quá tay (mục F trong `dau-hieu-ai.md`): không nhồi tiếng lóng, không cố ý sai chính tả, không rải câu cụt khắp nơi.

### 4. Chạy checker

Với bài từ khoảng 5 câu trở lên:

```bash
printf '%s' "$DRAFT" | python3 SKILL_DIR/scripts/check_ai_tells.py --mode ads -
python3 SKILL_DIR/scripts/check_ai_tells.py --mode story bai-viet.md
```

`--mode`: `story` (truyện, sáng tạo, tự nhiên hóa), `ads`, `script` (kịch bản video, lời đọc), `chat`, `polite`, `formal`, `academic`. Chọn cái gần thể loại của bài nhất.

Checker đo độ lệch nhịp câu (CV) so với bốn nhà văn (0,5–0,7; dưới 0,35 là đều như máy; lời kể trên 0,9 là vụn quá), bắt chuỗi câu dài bằng nhau, đoạn đều nhau, bộ ba, từ sáo, mở và kết công thức, câu chốt đắt giá ở cuối. Nó chỉ gợi ý: sửa cảnh báo nào hợp lý, đừng sửa văn cho đẹp số. Văn trang trọng, học thuật đều hơn là bình thường.

Checker **không** bắt được chi tiết bịa, cảm xúc gọi tên, thoại chuẩn mực, nội dung chung chung. Mấy cái đó phải tự đọc to một lần.

### 5. Giao bài

- Chỉ đưa bài viết. Không mở bằng "Dưới đây là…", không kết bằng "Hy vọng…".
- Còn chỗ cần chi tiết thật: để `[chỗ trống]`, hỏi một câu ngắn sau bài.
- Người dùng chê "vẫn giống AI": hỏi câu nào, gọi đúng tên thói đó, sửa đúng chỗ đó. Đừng viết lại toàn bài theo cùng một khung.

### 6. Học từ phản hồi

Thước đo là người dùng, không phải checker. Mỗi lần người dùng chê hay duyệt là một dữ liệu, ghi lại:

- **Bị chê** ("giống AI", "máy quá", hoặc chỉ ra một câu): gọi đúng tên thói, sửa, rồi ghi:
  1. Cụm từ cố định: thêm vô đúng mục trong `scripts/phrases.txt`.
  2. Kiểu cấu trúc: thêm một dòng vô bảng mục A của `references/dau-hieu-ai.md`. Bắt được bằng regex thì thêm check vô `scripts/check_ai_tells.py` kèm một test trong `scripts/test_check_ai_tells.py`.
  3. Bài bị chê: ghi vô mục "Bị chê" của `references/mau-da-duyet.md`, theo định dạng ở đầu file.
- **Được duyệt** ("ok", "được rồi", "hay đó", hoặc dùng luôn): hỏi một câu ngắn có muốn lưu làm mẫu không; đồng ý thì ghi vô mục "Được duyệt".
- Sửa `phrases.txt` hoặc checker xong thì chạy `python3 SKILL_DIR/scripts/test_check_ai_tells.py`; test phải qua.
- Báo một dòng đã ghi gì, vô file nào. Không ghi thông tin riêng (tên khách, số điện thoại, địa chỉ) vô mẫu; thay bằng `[tên]`, `[sđt]`.
- Thư mục skill không ghi được: đưa người dùng đoạn cần thêm để họ tự dán.
