# 整包 Session Handoff：關西之旅與旅程系統

- **整理日期**：2026-09-27（台北）
- **來源**：Claude 雲端工作階段（Cowork），期間也交接過 ChatGPT 的行程稿。
- **用途**：任何人（你自己、Claude Code，或新的 Claude 對話）讀完這份文件，就能完整接手：
  - 目前的行程與決策
  - 已建好的系統
  - 資料來源與踩過的坑
  - 尚未完成的事

相關文件：
- `HANDOFF-claude-code.md`：Claude Code 安裝與 `/plan-trip` 用法
- `CLAUDE.md`：專案規則
- `trips/README.md`：行程資料結構

---

## 0. 所有入口一覽

| 項目 | 位置 |
|---|---|
| GitHub repo | https://github.com/peterlee7410/flight-tracker_1（branch `main`，Pages 從 root 發佈） |
| 關西追蹤網站 | https://peterlee7410.github.io/flight-tracker_1/ |
| 旅程產生器（GitHub 版） | https://peterlee7410.github.io/flight-tracker_1/planner/ |
| 旅程產生器（Claude Artifact 版，可直接呼叫 Claude、雲端儲存） | https://claude.ai/artifact/UarNLFkCboC8ETG1gZi3JR（只有本人可開） |
| 旅遊技能 | claude.ai 已儲存 `japan-trip-planner`；repo 內副本在 `.claude/skills/japan-trip-planner/SKILL.md` |
| Claude Code 指令 | `/plan-trip`（`.claude/commands/plan-trip.md`）加上 5 個 agent（`.claude/agents/`） |
| 推播 | Telegram，使用 GitHub Secrets `TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`；變數 `NOTIFY_EVERY_RUN=1` 時每次都推播 |
| 排程 | GitHub Actions `機票查價`，cron `47 0,12 * * *`，也就是台北 08:47 與 20:47。Claude 端的排程任務已依你的要求關閉 |

---

## 1. 需求演進（依時間順序）

1. **追蹤機票**
   - 桃園⇄大阪關西，2026-10-14 去、10-19 回，2 位成人。
   - LCC 或傳統航空都可以。
   - 行李：去程 1 件、回程 2 件托運。
   - 目標全員 NT$30,000 內，越便宜越好。
2. **加時間限制**
   - 去程不晚於 16:00 抵達 KIX。
   - 回程不早於 10:00 起飛。
   - 另外比較「LCC 去、傳統航空回」的組合。
3. **不耗 API**：改成獨立網頁自動更新，用 GitHub Actions 加 Pages，不花 Claude 或 API 費用。
4. **Spyder 報錯**：找不到 `config.json`。改成程式內建預設值，並處理 asyncio 衝突。
5. **關閉 Claude 排程**：你說「幫我關」，已關。
6. **接手 ChatGPT 的行程**
   - 確認天橋立住宿（與謝荘，要性價比高、有接駁）。
   - 確認京都 Sakura Terrace The Atelier。
   - 加上圖形化動線。
7. **飯店動態比價**：比照機票，做飯店價格追蹤與提醒。
8. **納入其他候選飯店**：Il Verde、ZEQUU Annex、Kyoto Pleasant、VIA INN、APA。
9. **改以 Agoda 為主**：按鈕要能自動帶入日期與人數。
10. **晚上活動**
    - 評估清水寺夜間參拜、嵐山小火車。
    - 改成晚上去嵐山：10/16 晚上嵐山月灯路，10/17 上午補清水寺。
11. **全程費用試算**：用可訂最便宜的飯店計算，放到網頁上。
12. **淀川花火**
    - 找免費觀賞點（不要大樓觀景台）。
    - 10/17 改成姫島方案（十三側為備案）。
    - 費用試算加上付費席與免費的切換。
13. **每日電車時刻表**：標示最建議的班次、車次和月台。
14. **整合成技能**：把流程整合成旅遊技能，並評估要在 Cowork 還是 Claude Code 開發（以及是否耗 API）。
15. **通用產生器**：做一個網頁，輸入任何目的地與時間就產生整套內容。
16. **放上 GitHub**：讓遠端也能用。
17. **改用 Claude Code agent**：評估後在 repo 建好 Claude Code 設定與 handoff 文件。
18. **本文件**：整個 session 的完整交接。

