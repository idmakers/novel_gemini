# 《雪與鋼琴的邊境》小說創作實現計劃

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推薦）或 superpowers:executing-plans 逐任務實現此計劃。步驟使用複選框（`- [ ]`）語法來跟蹤進度。

**目標：** 創作一部融合月姬、86、巨人、白相2與物語系列價值觀的純愛Boy Meets Girl十萬字小說《雪與鋼琴的邊境》。

**架構：** 將小說分為10章，每章以 Markdown 格式單獨寫入 `chapters/chapter_XX.md`，字數為 8,000 至 12,000 中文字。最終彙整至 `novel_full.md`，總字數達到 100,000 字以上。

**技術棧：** Markdown、Python（字數統計與格式驗證）

---

## 預備工作

在開始寫作之前，我們需要建立一個 Python 字數統計與關鍵詞驗證腳本，用於對各章節進行自動化驗證。

### 任務 0：建立驗證腳本
* **文件：**
  * 創建：`scripts/verify_chapter.py`
* - [ ] **步驟 1：編寫驗證代碼**
  * 在 `scripts/verify_chapter.py` 中寫入字數統計與關鍵詞檢查邏輯。
* - [ ] **步驟 2：運行測試驗證**
  * 運行：`python3 scripts/verify_chapter.py --help`
  * 預期：成功輸出幫助信息。
* - [ ] **步驟 3：Commit**
  * 運行：`git add scripts/verify_chapter.py && git commit -m "chore: add chapter verification script"`

---

## 小說章節創作

各章節寫作要求：
1. 字數必須達到 **8,000字至12,000字** 區間。
2. 完美融入相應視角的語氣、意識流與對白風格（修亞：物語式的自嘲與辯駁；塞西莉雅：白相式的糾結與高潔；蕾拉：戰場的寫實與毒舌）。

### 任務 1：創作第一章《鐵翼、暴雪與第一聲和弦》
* **文件：**
  * 創建：`chapters/chapter_01.md`
* - [ ] **步驟 1：寫作第一章內容**
  * 描寫修亞在暴風雪外圈駕駛機關「影縫」作戰，同化詛咒導致嗅覺喪失。接通「共鳴儀」，聽見塞西莉雅彈奏的鋼琴聲。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_01.md --min-words 8000 --keywords "修亞" "塞西莉雅" "影縫" "共鳴儀"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_01.md && git commit -m "feat: write chapter 1"`

### 任務 2：創作第二章《玻璃溫室中的白銀之琴》
* **文件：**
  * 創建：`chapters/chapter_02.md`
* - [ ] **步驟 1：寫作第二章內容**
  * 塞西莉雅視角。牆內優雅而冰冷的生活，高牆「白銀之門」的宏偉。她被指派為「守望者」，接入修亞的心靈連結，被其刺耳卻孤獨的聲音震撼，開始為他彈琴。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_02.md --min-words 8000 --keywords "塞西莉雅" "修亞" "共鳴儀" "鋼琴"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_02.md && git commit -m "feat: write chapter 2"`

### 任務 3：創作第三章《共死之人的體溫》
* **文件：**
  * 創建：`chapters/chapter_03.md`
* - [ ] **步驟 1：寫作第三章內容**
  * 修亞視角。描寫牆外防護隊前線基地。修亞與蕾拉的物語式日常毒舌互損與無奈的共死命運。蕾拉右臂金屬化（怪異同化）加劇。一場遭遇戰，修亞為了救蕾拉強行過載，失去了對「溫暖體溫」的感覺。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_03.md --min-words 8000 --keywords "修亞" "蕾拉" "金屬化" "怪異"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_03.md && git commit -m "feat: write chapter 3"`

### 任務 4：創作第四章《無法傳達的白色旋律》
* **文件：**
  * 創建：`chapters/chapter_04.md`
* - [ ] **步驟 1：寫作第四章內容**
  * 塞西莉雅視角。透過共鳴儀發現修亞忘記了香氣、溫度的概念。她試圖向他描述牆內的花草與朝陽，卻意識到彼此處於完全不同的世界。她對修亞產生了帶有愧疚感與救贖欲的執著。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_04.md --min-words 8000 --keywords "塞西莉雅" "修亞" "琴聲" "愧疚"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_04.md && git commit -m "feat: write chapter 4"`

### 任務 5：創作第五章《鏽蝕雙重奏的撕裂》
* **文件：**
  * 創建：`chapters/chapter_05.md`
