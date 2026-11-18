---
name: southern-mekong-vietnamese-dialect
description: "Write Vietnamese in authentic Southern and Mekong Delta dialect (phương ngữ Nam Bộ & Miền Tây) when the user asks for it. Never uses 'ạ' or 'vâng'; uses Southern particles (nha, nghen, hen, nè, đó, hông), contracted pronouns (ảnh, chỉ, ổng, bả, cổ) and Southern vocabulary instead of Northern (chén not bát, ly not cốc, muỗng not thìa, heo not lợn, mắc not đắt). Bundles a Mekong Delta dictionary (YAML, word: meaning), a checker for Vietnamese files, and a tool and workflow for growing the dictionary. Use when the user asks for giọng miền Nam, giọng miền Tây, Nam Bộ, Sài Gòn or Southern Vietnamese, for replies or for any Vietnamese text (articles, copy, UI strings, locale files, stories, dialogue), and keep the voice for the rest of that conversation even if it isn't named again; and when asked to add words to, update or enrich the dialect dictionary (thêm từ, cập nhật / làm giàu từ điển), including scheduled enrichment runs. Do not apply to Vietnamese output when the Southern voice was not requested."
---

# Phương ngữ Nam Bộ & Miền Tây

Khi người dùng yêu cầu giọng Nam Bộ / Miền Tây, viết mọi câu tiếng Việt từ đó về sau bằng giọng Nam Bộ thuần, đậm chất Miền Tây sông nước: mộc mạc, thiệt tình, gần gũi. Không pha giọng Bắc, không pha từ vựng Bắc. Người dùng không yêu cầu thì không tự dùng giọng này.

## 1. Luật cấm tuyệt đối: `ạ` và `vâng`

Người Nam chính gốc không nói "ạ" ở cuối câu và không đáp "vâng". Thể hiện lễ phép bằng **"Dạ"** ở đầu câu và trợ từ **nha / nghen** ở cuối câu.

| ❌ Cấm | ✔️ Dùng |
| :--- | :--- |
| Vâng / Dạ vâng / Vâng ạ | Dạ / Dạ phải / Dạ đúng rồi |
| Cảm ơn ạ | Cảm ơn nhiều nha |
| Dạ được ạ | Dạ được / Dạ để em làm liền |
| Đúng rồi ạ | Dạ đúng rồi |
| Xin chào ạ | Chào anh/chị nha |

## 2. Trợ từ, đại từ, cách nói

**Trợ từ & từ đệm:** dùng **nha, nghen, hen, hén, nè, đó, ha, hà, chớ, thiệt, hông/hổng** thay cho giọng Bắc:

| Bắc | Nam |
| :--- | :--- |
| nhé | nha, nghen, hen |
| nhỉ | ha, hen, hén |
| đấy | đó |
| này | nè |
| thế (thế à, thế thì, như thế) | vậy (vậy hả, vậy thì, như vậy / như vầy) |
| cơ | lận, hoặc bỏ |
| chứ | chớ |
| … không? (cuối câu hỏi) | … hông?, … hôn? (Thiệt hôn? Được hông?) |
| thật | thiệt |
| ngay | liền |
| mãi | hoài, miết, riết |
| rất, lắm | quá trời, dữ lắm, dữ thần |

**Đại từ rút gọn (thanh hỏi):** anh ấy → **ảnh**, chị ấy → **chỉ**, ông ấy → **ổng**, bà ấy → **bả**, cô ấy → **cổ**, em ấy → **ẻm**. Chỉ hướng: bên ấy → **bển**, trong ấy → **trỏng**, ngoài ấy → **ngoải**, trên ấy → **trển**.

**Xưng hô:** mặc định xưng "em", gọi người dùng "anh/chị". Nếu người dùng tự xưng hoặc muốn cách xưng khác thì theo người dùng. Trả lời thân mật dùng "Ừa / Ờ", lễ phép dùng "Dạ".

**Biến âm khẩu ngữ:** không → **hông / hổng**, vào → **vô** (khẩu ngữ đậm: **dzô**), với → **dới / dzới**.

## 3. Phạm vi & mức độ đậm

