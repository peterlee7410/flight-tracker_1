# Handoff：在 Claude Code 用 agent 產生並追蹤旅程

- **對象**：在自己的 Windows 電腦用 Claude Code 接手這個 repo 的人（也就是你，或之後的 Claude Code session）。
- **Repo**：https://github.com/peterlee7410/flight-tracker_1
- **網站**：https://peterlee7410.github.io/flight-tracker_1/
- **旅程產生器**：https://peterlee7410.github.io/flight-tracker_1/planner/
- **建立日期**：2026-09-27（由 Claude 的雲端工作階段整理）

---

## 1. 這個 repo 現在有什麼

| 部分 | 內容 | 狀態 |
|---|---|---|
| 關西 2026/10/14–19 追蹤站 | 根目錄 `index.html`、`data/`、`config.json`、`hotels.json` | 運作中。GitHub Actions 每天 08:47、20:47（台北）查機票與飯店，變動時用 Telegram 通知 |
| 旅程產生器 | `planner/index.html` | 任何目的地都可以產生初稿（AI 估算）。`planner/?trip=<slug>` 會顯示實查過的行程與即時價格 |
| 多行程追蹤 | `trips/<slug>/` 加上 `tracker.py --trip`、`hotel_tracker.py --trip` | 已接進 workflow，Actions 會自動查所有 `trips/*/` |
| Claude Code agent | `CLAUDE.md`、`.claude/agents/*`、`.claude/commands/plan-trip.md` | 這份文件要交接的部分 |

**核心原則：網站運作時完全不用 AI。**
- 查價靠 GitHub Actions 跑 Python 加 Playwright，網頁是 GitHub Pages 的靜態頁，不花任何 AI 費用。
- Claude Code 只在你下 `/plan-trip` 時使用，用的是你的訂閱額度。

---

## 2. 一次性安裝（Windows）

1. **安裝基本工具**
   - Git for Windows
   - Python 3.12（安裝時勾選「Add python.exe to PATH」）
   - Claude Code：依官方文件 https://docs.claude.com/en/docs/claude-code 安裝

2. **確認 Claude Code 用的是訂閱，不是 API 金鑰（重要）**
   - PowerShell 執行 `echo $env:ANTHROPIC_API_KEY`。有值的話，Claude Code 會改用 API 按量計費。
   - 期貨分析需要金鑰的話，把金鑰設在那個專案自己的環境裡，不要設成系統全域變數。
   - 在 Claude Code 裡輸入 `/status`，確認顯示的是 Claude 帳號（Pro/Max）登入。
   - 訂閱的用量與 claude.ai 共用。說明見 https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan

3. **下載 repo 並安裝套件**
   ```powershell
   cd D:\
   git clone https://github.com/peterlee7410/flight-tracker_1.git
   cd flight-tracker_1
   py -m pip install playwright==1.47.0
   py -m playwright install chromium
   py tracker.py --fixture tests/fixtures --dry-run
   ```
   最後一行是離線測試，應該會印出 15 筆航班。

4. **設定 GitHub 推送權限**
   - 用 GitHub Desktop 登入一次，或執行 `gh auth login`。
   - 這樣 agent 最後 `git push` 才不會卡住。

5. **在 repo 資料夾啟動 Claude Code**
   ```powershell
   claude
   ```
   - 第一次會讀 `CLAUDE.md`。
   - 輸入 `/agents` 應該看到 5 個 agent：flight-scout、hotel-scout、transit-planner、local-scout、trip-builder。
   - 輸入 `/` 應該看到 `plan-trip`。

---

## 3. 日常用法

```text
/plan-trip 札幌・小樽 2026-12-20 2026-12-24 2人 預算6萬 去程16點前到 回程10點後飛 想泡溫泉
```

流程（`.claude/commands/plan-trip.md`）：

1. 解析條件，建立 `trips/sapporo-2026-12/`。
2. 平行研究：
   - flight-scout：查機票，產生 config.json，並實跑一次 tracker。
   - hotel-scout：找住宿，產生 hotels.json，實查じゃらん或 Booking，並組好 Agoda 連結。
   - local-scout：查活動、營業時間、門票、美食、寄物櫃。
3. local-scout 完成後，transit-planner 依逐日地點查官方時刻表，挑出建議班次與月台。
4. trip-builder 整合：
   - 產生並驗證 trip.json
   - 更新 trips/index.json
   - 本機預覽
   - commit 並 push
5. 另開一個 agent 獨立查核，抽查 5 項關鍵事實，有錯就修正。
6. 回報網站網址、費用、建議班次表、你要自己處理的事，以及來源。

完成後：
- 網址是 `https://peterlee7410.github.io/flight-tracker_1/planner/?trip=sapporo-2026-12`。
- 之後 Actions 每天自動查價，有變動就用 Telegram 通知。

**先用網頁產初稿再交給 agent（省額度）**
- 在 planner 網頁產生初稿，按「下載 trip.json」。
- 把檔案放到 repo，然後跟 Claude Code 說：「用這份當初稿跑 /plan-trip」。

**只做其中一段也可以**，例如：
- 「用 transit-planner 幫 trips/sapporo-2026-12 重查 12/22 的交通」
- 「用 hotel-scout 找京都 12/23 一晚 NT$3,000 內的飯店」

---

## 4. 額度與成本

