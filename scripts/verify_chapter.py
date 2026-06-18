#!/usr/bin/env python3
import argparse
import sys
import os
import re

def count_words(content: str) -> int:
    """
    Counts words in the content.
    - Each Chinese character (CJK Unified Ideographs) counts as 1 word.
    - Each English word (continuous alphabetic characters, including apostrophes) counts as 1 word.
    - Continuous digits are also counted as 1 word (since they represent numbers in text).
    """
    # Match CJK unified ideographs (Chinese characters)
    # Range \u4e00-\u9fff covers common Chinese characters.
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    
    # Match English words (including words with apostrophes like "don't" or "it's")
    english_words = re.findall(r'\b[a-zA-Z]+(?:\'[a-zA-Z]+)?\b', content)
    
    # Match numbers (continuous digits)
    numbers = re.findall(r'\b\d+\b', content)
    
    return len(chinese_chars) + len(english_words) + len(numbers)

def main():
    parser = argparse.ArgumentParser(description="Verify novel chapter word count and keywords.")
    parser.add_argument("filepath", help="Path to the chapter markdown file")
    parser.add_argument(
        "--min-words", 
        type=int, 
        default=8000, 
        help="Minimum required word count (default: 8000)"
    )
    parser.add_argument(
        "--keywords", 
        nargs='+', 
        default=[], 
        help="List of required keywords that must be present in the chapter"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.filepath):
        print(f"Error: File '{args.filepath}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(args.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Failed to read file '{args.filepath}': {e}", file=sys.stderr)
        sys.exit(1)
        
    actual_words = count_words(content)
    
    errors = []
    
    # Check word count
    if actual_words < args.min_words:
        errors.append(f"Word count check failed. Required: at least {args.min_words} words. Actual: {actual_words} words.")
        
    # Check keywords
    missing_keywords = []
    for kw in args.keywords:
        if kw not in content:
            missing_keywords.append(kw)
            
    if missing_keywords:
        errors.append(f"Keyword check failed. Missing keywords: {', '.join(repr(k) for k in missing_keywords)}")
        
    if errors:
        print("Verification FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Verification PASSED")
    print(f"Actual word count: {actual_words}")

if __name__ == "__main__":
    main()
