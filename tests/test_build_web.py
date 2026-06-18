# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from build_web import extract_yaml, markdown_to_html, count_words

class TestBuildWeb(unittest.TestCase):
    def test_extract_yaml_valid(self):
        content = "---\ntitle: 測試章節\n---\n測試內容"
        metadata, body = extract_yaml(content)
        self.assertEqual(metadata.get("title"), "測試章節")
        self.assertEqual(body.strip(), "測試內容")

    def test_markdown_to_html_paragraphs(self):
        content = "第一段\n\n第二段\n\n### 1\n\n第三段"
        html = markdown_to_html(content)
        self.assertIn("<p>第一段</p>", html)
        self.assertIn("<p>第二段</p>", html)
        self.assertIn('<h3 class="section-divider">1</h3>', html)

    def test_count_words(self):
        content = "這是一段測試中文內容。And English word 123."
        # 中文(10) + 英文(3) + 數字(1) = 14
        self.assertEqual(count_words(content), 14)

if __name__ == '__main__':
    unittest.main()
