#!/usr/bin/env python3
"""Tests for check_ai_tells.py. Run: python3 test_check_ai_tells.py

When a new pattern is added to the checker (or to phrases.txt), add a case here:
one text that must be flagged, and keep the "clean" texts clean.
"""
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("check_ai_tells", os.path.join(HERE, "check_ai_tells.py"))
cat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cat)

AI_AD = (
    "Trong thời đại công nghệ 4.0, video đóng vai trò quan trọng trong chiến lược marketing. "
    "Công cụ của chúng tôi giúp bạn tạo video nhanh chóng, dễ dàng và chuyên nghiệp. "
    "Chỉ cần nhập ý tưởng, bấm một nút, hệ thống sẽ tự động xử lý từ A đến Z. "
    "Không chỉ tiết kiệm thời gian mà còn tối ưu chi phí cho doanh nghiệp. "
    "Bên cạnh đó, giao diện thân thiện mang lại trải nghiệm tuyệt vời cho người dùng. "
    "Tóm lại, đây là giải pháp toàn diện cho mọi nhu cầu sáng tạo nội dung."
)
# Public-domain Nam Cao lines (Chí Phèo, Lão Hạc).
NAM_CAO = (
    "Hắn vừa đi vừa chửi. Bao giờ cũng thế, cứ rượu xong là hắn chửi. "
    "Lão Hạc thổi cái mồi rơm, châm đóm. Tôi đã thông điếu và bỏ thuốc rồi. "
    "Tôi mời lão hút trước. À không! À không! Không giết cậu Vàng đâu nhỉ!..."
)
HUMAN_LIKE = (
    "Họ có nhà để về, chúng tôi thì không. Tôi chưa bao giờ thấy cái màu đỏ lạ lùng ấy. "
    "Đỏ hơn bông bụp ngoài sân, đỏ hơn máu. Hôm qua gõ đại một câu kiểu review quán ăn, "
    "đợi chừng năm bảy phút gì đó là nó ra video. Sub có mấy chỗ sai chính tả phải sửa tay. Nhạc nền hơi sến."
)


def codes(text, mode="story"):
    return {c for c, _ in cat.analyze(text, mode)["warnings"]}


class CleanTexts(unittest.TestCase):
    def test_nam_cao_is_clean(self):
        self.assertEqual(codes(NAM_CAO), set())

    def test_human_like_is_clean(self):
        self.assertEqual(codes(HUMAN_LIKE), set())


class Detection(unittest.TestCase):
    def test_ai_ad_paragraph(self):
        expected = {"rhythm", "run", "triplet", "phrases:strong", "phrases:ads", "connectors",
                    "khong-chi", "opener", "closer", "formula"}
        self.assertTrue(expected <= codes(AI_AD, "ads"), expected - codes(AI_AD, "ads"))

    def test_formal_mode_softens_rhythm(self):
        c = codes(AI_AD, "formal")
        self.assertNotIn("rhythm", c)
        self.assertIn("phrases:strong", c)

    def test_anaphora_triplet(self):
        self.assertIn("triplet", codes("Quay lại là có video 60 giây, có sub, có nhạc."))

    def test_translationese(self):
        text = ("Nó là một công cụ được thiết kế cho người bận rộn. Việc sử dụng ứng dụng khá đơn giản. "
                "Đây là một trong những ứng dụng tốt nhất hiện giờ.")
        self.assertIn("translationese", codes(text))

    def test_emotion_named_only_in_expressive_modes(self):
        text = "Tôi vô cùng xúc động và hạnh phúc khi nhận được tin."
        self.assertIn("emotion", codes(text, "story"))
        self.assertNotIn("emotion", codes(text, "formal"))

    def test_same_opener(self):
        text = "Bạn muốn bán hàng. Bạn cần khách. Bạn sẽ thích công cụ này. Mình thì không chắc. Thử coi."
        self.assertIn("same-opener", codes(text))

    def test_emoji_and_hashtags(self):
        text = "🔥 Sale lớn\n✨ Giảm giá sâu\n🎁 Quà tặng kèm\nMua ngay #sale #giamgia #quatang #hot"
        c = codes(text, "ads")
        self.assertIn("emoji", c)
        self.assertIn("hashtag", c)

    def test_script_long_sentence(self):
        long = " ".join(["chữ"] * 30) + "."
        self.assertIn("long-sentence", codes(long, "script"))
        self.assertNotIn("long-sentence", codes(long, "story"))

    def test_script_greeting_cliche(self):
        self.assertIn("phrases:ads", codes("Xin chào các bạn, hôm nay mình sẽ review quán bún.", "script"))

    def test_markdown_in_chat(self):
        self.assertIn("markdown", codes("**Chào anh**\n- Đơn đã giao\n- Còn thiếu một món", "chat"))

    def test_choppy_narration(self):
        text = ("Đêm. Gió. Tui nằm yên trên cái võng ngoài hiên mà nghe nước liếm vô chân cột nhà từng hồi. "
                "Lạnh. Im. Tiếng đếm. Gần. Xa. Rồi tui nghe tiếng con ểnh ương dưới đìa kêu một tiếng dài "
                "thiệt dài rồi thôi luôn. Sợ.")
        self.assertIn("choppy", codes(text))

    def test_dialogue_does_not_count_as_choppy(self):
        text = ("Tiếng đếm vọng từ phía cầu, đều đều như người ta đếm tiền cho khỏi quên.\n\n"
                "\"Một. Hai. Ba.\"\n\n\"Bốn. Năm.\"\n\n\"Sáu.\"\n\n"
                "Sáng ra ba tui ra cầu coi, cầu còn y nguyên, chỉ có thân dừa ướt sũng. "
                "Má tui nói dấu mèo. Mà mèo nhà mình đi mất tiêu từ hôm nước lên. "
                "Ba tui nhìn cái dấu một hồi lâu rồi đi vô nhà. Chiều nước rút. "
                "Tui ra đìa sau nhà kiếm cái gáo bị trôi hồi hôm. Má đứng trên bờ.")
        self.assertNotIn("choppy", codes(text))

    def test_punchy_closer(self):
        story = ("Má tui đứng trên bờ, ôm rổ rau.\n\nMiệng má lẩm nhẩm, tui ghé tai lại thì nghe rõ ràng là đếm.\n\n"
                 "Tui không dám hỏi đếm cái gì.")
        self.assertIn("closer-punch", codes(story))
        ad = ("Gõ một câu, đi pha ly cà phê, quay lại là có video sáu mươi giây để đăng luôn lên trang. "
              "Tui chưa từng mở Premiere lần nào.")
        self.assertIn("closer-punch", codes(ad, "ads"))
        self.assertNotIn("closer-punch", codes(story, "formal"))

    def test_self_answer(self):
        self.assertIn("self-answer", codes("Bạn có biết vì sao? Đó chính là nhờ công nghệ mới."))


class PhrasesFile(unittest.TestCase):
    def test_sections_present_and_unique(self):
        p = cat.load_phrases()
        for section in ("strong", "ads", "connectors", "density", "wrappers", "translationese", "emotion"):
            self.assertIn(section, p)
        everything = [x for v in p.values() for x in v]
        dupes = {x for x in everything if everything.count(x) > 1}
        self.assertEqual(dupes, set(), f"cụm bị lặp: {dupes}")


if __name__ == "__main__":
    unittest.main(verbosity=1)
