# 《雪與鋼琴的邊境》互動式小說閱讀器設計規格書

> **目標：** 為小說《雪與鋼琴的邊境》建置一個精美、互動性強的白銀雪原極簡風網頁閱讀器，支援部署至 GitHub Pages (github.io) 且能直接在本地雙擊打開。

---

## 1. 系統架構

採用**靜態打包單網頁應用 (Single-File Compiled SPA)** 的技術方案：
1. **內容來源**：位於 `chapters/chapter_01.md` 至 `chapter_10.md` 的 Markdown 原始檔案。
2. **建置腳本**：撰寫 `scripts/build_web.py`，讀取所有章節的 Markdown 檔案，將其解析為段落 HTML 並打包成 JSON 格式，最終生成根目錄下的 `index.html`。
3. **網頁架構**：生成的 `index.html` 包含完整的 HTML、CSS 設計系統與 JavaScript 邏輯，並直接嵌入小說的章節資料，以實現免網路請求、免 CORS 限制、本地雙擊直接開啟的目標。

---

## 2. 視覺設計系統 (白銀雪原極簡風)

1. **色彩系統 (Theme Colors)**：
   - **雪白 (Silver Snow - 預設)**：背景 `#f7f9fa`，文字 `#2b303c`，標題 `#1a1e29`，微光冰藍 `#3b82f6`。
   - **暖黃 (Warm Paper)**：背景 `#fdf6e3`，文字 `#5b4636`，標題 `#3f2d21`。
   - **靜謐夜 (Midnight Blue)**：背景 `#1e2430`，文字 `#a0a8b6`，標題 `#e2e8f0`。
2. **磨砂玻璃效果 (Glassmorphism)**：
   - 浮動面板與按鈕使用 `backdrop-filter: blur(15px); background: rgba(255, 255, 255, 0.75); border: 1px solid rgba(255, 255, 255, 0.4);` 質感。
3. **雪花微動畫 (Ambient Snow Animation)**：
   - 在背景中加入 5-10 個隨機位置的半透明雪花元素，利用 CSS `keyframes` 動畫實現緩慢飄落與自轉，並在深色模式下有更好的對比度。
4. **字體與排版**：
   - 預設字體：`Georgia, Cambria, "Noto Serif TC", "Songti TC", "PMingLiU", serif`（優雅中文襯線體）。
   - 正文字體大小預設 `1.1rem`，行高 `1.8`，段落間距 `1.5rem`，首行縮排 `2em`。

---

## 3. 核心功能與組件

1. **沉浸式閱讀主體 (Focus Reading Area)**：
   - 單欄置中排版，最大寬度 `800px`，隨螢幕寬度自適應縮小左右邊距。
   - 頂部顯示當前章節標題。
2. **浮動控制按鈕 (Floating Control Button)**：
   - 常駐於網頁右上角，點擊可滑出「目錄與設定面板」。
3. **目錄與設定面板 (Sidebar Panel)**：
   - **章節目錄**：列出第一章至第十章，點擊後平滑切換內文，並自動將閱讀區域滾動至頂部。
   - **字型縮放**：提供字體放大（A+）與縮小（A-）按鈕，範圍在 `0.8rem` 到 `2.0rem` 之間。
   - **主題切換**：點擊切換「雪白」、「暖黃」、「靜謐夜」三種主題。
4. **閱讀進度保存 (Progress Save & Restore)**：
   - 每次切換章節或滾動頁面時，利用 `localStorage` 記錄當前閱讀的章節索引與滾動比例。
   - 當讀者重新開啟網頁時，自動讀取進度，載入對應章節並平滑滾動到上次的閱讀位置。

---

## 4. 部署與測試方案

1. **GitHub Pages 部署**：
   - 將產生的 `index.html` 放置於專案根目錄。
   - 推送至 GitHub 後，在 Repository 的 Settings -> Pages 中啟動 GitHub Pages，即可直接在 `https://<username>.github.io/<repo-name>/` 執行。
2. **測試計劃**：
   - **格式驗證**：確保生成的 `index.html` 在所有瀏覽器（Chrome, Safari, Edge, Firefox）皆能正常運作且排版無跑版。
   - **本地端測試**：不啟動本地伺服器，直接在檔案瀏覽器雙擊 `index.html` (使用 `file://` 協定)，驗證是否能正常載入內文、調整字體與切換主題。
   - **RWD 自適應測試**：調整瀏覽器視窗寬度，模擬手機 (375px) 與平板 (768px)，確保浮動面板不遮擋內容且字體大小適中。