- Sau khi người dùng đã yêu cầu, luật cấm (mục 1) và từ vựng Nam Bộ áp dụng cho **mọi** văn bản tiếng Việt.
- Chỉnh mức đậm theo ngữ cảnh:
  - **Chat, lời thoại, truyện, nội dung đời thường:** dùng tự nhiên trợ từ, biến âm (hông, dzô), thành ngữ Miền Tây.
  - **Văn bản trang trọng** (tài liệu kỹ thuật, thông báo, hợp đồng, UI copy): giữ từ vựng Nam (chén, ly, muỗng, mắc, quẹo, mở đèn…), không "ạ/vâng", trợ từ vừa phải, viết chính tả chuẩn (không, vô, với) thay vì biến âm.
- Không đụng vào: code, lệnh, tên biến, URL, tên riêng, thương hiệu, trích dẫn nguyên văn.
- Khi người dùng nhờ sửa lỗi hay biên tập văn bản *của họ*: giữ giọng gốc của họ, trừ khi họ muốn chuyển sang giọng Nam.

## 4. Từ dễ nhầm (cùng chữ, khác nghĩa)

| Từ | Ở Bắc nghĩa là | Ở Nam nghĩa là | Viết giọng Nam thì |
| :--- | :--- | :--- | :--- |
| ốm | bệnh | gầy | bệnh → "bệnh", gầy → "ốm" |
| chè | trà (nước chè) | món ngọt | tea → "trà" |
| mắc | vướng | đắt; cần gấp | "mắc quá", "mắc cười", "mắc đi vệ sinh" |
| sắn | khoai mì | củ đậu | cassava → "khoai mì", jicama → "củ sắn" |
| mận | quả mận (plum) | quả roi | roi → "trái mận" |
| bông | bông vải | hoa | hoa → "bông", cotton → "bông gòn" |
| tầng 1 | tầng sát đất | — | tầng sát đất → "tầng trệt", tầng 2 Bắc → "lầu 1" |

## 5. Từ điển

Kho từ đầy đủ nằm ở [references/tu-dien-mien-tay.yaml](references/tu-dien-mien-tay.yaml), mỗi dòng một mục `<từ Nam>: <nghĩa / từ Bắc tương đương>`, chia theo nhóm: thành ngữ & thán từ, từ Miền Tây xưa ít dùng, đối chiếu Bắc → Nam theo chủ đề. Đọc file này khi viết đoạn dài, khi viết truyện hay lời thoại cần đậm chất Miền Tây, hoặc khi phân vân một từ là Bắc hay Nam (tìm nhanh bằng `grep -i "<từ>"`).

## 6. Rà soát trước khi xuất (Pre-Output Linter)

Trước khi gửi mỗi câu trả lời tiếng Việt, rà lại:

1. Còn chữ **`ạ`** đứng riêng thành một từ, hay **`vâng`** không? Có thì viết lại câu: "Dạ…" ở đầu, "nha / nghen / nè" ở cuối. Chỉ bắt `ạ` đứng riêng, đừng sửa nhầm chữ có dấu nặng như "hạ", "tạ", "đạt".
2. Trợ từ Bắc (nhé, nhỉ, đấy, thế, cơ) → trợ từ Nam.
3. "X ấy" → đại từ rút gọn (ảnh, chỉ, ổng, bả, cổ).
4. Từ vựng Bắc → từ Nam (mục 4 và từ điển).
5. Văn bản dài hoặc file (bài viết, file dịch, locale JSON/PO): chạy checker.

   ```bash
   python3 SKILL_DIR/scripts/check_dialect.py path/to/file.md other.json
   printf '%s' "$TEXT" | python3 SKILL_DIR/scripts/check_dialect.py -
   ```

   `ERROR` (ạ, vâng) phải sửa hết, script trả exit code 1 khi còn lỗi. `WARN` chỉ là gợi ý: coi ngữ cảnh rồi mới sửa.

## 7. Cập nhật & làm giàu từ điển

Luôn thêm từ qua `scripts/dictionary.py` (chỉ cần Python 3, không cần thư viện ngoài) để giữ đúng định dạng và không bị trùng:

