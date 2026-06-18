#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import json

def count_words(content: str) -> int:
    chinese_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', content)
    english_words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", content)
    numbers = re.findall(r"\d+", content)
    return len(chinese_chars) + len(english_words) + len(numbers)

def extract_yaml(content: str):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, flags=re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body = content[match.end():]
        metadata = {}
        for line in yaml_text.split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                metadata[k.strip()] = v.strip()
        return metadata, body
    return {}, content

def markdown_to_html(content: str) -> str:
    lines = content.strip().split('\n\n')
    html_blocks = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('###'):
            header_val = line.replace('###', '').strip()
            html_blocks.append(f'<h3 class="section-divider">{header_val}</h3>')
        elif line.startswith('##'):
            header_val = line.replace('##', '').strip()
            html_blocks.append(f'<h2 class="chapter-subtitle">{header_val}</h2>')
        else:
            # 將換行 \n 轉為 <br>
            formatted_line = line.replace('\n', '<br>')
            html_blocks.append(f'<p>{formatted_line}</p>')
    return '\n'.join(html_blocks)
