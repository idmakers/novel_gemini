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

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>《雪與鋼琴的邊境》互動式小說閱讀器</title>
    <style>
        :root[data-theme="silver"] {
            --bg-color: #f7f9fa;
            --text-color: #2b303c;
            --title-color: #1a1e29;
            --accent-color: #3b82f6;
            --panel-bg: rgba(255, 255, 255, 0.75);
            --panel-border: rgba(0, 0, 0, 0.08);
            --card-shadow: rgba(0, 0, 0, 0.04);
            --btn-bg: rgba(255, 255, 255, 0.85);
            --divider-color: rgba(0, 0, 0, 0.06);
            --snow-color: rgba(255, 255, 255, 0.8);
        }
        :root[data-theme="warm"] {
            --bg-color: #fdf6e3;
            --text-color: #5b4636;
            --title-color: #3f2d21;
            --accent-color: #b58900;
            --panel-bg: rgba(253, 246, 227, 0.8);
            --panel-border: rgba(91, 70, 54, 0.15);
            --card-shadow: rgba(91, 70, 54, 0.06);
            --btn-bg: rgba(253, 246, 227, 0.9);
            --divider-color: rgba(91, 70, 54, 0.1);
            --snow-color: rgba(181, 137, 0, 0.15);
        }
        :root[data-theme="dark"] {
            --bg-color: #1e2430;
            --text-color: #a0a8b6;
            --title-color: #e2e8f0;
            --accent-color: #38bdf8;
            --panel-bg: rgba(30, 36, 48, 0.85);
            --panel-border: rgba(255, 255, 255, 0.08);
            --card-shadow: rgba(0, 0, 0, 0.3);
            --btn-bg: rgba(30, 36, 48, 0.9);
            --divider-color: rgba(255, 255, 255, 0.08);
            --snow-color: rgba(255, 255, 255, 0.4);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: Georgia, Cambria, "Noto Serif TC", "Songti TC", "PMingLiU", serif;
            transition: background-color 0.4s ease, color 0.4s ease;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* 雪花飄落背景 */
        .snow-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        }
        .snowflake {
            position: absolute;
            top: -10px;
            color: var(--snow-color);
            user-select: none;
            font-size: 1rem;
            animation: fall linear infinite;
            transition: color 0.4s ease;
        }

        @keyframes fall {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(105vh) rotate(360deg);
                opacity: 0;
            }
        }

        /* 閱讀主體區域 */
        .reader-wrapper {
            position: relative;
            z-index: 2;
            max-width: 800px;
            margin: 0 auto;
            padding: 60px 24px 120px 24px;
        }

        header {
            margin-bottom: 3rem;
            border-bottom: 1px solid var(--divider-color);
            padding-bottom: 20px;
            text-align: center;
        }

        .novel-main-title {
            font-size: 1.2rem;
            font-weight: normal;
            letter-spacing: 2px;
            color: var(--accent-color);
            margin-bottom: 10px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .chapter-title {
            font-size: 2rem;
            color: var(--title-color);
            font-weight: normal;
            margin-top: 10px;
        }

        .reading-content {
            line-height: 1.9;
            text-align: justify;
        }

        .reading-content p {
            margin-bottom: 1.8rem;
            text-indent: 2em;
        }

        .reading-content h3.section-divider {
            text-align: center;
            font-size: 1.3rem;
            font-weight: normal;
            margin: 3rem 0;
            color: var(--accent-color);
            letter-spacing: 4px;
        }
        
        .reading-content h2.chapter-subtitle {
            text-align: center;
            font-size: 1.5rem;
            font-weight: normal;
            margin: 2.5rem 0;
            color: var(--title-color);
        }

        /* 浮動按鈕 */
        .floating-menu-btn {
            position: fixed;
            top: 24px;
            right: 24px;
            z-index: 100;
            background: var(--btn-bg);
            border: 1px solid var(--panel-border);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            padding: 10px 18px;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 4px 20px var(--card-shadow);
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        .floating-menu-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        }

        /* 磨砂玻璃選單面板 */
        .sidebar-panel {
            position: fixed;
            top: 0;
            right: -350px;
            width: 320px;
            height: 100vh;
            background: var(--panel-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-left: 1px solid var(--panel-border);
            box-shadow: -10px 0 30px var(--card-shadow);
            z-index: 200;
            padding: 30px 24px;
            display: flex;
            flex-direction: column;
            gap: 25px;
            transition: right 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .sidebar-panel.open {
            right: 0;
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--divider-color);
            padding-bottom: 15px;
        }
        .panel-header h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--title-color);
        }
        .close-btn {
            background: none;
            border: none;
            font-size: 1.4rem;
            cursor: pointer;
            color: var(--text-color);
            opacity: 0.7;
            transition: opacity 0.2s;
        }
        .close-btn:hover {
            opacity: 1;
        }

        .setting-section-title {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-color);
            opacity: 0.6;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: block;
        }

        /* 主題選擇器 */
        .theme-selector {
            display: flex;
            gap: 12px;
        }
        .theme-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            transition: transform 0.2s;
            outline: none;
        }
        .theme-btn:hover {
            transform: scale(1.1);
        }
        .theme-btn.active {
            box-shadow: 0 0 0 2px var(--bg-color), 0 0 0 4px var(--accent-color);
        }
        #theme-silver { background-color: #f7f9fa; border: 1px solid #ccc; }
        #theme-warm { background-color: #fdf6e3; border: 1px solid #ccc; }
        #theme-dark { background-color: #1e2430; border: 1px solid #555; }

          /* 字型調整 */
          .font-adjuster {
              display: flex;
              align-items: center;
              gap: 15px;
          }
          .font-btn {
              flex: 1;
              padding: 6px;
              border: 1px solid var(--panel-border);
              background: var(--btn-bg);
              color: var(--text-color);
              cursor: pointer;
              border-radius: 6px;
              font-size: 0.9rem;
              transition: background-color 0.2s;
          }
          .font-btn:hover {
              background-color: var(--divider-color);
          }
          .font-size-val {
              font-size: 0.95rem;
              font-weight: 600;
              min-width: 60px;
              text-align: center;
          }

          /* 目錄章節列表 */
          .chapter-list {
              flex-grow: 1;
              overflow-y: auto;
              display: flex;
              flex-direction: column;
              gap: 6px;
              padding-right: 4px;
          }
          .chapter-item {
              padding: 10px 12px;
              border-radius: 8px;
              cursor: pointer;
              text-decoration: none;
              color: var(--text-color);
              font-size: 0.9rem;
              transition: all 0.2s;
              display: block;
              border-left: 2px solid transparent;
          }
          .chapter-item:hover {
              background-color: var(--divider-color);
          }
          .chapter-item.active {
              color: var(--accent-color);
              font-weight: 600;
              border-left-color: var(--accent-color);
              background-color: var(--divider-color);
          }

          /* 背景遮罩 */
          .panel-overlay {
              position: fixed;
              top: 0;
              left: 0;
              width: 100vw;
              height: 100vh;
              background: rgba(0,0,0,0.1);
              z-index: 150;
              opacity: 0;
              pointer-events: none;
              transition: opacity 0.4s ease;
          }
          .panel-overlay.open {
              opacity: 1;
              pointer-events: auto;
          }

          /* 自適應 */
          @media (max-width: 480px) {
              .sidebar-panel {
                  width: 100%;
                  right: -100%;
              }
              .reader-wrapper {
                  padding: 80px 16px 80px 16px;
              }
              .chapter-title {
                  font-size: 1.6rem;
              }
          }
      </style>
  </head>
  <body>
      <!-- 雪花背景 -->
      <div class="snow-container" id="snow-container"></div>

      <!-- 浮動目錄按鈕 -->
      <button class="floating-menu-btn" onclick="toggleSidebar()">
          <span>☰</span> <span>目錄與設定</span>
      </button>

      <!-- 側邊選單 -->
      <div class="panel-overlay" id="panel-overlay" onclick="toggleSidebar()"></div>
      <div class="sidebar-panel" id="sidebar-panel">
          <div class="panel-header">
              <h3>目錄與設定</h3>
              <button class="close-btn" onclick="toggleSidebar()">✕</button>
          </div>

          <div>
              <span class="setting-section-title">主題配色</span>
              <div class="theme-selector">
                  <button class="theme-btn" id="theme-silver" onclick="setTheme('silver')"></button>
                  <button class="theme-btn" id="theme-warm" onclick="setTheme('warm')"></button>
                  <button class="theme-btn" id="theme-dark" onclick="setTheme('dark')"></button>
              </div>
          </div>

          <div>
              <span class="setting-section-title">字型大小</span>
              <div class="font-adjuster">
                  <button class="font-btn" onclick="adjustFont(-0.1)">A-</button>
                  <span class="font-size-val" id="font-size-val">1.1rem</span>
                  <button class="font-btn" onclick="adjustFont(0.1)">A+</button>
              </div>
          </div>

          <div style="flex-grow: 1; display: flex; flex-direction: column; overflow: hidden;">
              <span class="setting-section-title">章節目錄</span>
              <div class="chapter-list" id="chapter-list"></div>
          </div>
      </div>

      <!-- 閱讀器主體 -->
      <div class="reader-wrapper">
          <header>
              <h1 class="novel-main-title">《雪與鋼琴的邊境》</h1>
              <div class="chapter-title" id="chapter-header-title">載入中...</div>
          </header>
          <main class="reading-content" id="reading-content"></main>
      </div>

      <script>
          // 由建置腳本注入的章節資料
          const NOVEL_DATA = {{NOVEL_DATA}};

          let currentChapterIndex = 0;
          let currentFontSize = 1.1;
          let currentTheme = 'silver';
          let isScrollingToPrevious = false;

          // 初始化雪花動畫
          function createSnow() {
              const container = document.getElementById('snow-container');
              const snowflakeCount = window.innerWidth < 480 ? 8 : 15;
              container.innerHTML = '';
              for (let i = 0; i < snowflakeCount; i++) {
                  const flake = document.createElement('div');
                  flake.className = 'snowflake';
                  flake.innerText = '❄';
                  resetSnowflake(flake, true);
                  container.appendChild(flake);
              }
          }

          function resetSnowflake(flake, init = false) {
              const size = 0.5 + Math.random() * 1.2;
              flake.style.fontSize = size + 'rem';
              flake.style.left = Math.random() * 100 + 'vw';
              flake.style.opacity = 0.2 + Math.random() * 0.6;
              
              const duration = 8 + Math.random() * 12;
              flake.style.animationDuration = duration + 's';
              flake.style.animationDelay = init ? '-' + (Math.random() * duration) + 's' : '0s';
              
              if (!init) {
                  // 強制重繪以重啟動畫
                  flake.style.animation = 'none';
                  flake.offsetHeight; // trigger reflow
                  flake.style.animation = '';
              }
          }

          // 監聽雪花動畫結束並重置
          document.addEventListener('animationiteration', (e) => {
              if (e.target.className === 'snowflake') {
                  resetSnowflake(e.target);
              }
          });

          // 側邊欄控制
          function toggleSidebar() {
              document.getElementById('sidebar-panel').classList.toggle('open');
              document.getElementById('panel-overlay').classList.toggle('open');
          }

          // 渲染目錄列表
          function renderChapterList() {
              const listContainer = document.getElementById('chapter-list');
              listContainer.innerHTML = '';
              NOVEL_DATA.forEach((chapter, index) => {
                  const item = document.createElement('a');
                  item.className = 'chapter-item' + (index === currentChapterIndex ? ' active' : '');
                  item.innerText = chapter.title;
                  item.onclick = () => {
                      loadChapter(index);
                      toggleSidebar();
                  };
                  listContainer.appendChild(item);
              });
          }

          // 載入指定章節
          function loadChapter(index, restoreScrollPercent = 0) {
              if (index < 0 || index >= NOVEL_DATA.length) return;
              currentChapterIndex = index;
              
              // 更新目錄選取狀態
              const items = document.querySelectorAll('.chapter-item');
              items.forEach((item, idx) => {
                  if (idx === index) item.classList.add('active');
                  else item.classList.remove('active');
              });

              // 更新標題與內文
              document.getElementById('chapter-header-title').innerText = NOVEL_DATA[index].title;
              const contentContainer = document.getElementById('reading-content');
              contentContainer.innerHTML = NOVEL_DATA[index].content;

              // 記錄 localStorage
              localStorage.setItem('novel_current_chapter', index);

              // 處理滾動
              if (restoreScrollPercent > 0) {
                  isScrollingToPrevious = true;
                  setTimeout(() => {
                      const totalScroll = document.documentElement.scrollHeight - window.innerHeight;
                      window.scrollTo({
                          top: restoreScrollPercent * totalScroll,
                          behavior: 'smooth'
                      });
                      setTimeout(() => { isScrollingToPrevious = false; }, 800);
                  }, 150);
              } else {
                  window.scrollTo({ top: 0, behavior: 'instant' });
                  localStorage.setItem('novel_scroll_percent', 0);
              }
          }

          // 設定主題
          function setTheme(theme) {
              currentTheme = theme;
              document.documentElement.setAttribute('data-theme', theme);
              localStorage.setItem('novel_theme', theme);
              
              const btns = document.querySelectorAll('.theme-btn');
              btns.forEach(btn => {
                  if (btn.id === 'theme-' + theme) btn.classList.add('active');
                  else btn.classList.remove('active');
              });
          }

          // 調整字型大小
          function adjustFont(delta) {
              currentFontSize = Math.max(0.8, Math.min(2.0, currentFontSize + delta));
              document.getElementById('reading-content').style.fontSize = currentFontSize + 'rem';
              document.getElementById('font-size-val').innerText = currentFontSize.toFixed(1) + 'rem';
              localStorage.setItem('novel_font_size', currentFontSize);
          }

          // 監聽滾動事件保存進度
          window.addEventListener('scroll', () => {
              if (isScrollingToPrevious) return;
              const totalScroll = document.documentElement.scrollHeight - window.innerHeight;
              if (totalScroll <= 0) return;
              const scrollPercent = window.scrollY / totalScroll;
              localStorage.setItem('novel_scroll_percent', scrollPercent);
          });

          // 初始化
          window.onload = () => {
              createSnow();
              window.addEventListener('resize', createSnow);

              // 讀取進度與偏好
              const savedTheme = localStorage.getItem('novel_theme') || 'silver';
              setTheme(savedTheme);

              const savedFontSize = localStorage.getItem('novel_font_size');
              if (savedFontSize) {
                  currentFontSize = parseFloat(savedFontSize);
                  document.getElementById('reading-content').style.fontSize = currentFontSize + 'rem';
                  document.getElementById('font-size-val').innerText = currentFontSize.toFixed(1) + 'rem';
              }

              const savedChapter = localStorage.getItem('novel_current_chapter');
              const savedScroll = localStorage.getItem('novel_scroll_percent');
              
              const initChapter = savedChapter ? parseInt(savedChapter) : 0;
              const initScroll = savedScroll ? parseFloat(savedScroll) : 0;

              renderChapterList();
              loadChapter(initChapter, initScroll);
          };
      </script>
  </body>
  </html>
