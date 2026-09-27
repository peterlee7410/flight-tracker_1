# flight-tracker_1 — 旅程規劃與零 API 追蹤系統

這個 repo 同時是：
1. 2026/10 關西之旅的追蹤網站（根目錄 `index.html`、`data/`、`config.json`、`hotels.json`）。
2. 可套用到任何目的地的「旅程產生器」：`planner/`（產生／瀏覽行程）＋ `trips/<slug>/`（每趟實查後的行程與追蹤資料）。
3. Claude Code agent 流程：`/plan-trip` 指令與 `.claude/agents/` 的分工 agent。

## 架構原則（不可違反）
- **執行時零 AI 費用**：GitHub Actions 只跑 `tracker.py`、`hotel_tracker.py`（Python＋Playwright），網站是 GitHub Pages 靜態頁。不要在 Actions、網站或腳本中呼叫 Claude API、不要加入 `ANTHROPIC_API_KEY`。
- **不代訂**：不下單、不付款、不登入、不輸入卡號或密碼、不過 CAPTCHA。只提供帶日期與人數的預訂連結。
- **尊重網站限制**：WebFetch 因 robots 拒絕的網站（Jorudan、ekitan 路線搜尋、NAVITIME 等）不改用 curl/Playwright 硬抓；改用官方來源或 ekitan `/transit/section/`、JR おでかけネット 等可用頁面。
- **時刻表著作權**：JR 等官方時刻表禁止轉載。每段只列 2–4 班重點車＋官方當日時刻表連結（`src`）。
- **會變的資訊一律現查**並記錄查證日期；估算值要在 note 標明「估」。

## 目錄
| 路徑 | 用途 |
|---|---|
| `tracker.py [--trip trips/<slug>]` | Google Flights 查價；讀 `<trip>/config.json`，寫 `<trip>/data/history.json` |
| `hotel_tracker.py [--trip trips/<slug>]` | じゃらん（主）＋Booking（輔）查房價；讀 `<trip>/hotels.json`，寫 `<trip>/data/hotels.json` |
| `planner/index.html` | 旅程產生器；`planner/?trip=<slug>` 顯示 `trips/<slug>/trip.json` 與即時價格 |
| `trips/index.json` | 已建立行程清單 `[{slug,title,start,end,destination}]` |
| `trips/<slug>/` | `trip.json`、`config.json`、`hotels.json`、`research/*.md`、`data/`（Actions 寫入） |
| `trips/README.md` | **trip.json 結構定義（必讀）** |
| `.github/workflows/track.yml` | 每天 08:47／20:47（台北）查根目錄行程與所有 `trips/*/` |

## 開發慣例
- Windows 上用 `py` 或 `python`；測試：`python tracker.py --fixture tests/fixtures --dry-run`。
- 網頁改完要本機預覽：`python -m http.server 8000` 後開 `http://localhost:8000/planner/?trip=<slug>`，檢查 390px 手機寬度沒有橫向捲動。
- Git：先 `git pull --rebase` 再 push（Actions 也會 commit）；禁止 force push。
- 回報格式：一兩句說明改了什麼＋「日期｜建議｜備註」短表＋使用者要自己處理的事（劃位、預約）＋Sources。