---

## 2. 關西行程現況（2026-10-14 週三 至 10-19 週一，2 人）

### 2.1 機票（2026-09-27 13:46 查價，全員含行李估算）

| 組合 | 去程 | 回程 | 估價 |
|---|---|---|---|
| 最低（符合條件） | 捷星 02:30→06:05（紅眼） | 泰越捷 12:25→14:30 | NT$23,836 |
| 最低非紅眼 | 虎航 06:40→10:05 | 泰越捷 12:25 | NT$26,518 |
| LCC 去＋傳統回 | 捷星 | 中華 | 約 NT$35,091 |

- **2026-09-29 已訂：星宇 JX820 10/14 08:30 TPE→12:15 KIX；JX823 10/19 15:10 KIX→17:05 TPE（2 人）。** 機票查價已停止（`config.json` 的 `booked: true`）；以下為訂票前的查價紀錄。
- 追蹤中：追蹤頁會標示「建議現在下訂」，價格跌破門檻時發 Telegram 通知。
- 提醒條件：`alert_below` 21000、`alert_drop` 800、出發前 7 天。

### 2.2 住宿

| 晚 | 住宿 | 狀態與價格 | 重點 |
|---|---|---|---|
| 10/14 | RTI 天王寺 | **已訂**，金額由你自行填入費用試算 | HARUKA 與関空快速直達 |
| 10/15 | 天橋立荘 別館 よさの荘（與謝荘） | 未訂。じゃらん素泊 ¥14,268（「お得な10日間」到 9/29；之後約 ¥15,020），剩 3 間 | 不是溫泉。接駁約 5 分鐘，**要預約**：0772-22-3555。check-in 15:00–18:00 |
| 10/16 | Green Rich Hotel 京都駅南 | 未訂。じゃらん ¥19,280（吸菸室素泊）或 ¥22,560（禁菸含早） | 京都可訂最便宜且有獨立衛浴 |
| 10/17、10/18 | RTI 天王寺 | **已訂** | |

京都其他候選（9/27 查詢時 10/16 的狀態）：
- Sakura Terrace The Atelier：客滿，而且是共用衛浴。
- Kyoto Pleasant：客滿。
- Il Verde：¥20,400，不可退款。
- ZEQUU Annex：¥23,050，不可退款。
- VIA INN Prime 八条口、APA 京都駅前中央口：在追蹤清單中。

天橋立另一個選擇：天橋立ホテル，站前、海景，¥37,400 起。

### 2.3 每日行程（每天建議班次與月台都已放在網站上）

**10/14（三）**
- KIX → 天王寺
  - 紅眼班機：07:32 直通快速 4316M，08:24 到天王寺 18 號。
  - 虎航：11:17 関空快速 4146M，12:10 到天王寺。
- 新世界 → 難波八阪神社 → 千日前 → 道頓堀 → 心齋橋藥妝比價。

**10/15（四）**
- 天王寺 07:21 HARUKA 1002M（18 號）→ 京都 08:11（30 號）。
- 京都 08:38 はしだて1号 5081M（31 號）→ 天橋立 10:39。
- 天橋立站 ¥800 大型寄物櫃（12 格）放行李，逛智恩寺、View Land、沙洲。
- 回站搭與謝荘接駁車。

**10/16（五）**
- 接駁回站，行李寄櫃。
- 丹海巴士到伊根（單程 ¥400），搭伊根灣遊船（¥1,200），吃海鮮。
- 天橋立 15:51 はしだて6号 5086M → 京都 18:07（31 號）。
- 先到飯店放行李，京都 18:45 普通 261M（32 號）→ 嵯峨嵐山 19:02。
- **嵐山月灯路**
  - 期間 9/30–11/8，每天 18:00–21:00，最後入場 20:40。
  - 現場票 ¥1,500，17:50 起賣，只收現金。
  - 網路票 ¥2,000，透過 JR 東海「EX旅先予約」。