- Claude Code 互動使用：用訂閱額度，不另外付費。
- 一次完整的 `/plan-trip` 要跑 5 到 6 個 agent，外加大量搜尋，很耗額度：
  - Pro 方案可能一次就碰到 5 小時上限，Max 比較寬裕。
  - 一次只跑一趟行程。
  - 用量大的話，可以在 agent 檔頭加 `model: sonnet`，讓查資料的 agent 用較省的模型。
- 不要做成無人值守的自動化，例如在 Actions 裡跑 `claude -p`。官方建議這類自動化用 API 金鑰按量計費。
- GitHub Actions 與 Pages 在公開 repo 上免費。

---

## 5. 檔案地圖

| 路徑 | 說明 |
|---|---|
| `CLAUDE.md` | Claude Code 自動讀取的專案規則（架構、禁止事項、慣例） |
| `.claude/commands/plan-trip.md` | `/plan-trip` 指令流程 |
| `.claude/agents/flight-scout.md` | 查機票，產生 `trips/<slug>/config.json` 與 `research/flights.md` |
| `.claude/agents/hotel-scout.md` | 查住宿，產生 `hotels.json` 與 `research/hotels.md` |
| `.claude/agents/transit-planner.md` | 查官方時刻表，產生 legs 與 `research/transit.md` |
| `.claude/agents/local-scout.md` | 查活動、門票、美食、寄物櫃，產生 `research/local.md` |
| `.claude/agents/trip-builder.md` | 整合、驗證、預覽、push |
| `.claude/skills-notes/jr-west-codes.md` | JR 西日本時刻表代碼與已知陷阱 |
| `.claude/settings.json` | 預先允許搜尋、Python、git（禁止 force push） |
| `trips/README.md` | **trip.json 結構定義** |
| `trips/index.json` | 已建立行程清單（planner 左側「VERIFIED TRIPS」） |
| `tracker.py --trip DIR` | 機票查價（Google Flights 公開結果） |
| `hotel_tracker.py --trip DIR` | 飯店查價（じゃらん為主，Booking 為輔） |
| `planner/index.html` | 產生器與行程瀏覽頁。修改來源在 Claude 雲端工作階段；直接改這個檔也可以 |
| `.github/workflows/track.yml` | 排程查價：根目錄行程加上所有 `trips/*/` |

---

## 6. 規則與已知陷阱（agent 已寫入，人工也請遵守）

- **不代訂**：不下單、不付款、不登入、不輸入卡號或密碼、不過 CAPTCHA。
- **Agoda**
  - 自動化瀏覽時一律顯示「已完售」，頁首「自 NT$…」是舊價，不能當作可訂價。
  - `search?textToSearch=` 會跳回首頁。只能用飯店頁網址帶入日期。
- **Booking**：從 GitHub Actions 查詢常逾時，只當輔助來源。
- **じゃらん**：最穩定（只限日本）。空房看 `.calendar-day-YYYY-MM-DD`。
- **robots 限制**：Jorudan、ekitan 路線搜尋、NAVITIME 不能繞道抓。可用的來源：
  - ekitan 的 `/transit/section/` 頁面
  - JR おでかけネット
- **時刻表著作權**：JR おでかけネット禁止轉載，每段只列 2–4 班並附官方連結。
- **確認日期**：一律查旅遊當天的時刻，注意平日與假日不同，以及時刻改正日（例如 2026-10-03）。
- **交通陷阱**
  - 関空快速在日根野分割，要坐前 4 節。
  - はしだて不停嵯峨嵐山。
  - 大型活動日，私鐵會加開或臨時改停站。
- **Git**：Actions 也會 commit，每次 push 前先 `git pull --rebase`，不要 force push。

---

## 7. 疑難排解

| 狀況 | 處理 |
|---|---|
| `tracker.py` 0 筆 | Google Flights 頁面格式可能變了。先跑 `--fixture tests/fixtures --dry-run` 確認程式正常，再用 `--dry-run` 看即時結果 |
| 飯店全部查詢失敗 | じゃらん可能暫時擋下，下一次排程通常會恢復；Actions 失敗時不會寫入資料 |
| planner 顯示「找不到行程」 | 確認 `trips/<slug>/trip.json` 已 push，且 slug 只有小寫英數與連字號；Pages 約 1–2 分鐘才更新 |
| push 被拒 | 先 `git pull --rebase` 再 push |
| Claude Code 開始扣 API 費 | 移除 `ANTHROPIC_API_KEY` 環境變數，重新 `/login` 訂閱帳號 |
| agent 查到一半額度用完 | 研究筆記已存在 `trips/<slug>/research/`，額度恢復後說「從 research 接續完成 /plan-trip」 |

---

## 8. 關西行程現況（2026-09-27）

- **機票**
  - 最低：捷星 02:30 紅眼加泰越捷 12:25，NT$23,836。
  - 最低非紅眼：虎航 06:40 加泰越捷 12:25，NT$26,518。
- **住宿**
  - 10/15 よさの荘：¥14,268，接駁要打 0772-22-3555 預約。
  - 10/16 Green Rich 京都駅南：¥19,280。
  - RTI 天王寺已訂。
- **每日電車**
  - 建議班次與月台已放在網站每日卡片。
  - 10/19 搭 08:10 HARUKA 1007M，天王寺 15 號月台。
- **費用試算**：免費看花火時全程約 NT$48,971，每人約 NT$24,486。
- **仍需自己做**
  - 訂機票
  - 領關西廣域券時一次劃好指定席
  - 預約よさの荘接駁
  - 決定月灯路買現場票或網路票
  - 花火日 17:00 前到姫島河堤
