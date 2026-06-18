#!/usr/bin/env python3
import os
import re
import sys

def count_words(content: str) -> int:
    """
    Counts words in the content.
    - Each Chinese character counts as 1 word.
    - Each English word counts as 1 word.
    - Continuous digits are also counted as 1 word.
    """
    chinese_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]', content)
    english_words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", content)
    numbers = re.findall(r"\d+", content)
    return len(chinese_chars) + len(english_words) + len(numbers)

def extract_yaml_frontmatter(content: str):
    """
    Extracts YAML front matter and body content.
    """
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

def main():
    chapters_dir = "chapters"
    output_file = "novel_full.md"
    
    if not os.path.exists(chapters_dir):
        print(f"Error: Directory '{chapters_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.startswith("chapter_") and f.endswith(".md")])
    
    if not chapter_files:
        print("Error: No chapter files found.", file=sys.stderr)
        sys.exit(1)
        
    compiled_chapters = []
    toc = []
    
    for filename in chapter_files:
        filepath = os.path.join(chapters_dir, filename)
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        metadata, body = extract_yaml_frontmatter(content)
        title = metadata.get("title", filename[:-3].replace("_", " ").title())
        
        # Prepare TOC entry
        anchor = title.lower().replace("：", "").replace("、", "").replace(" ", "-")
        toc.append(f"- [{title}](#{anchor})")
        
        compiled_chapters.append((title, body))
        
    # Build the full content
    full_markdown = []
    full_markdown.append("# 《雪與鋼琴的邊境》\n")
    full_markdown.append("## 目錄\n")
    for entry in toc:
        full_markdown.append(entry)
    full_markdown.append("\n---\n")
    
    for title, body in compiled_chapters:
        full_markdown.append(f"\n## {title}\n")
        full_markdown.append(body.strip())
        full_markdown.append("\n")
        
    full_content = "\n".join(full_markdown)
    
    # Calculate word count (excluding title and TOC)
    # We will compute word count on the compiled body content
    body_only = "\n".join(body for _, body in compiled_chapters)
    total_words = count_words(body_only)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"Compilation finished successfully.")
    print(f"Compiled {len(compiled_chapters)} chapters into '{output_file}'.")
    print(f"Total word count of novel body: {total_words} words.")
    
    if total_words < 100000:
        print(f"Warning: Word count ({total_words}) is below 100,000 words.")
        sys.exit(1)
    else:
        print("Verification PASSED: Word count is 100,000+ words.")

if __name__ == "__main__":
    main()