- 回程建議 20:17 普通 268M → 京都 20:34（32 號）；最後保底班 20:48。

**10/17（六）**
- 07:00 退房，計程車到清水寺（06:00 開門，¥500）。
- 三年坂、二年坂 → 祇園四条 → 京阪到出町柳 → 下鴨神社、糺之森、早午餐。
- 地鐵從今出川到京都，12:00 前取回行李。
- 京都 13:00 HARUKA 1029M（30 號）→ 天王寺 13:45（15 號），回 RTI 放行李。
- 御堂筋線到梅田，約 16:10 搭阪神普通車到姫島，17:00 前到淀川河堤。
- **淀川花火** 19:00–20:00，免費觀賞。
  - 12:00 起才能佔位。
  - 堤防上不能觀賞。
  - 梅田側（左岸）全面禁止觀賞。
  - 花火日阪神會加開，急行臨時停姫島。
  - 散場後姫島站會管制進站，可以走到千船站分流。
  - 備案：十三側免費區，15:30 前到。
- 付費席兩人約 ¥28,000。網頁上有「付費／免費」切換，預設免費。

**10/18（日）**
- 天王寺 08:20 大和路快速 308K（16 號）→ 奈良 08:55。
- 奈良公園、東大寺（¥800）、二月堂。
- 奈良 13:07 みやこ路快速 2626M → 宇治 13:37，逛平等院（¥700）、宇治川、抹茶。
- 宇治 16:07 みやこ路快速 2636M → 京都 16:25（10 號）。
- 京都 17:00 HARUKA 1045M（30 號）→ 天王寺 17:46，回大阪補買藥妝。

**10/19（一）**
- 天王寺 08:10 HARUKA 1007M（15 號）→ KIX 08:51，搭 12:25 航班。
- 備案：07:37 HARUKA。
- 若改搭関空快速，要坐前 4 節。

### 2.4 票券與費用

- **JR 關西廣域鐵路周遊券 5 日**：¥12,000 × 2，使用 10/15–10/19。涵蓋 HARUKA、はしだて、京都丹後鐵道、嵯峨野線、奈良線和回機場。
- **全程費用試算**（網頁可切換航班、每晚住宿、餐費等級、花火付費與否、匯率）：
  - 免費看花火：約 NT$48,971（每人約 NT$24,486）。
  - 買付費席：約 NT$54,851。
  - 以上不含 RTI 住宿費與購物。
  - 匯率以 1 JPY ≈ 0.21 TWD 計。

### 2.5 還要你自己處理的事

- [x] 訂機票：已訂星宇 JX820／JX823（2026-09-29）。10/14 建議 13:32 關空快速 4164M 到天王寺；10/19 建議 11:47 HARUKA 1021M 到機場。
- [x] 訂與謝荘（2026-09-29 已訂，10/15 15:00 入住、10/16 10:00 退房）；仍須預約接駁：0772-22-3555。
- [x] 京都 10/16：已訂 Almont Hotel Kyoto（八条東口步行約 5 分，14:00 入住、10/17 11:00 退房）。飯店查價已停止（`hotels.json` 的 `booked: true`）。
- [ ] 在 KIX 領關西廣域券時，一次劃好 HARUKA、はしだて1号、はしだて6号的指定席。
- [ ] 決定月灯路買現場票或網路票。
- [ ] 把 RTI 住宿金額填入網頁的費用試算。
- [ ] 出發前一天，用官方時刻表再確認一次班次與月台。

---

## 3. 系統架構

```
GitHub Actions（每天 2 次，免費）
 ├─ tracker.py        Google Flights（zh-TW／TWD）→ data/history.json → Telegram
 ├─ hotel_tracker.py  じゃらん（主）＋ Booking（輔）→ data/hotels.json → Telegram
 └─ trips/*/          同上，針對每趟新行程（--trip）
        │ commit data/
        ▼
GitHub Pages（靜態）
 ├─ /            關西追蹤站 index.html（讀 data/*.json、hotels.json）
 └─ /planner/    旅程產生器（產生初稿／?trip=<slug> 看實查行程）
        ▲
Claude（只在規劃時使用，用訂閱額度）
 ├─ Cowork 對話＋japan-trip-planner 技能
 ├─ Claude Artifact 版產生器（sample 能力＝用你的 Claude 額度）
 └─ Claude Code /plan-trip ＋ 5 agents（本機，訂閱登入）
```