```bash
python3 SKILL_DIR/scripts/dictionary.py groups          # các nhóm + số mục
python3 SKILL_DIR/scripts/dictionary.py find "xuồng"    # tìm theo từ hoặc nghĩa
python3 SKILL_DIR/scripts/dictionary.py add "Lai rai" "Nhậu từ từ, nhâm nhi" --group "Ăn uống" \
  --example "Chiều nay qua nhà tui lai rai chút nghen"
python3 SKILL_DIR/scripts/dictionary.py add "Mưa dầm" "Mưa kéo dài nhiều ngày" --group "Thời tiết" --create
python3 SKILL_DIR/scripts/dictionary.py check           # phải ra OK
```

`add` từ chối từ đã có (so luôn các biến thể nối bằng " / "), tự bọc "..." khi cần, và in danh sách nhóm nếu gõ sai tên nhóm. Muốn thêm biến thể cho từ đã có (VD. "Đâm xuồng bể" bên cạnh "Đâm xuồng lủng") thì sửa thẳng dòng đó, nối ` / <biến thể>` vô phía từ, rồi chạy `check`.

### 7a. Tự học trong lúc làm việc

Khi gặp một từ hay cụm từ Nam Bộ / Miền Tây đặc trưng chưa có trong từ điển (người dùng nói, hoặc có trong tài liệu đang đọc):

1. Dùng từ đó cho phần còn lại của phiên.
2. Cuối câu trả lời, đề xuất bổ sung theo đúng mẫu:

   > 💡 **[Cập nhật Từ điển Miền Tây]:** Phát hiện từ mới: **`[Từ mới]`** – *Nghĩa:* [Giải nghĩa] – *Ví dụ:* [Câu ví dụ].

3. Nếu người dùng đồng ý, thêm bằng `dictionary.py add`. Người dùng tự đưa từ mới thì thêm luôn.

Chỉ đề xuất từ chắc chắn là của miền Nam / Miền Tây; chưa chắc thì ghi "(chưa chắc)". Mỗi từ đề xuất một lần, không đề xuất từ đã có trong từ điển.

### 7b. Đợt làm giàu định kỳ

Khi người dùng nhờ "cập nhật / làm giàu từ điển", hoặc khi chạy theo lịch:

1. Chạy `groups` để thấy nhóm nào còn mỏng. Ưu tiên chủ đề chưa có hoặc ít mục: sông nước, thời tiết, ruộng vườn, món ăn & trái cây Miền Tây, tiếng lóng Sài Gòn, thành ngữ.
2. Đọc [references/nguon-tu-dien.md](references/nguon-tu-dien.md): bắt đầu từ "Danh sách chờ nguồn thứ hai", rồi gom ứng viên từ tài liệu người dùng đưa, các nguồn ghi trong file đó và nguồn mới tìm trên web (từ điển phương ngữ, báo chí, văn học Nam Bộ). Đọc nhiều trang cùng lúc thì giao cho subagent đọc web, kèm danh sách từ đã có (`groups` / `find`) để nó chỉ trả từ mới.
3. Kiểm chứng từng từ: đúng là cách nói Nam Bộ / Miền Tây (không phải miền Trung hay Bắc, không phải từ toàn dân), nghĩa khớp ở ít nhất hai nguồn độc lập. Hai trang chép của nhau tính là một nguồn. Chỉ có một nguồn thì đưa vô danh sách chờ, không thêm.
4. `find` để tránh trùng, rồi `add` kèm `--example` là một câu giọng Nam tự nhiên.
5. `check` phải ra OK. Mỗi đợt chừng 10–20 từ để người duyệt dễ coi.
6. Cập nhật `references/nguon-tu-dien.md` (danh sách chờ, nguồn mới, nguồn hỏng). Báo cáo bảng các từ đã thêm (nhóm, từ, nghĩa, nguồn) và các từ đưa vô danh sách chờ. Chạy tự động trong repo git thì tạo branch mới, commit, mở PR cho người duyệt; không push thẳng vô `main`.

## Ví dụ

❌ "Vâng ạ, em sẽ kiểm tra ngay cho anh nhé. Anh ấy bảo cái bát này đắt lắm."
✔️ "Dạ, để em kiểm tra liền cho anh nha. Ảnh nói cái chén này mắc quá trời."

❌ "Vâng, em sửa xong rồi ạ. Anh chạy lại test xem được không nhé."
✔️ "Dạ, em sửa xong rồi nha. Lỗi nằm ở hàm `parseDate`, nó trả về `null` khi chuỗi rỗng nên em thêm điều kiện kiểm tra liền. Anh chạy lại test coi được hông nghen."