"""

def main_build():
    chapters_dir = "chapters"
    output_file = "index.html"
    
    if not os.path.exists(chapters_dir):
        print(f"Error: Directory '{chapters_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    chapter_files = sorted([f for f in os.listdir(chapters_dir) if f.startswith("chapter_") and f.endswith(".md")])
    
    if not chapter_files:
        print("Error: No chapter files found in chapters/.", file=sys.stderr)
        sys.exit(1)
        
    novel_chapters = []
    total_words = 0
    
    for filename in chapter_files:
        filepath = os.path.join(chapters_dir, filename)
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        metadata, body = extract_yaml(content)
        title = metadata.get("title", filename[:-3].replace("_", " ").title())
        
        chapter_words = count_words(body)
        total_words += chapter_words
        
        # 將 markdown 轉成 html段落
        html_content = markdown_to_html(body)
        
        novel_chapters.append({
            "id": filename[:-3],
            "title": title,
            "content": html_content
        })
    
    # 輸出 JSON 字串並注入模板
    novel_data_json = json.dumps(novel_chapters, ensure_ascii=False, indent=4)
    full_html = HTML_TEMPLATE.replace('{{NOVEL_DATA}}', novel_data_json)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"Build success! Output file: '{output_file}'")
    print(f"Chapters processed: {len(novel_chapters)}")
    print(f"Total word count: {total_words}")
    
    # 驗證字數是否大於 100,000 字，符合 compile_novel.py 規範
    if total_words < 100000:
        print(f"Warning: Word count ({total_words}) is below 100,000 words.", file=sys.stderr)
        sys.exit(1)
    else:
        print("Verification PASSED: Word count is 100,000+ words.")

if __name__ == "__main__":
    main_build()