### 3.1 檔案

| 檔案 | 說明 |
|---|---|
| `tracker.py` | 用 Playwright 讀 Google Flights 的 `li div[aria-label]`，篩選時間條件並組合航班，再加上 LCC 行李費估算 |
| `config.json` | 機票追蹤條件，另見 `DEFAULT_CONFIG` |
| `hotel_tracker.py` | じゃらん（`JALAN_JS`）與 Booking（`BOOKING_JS`）；提醒條件見下方 |
| `hotels.json` | 關西 9 間飯店，含 jalan yad 編號、Agoda 路徑、照片、優缺點；`jpy_to_twd` 0.21 |
| `data/trip.json` | 關西逐日行程（items、route、transport、tickets、restaurants、lockers、trains）、scenes、costItems、foodLevels、trainsNote |
| `index.html` | 關西追蹤站；費用試算的函式是 `quote()` 與 `hotelOptions()` |
| `planner/src/template.html`、`planner/src/example.json`、`planner/build.py` | 產生器原始碼；執行 `python planner/build.py` 會輸出 `planner/index.html`（GitHub 版）與 `planner/artifact.html`（Artifact 版） |
| `trips/README.md`、`trips/index.json` | 多行程結構與清單 |
| `.github/workflows/track.yml` | 查價步驟：機票 → 飯店 → `trips/*/` → 存回（後三步 `if: always()`） |
| `windows/` | 本機排程腳本：`setup.bat`、`run.bat`、`open_page.bat` |
| `tests/` | 離線資料（`fixtures/`）、`make_fixtures.py`、`seed_hotels.py` |

`tracker.py` 的補充：
- 可在 Spyder 執行：已有 asyncio loop 時會改用 thread 跑。
- 參數用 `parse_known_args` 解析。
- 用 `--fixture` 離線測試，`--dry-run` 只印結果不寫檔。
- 用 `--trip DIR` 指定新行程的資料夾。

`hotel_tracker.py` 的提醒條件：
- 降價 ¥1,000 以上
- 由客滿變有房
- 由有房變客滿
- 只剩 1 間

`index.html` 的畫面：
- 機票價格走勢
- 飯店即時價卡片，Agoda 按鈕是主要按鈕（紫色），會帶入日期與人數
- 各城市住宿預算條
- 轉乘流程
- 每日 SVG 小地圖（`dailyMaps`、`dailyPOIs`）
- 實景照片（Wikimedia Commons）
- 每日電車時刻表（`trainBlock`）
- 全程費用試算

### 3.2 旅程產生器的兩種模式

| | GitHub 版 | Artifact 版 |
|---|---|---|
| 產生方式 | 按「產生提示詞」→ 貼到 Claude → 把 JSON 貼回 →「套用結果」 | 直接產生（`sample` 能力，用你的 Claude 額度，第一次會詢問同意） |
| 儲存 | 瀏覽器 localStorage | 雲端 db，換裝置也看得到 |
| 下載 | Blob 下載 | 透過 `downloads` 能力，會跳確認 |
| 看實查行程 | `?trip=<slug>` 讀 `trips/<slug>/`，並顯示即時價格 | — |

- 兩版的資料都是 AI 估算，頁面上有標示，每一項也附查證連結（Google Flights、Skyscanner、Booking、Google 地圖）。
- 「複製深度查證指令」會把初稿交給 Claude 或 Claude Code，做實查並建成追蹤網站。

---

## 4. 資料來源與踩過的坑