* - [ ] **步驟 1：寫作第五章內容**
  * 修亞視角。前線爆發大規模怪異潮。蕾拉機體受創，修亞在戰場中極度疲憊，精神防線崩潰。塞西莉雅透過琴聲試圖拉回他，但修亞在「反轉衝動」中產生幻覺，險些在駕駛艙中扼殺了前來救援的蕾拉。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_05.md --min-words 8000 --keywords "修亞" "蕾拉" "琴聲" "反轉衝動"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_05.md && git commit -m "feat: write chapter 5"`

### 任務 6：創作第六章《琉璃壁壘下的骸骨》
* **文件：**
  * 創建：`chapters/chapter_06.md`
* - [ ] **步驟 1：寫作第六章內容**
  * 塞西莉雅視角。她利用家族權限調查「箱庭」的能源中樞，發現牆內無憂無慮的高雅生活與屏障，全靠吸乾牆外戰死駕駛員的「怪異靈魂」來維持。塞西莉雅信念崩塌。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_06.md --min-words 8000 --keywords "塞西莉雅" "箱庭" "能源" "靈魂"`
  * 預期：輸出 `Verification PASSED` 與字數.
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_06.md && git commit -m "feat: write chapter 6"`

### 任務 7：創作第七章《背叛的冰冷雪夜》
* **文件：**
  * 創建：`chapters/chapter_07.md`
* - [ ] **步驟 1：寫作第七章內容**
  * 修亞視角。聽覺受損，再也聽不見塞西莉雅的高音。寒冬深夜的整備庫中，修亞與蕾拉抱團取暖。在將死的預感與對塞西莉雅純潔愛意的負罪感中，修亞與蕾拉接吻。白相2式的三角關係達到冰點。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_07.md --min-words 8000 --keywords "修亞" "蕾拉" "塞西莉雅" "接吻"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_07.md && git commit -m "feat: write chapter 7"`

### 任務 8：創作第八章《箱庭破裂的序曲》
* **文件：**
  * 創建：`chapters/chapter_08.md`
* - [ ] **步驟 1：寫作第八章內容**
  * 雙視角交織。帝國高層下達命令犧牲修亞第一小隊進行誘敵防線充能。塞西莉雅冒死在共鳴儀中發出預警並計劃反叛。修亞與蕾拉在廢墟基地中與眾人達成共識——與其作為零件死在鐵籠裡，不如擊碎高牆。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_08.md --min-words 8000 --keywords "修亞" "塞西莉雅" "蕾拉" "高牆"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_08.md && git commit -m "feat: write chapter 8"`

### 任務 9：創作第九章《砸碎樊籠的叛逆》
* **文件：**
  * 創建：`chapters/chapter_09.md`
* - [ ] **步驟 1：寫作第九章內容**
  * 戰鬥高潮。修亞與蕾拉帶領殘部引導怪異巨獸回衝「白銀之門」與「黃金之門」。城牆破裂。修亞的同化率達到極限，開始變化為巨大而美麗的怪異巨獸。蕾拉站在他的肩頭，與他並肩破城。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_09.md --min-words 8000 --keywords "修亞" "蕾拉" "巨獸" "破城"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_09.md && git commit -m "feat: write chapter 9"`

### 任務 10：創作第十章《雪原盡頭的遙遠奏鳴曲》
* **文件：**
  * 創建：`chapters/chapter_10.md`
* - [ ] **步驟 1：寫作第十章內容**
  * 尾聲與餘音。帝國崩潰，無牆的新時代到來。塞西莉雅在廢墟的鋼琴前，演奏最後的送行樂章。在無邊的雪原上，徹底化為巨獸的修亞馱著金屬化大半的蕾拉，走向那傳說中沒有冰凍、自由的「海」。
* - [ ] **步驟 2：運行字數與關鍵詞驗證**
  * 運行：`python3 scripts/verify_chapter.py chapters/chapter_10.md --min-words 8000 --keywords "塞西莉雅" "修亞" "蕾拉" "海"`
  * 預期：輸出 `Verification PASSED` 與字數。
* - [ ] **步驟 3：Commit**
  * 運行：`git add chapters/chapter_10.md && git commit -m "feat: write chapter 10"`

---

## 彙整與最終驗證

### 任務 11：小說彙整與總字數確認
* **文件：**
  * 創建：`novel_full.md`
* - [ ] **步驟 1：彙整所有章節**
  * 使用腳本將所有 `chapters/chapter_XX.md` 的內容拼接至 `novel_full.md`，並加上大標題與目錄。
* - [ ] **步驟 2：運行最終總字數驗證**
  * 運行統計：驗證 `novel_full.md` 總字數是否大於 100,000 字。
* - [ ] **步驟 3：Commit**
  * 運行：`git add novel_full.md && git commit -m "feat: compile and verify full novel"`