| 來源 | 狀態 | 注意 |
|---|---|---|
| Google Flights | ✅ 主要來源 | 用 zh-TW 介面、TWD 幣別，讀 aria-label |
| じゃらん | ✅ 飯店主要來源（只有日本） | 從 GitHub 查詢很穩定；空房月曆與各方案含稅總價都讀得到 |
| Booking.com | ⚠️ 輔助來源 | 從 GitHub 常逾時；網頁顯示「待下次查價」 |
| Agoda | ❌ 不追蹤，只放連結 | 自動化瀏覽一律顯示「已完售」，頁首「自 NT$…」是舊價。只能用飯店頁網址帶 `checkIn/checkOut/los/rooms/adults/children/currencyCode`；`search?textToSearch=` 會跳回首頁 |
| JR おでかけネット | ✅ 時刻與月台 | `station-timetable/<代碼>?date=YYYYMMDD`，列車詳細有番號與のりば。代碼表在 `.claude/skills-notes/jr-west-codes.md`。**禁止轉載**：只列重點班次，加上官方連結 |
| ekitan | ⚠️ 部分可用 | `/transit/express/section/`、`/transit/section/sf-X/st-Y?dt=&tm=` 可以用；路線搜尋被 robots 拒絕 |
| Jorudan、NAVITIME | ❌ | robots 拒絕，不繞道 |
| Wikimedia Commons | ✅ 照片 | 用 `Special:Redirect/file/<檔名>` |

過程中犯過的錯與修正：
- **Agoda 價格**：ChatGPT 稿寫的 Agoda「自 NT$…」是頁首舊價。我一度據此誤判 Il Verde、ZEQUU、與謝荘都已售完，之後發現連 11/10 也顯示售完，確認是自動化被擋，已更正並從網站移除錯誤資訊。
- **上傳後資料夾被攤平**：你手動上傳 repo 時資料夾結構不見了，已用 `git mv` 還原。
- **Node 20 棄用警告**：actions 升到 checkout@v5 與 setup-python@v6，runner 固定用 ubuntu-24.04。
- **京都 09:25 那班車**：是きのさき號，只到福知山，不是はしだて。已修正。
- **時刻表資料寫錯欄位**：把「建議」的 true 誤寫進到站月台欄，畫面出現「到 true 號」。已修正，之後寫入資料都會用 Python 檢查欄位型別。
- **手機版被撐寬**：grid 子項沒設 `min-width:0`，表格把手機版撐寬。已改成 `minmax(0,1fr)`。

---

## 5. 關於費用與開發方式的結論

- **不需要 API 費用**：網站運作完全不用 AI。Claude 和 Claude Code 登入訂閱帳號使用，不需要 API 金鑰，但會用到同一份訂閱額度。
- **什麼時候會真的付 API 費**：
  - 設了 `ANTHROPIC_API_KEY` 環境變數，Claude Code 會優先用它。
  - 在 CI 裡無人值守跑 `claude -p`。
  - 網頁本身即時呼叫 API。
  - 你的期貨技能需要 API 金鑰，請把金鑰限定在那個專案。
- **分工建議**：
  - 快速初稿：用產生器網頁。
  - 實查與正式版：用 Claude Code 的 `/plan-trip`，或在 Cowork 貼上「深度查證」指令。
  - 每天查價：GitHub Actions。

---

## 6. 後續可做（未開始）

- 把關西行程也轉成 `trips/kansai-2026-10/`，統一由 planner 顯示（目前關西用自己的 `index.html`）。
- `hotel_tracker.py` 加上非日本的來源（目前非日本只能靠 Booking，但 Booking 從 Actions 常逾時）。
- 產生器加上多城市地圖（目前只連到 Google 地圖）。
- 到了出發日（10/14），機票 tracker 會自動停止查關西；飯店 tracker 在最後一晚入住日停止。旅程結束後可以把關西的 `data/` 封存。

---

## 7. 給接手者的第一步

1. 讀 `CLAUDE.md`、`trips/README.md`、本文件。
2. 執行 `python tracker.py --fixture tests/fixtures --dry-run`，確認環境正常。
3. 關西這趟：只需要處理 2.5 節的待辦；網站會繼續自動更新。
4. 新行程：在 Claude Code 執行 `/plan-trip 目的地 出發日 回程日 人數 條件`。
