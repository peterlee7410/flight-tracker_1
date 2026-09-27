# 桃園 ⇄ 關西 機票追蹤器（不需 AI / API）

用無頭瀏覽器讀取 Google 航班的公開搜尋結果。依 `config.json` 的條件篩選航班、組合去回程、估算行李費後寫進 `data/history.json`；`index.html` 讀這個檔案畫出追蹤頁。整個流程不呼叫 Claude 或任何付費 API。

## 檔案

| 檔案 | 用途 |
|---|---|
| `config.json` | 日期、人數、時間限制（去程 16:00 前抵達、回程 10:00 後起飛）、行李件數與單價、目標價、提醒門檻 |
| `tracker.py` | 查價主程式 |
| `index.html` | 追蹤頁（讀 `data/history.json`） |
| `data/trip.json` | 10/14–10/19 逐日行程、偏好航班時段、兩人當地預算與換算參數 |
| `.github/workflows/track.yml` | GitHub Actions 排程：每天台北 08:47、20:47 |
| `windows/` | 在自己 Windows 電腦上跑的安裝與排程腳本 |
| `tests/` | 離線測試資料（2026-09-26 從真實頁面擷取） |

## 方式一：GitHub（推薦，免費、電腦不用開機、手機也能看）

1. 登入 GitHub → 右上角 **+ → New repository**，名稱例如 `flight-tracker`，選 **Public**（免費的 GitHub Pages 需要 Public），按 Create。
2. 在新 repo 頁面點 **uploading an existing file**，把這個資料夾內**所有檔案與資料夾**拖進去（含 `.github`；若拖拉時看不到隱藏資料夾，可改用 GitHub Desktop 上傳）→ Commit。
3. **Settings → Actions → General → Workflow permissions** 選 **Read and write permissions** → Save。
4. **Settings → Pages → Source** 選 **Deploy from a branch**，Branch 選 `main`、資料夾 `/ (root)` → Save。約 1 分鐘後頁面網址會出現在同一頁：`https://<你的帳號>.github.io/flight-tracker/`
5. **Actions** 分頁 → 左邊點「機票查價」→ **Run workflow**，手動跑第一次，確認成功（綠色勾勾）。之後每天自動跑兩次。

> 注意：Public repo 代表任何人都看得到行程日期與價格，但不含姓名等個資。若想要私人，可改用方式二。

## 方式二：自己的 Windows 電腦

1. 安裝 Python 3.10+（安裝時勾選 **Add python.exe to PATH**）。
2. 把整個資料夾放在固定位置（例如 `D:\flight-tracker`），雙擊 `windows\setup.bat`：會安裝 Playwright、建立每天 08:47 / 20:47 的 Windows 工作排程，並先跑一次。
3. 雙擊 `windows\open_page.bat` 開啟追蹤頁（會在本機起一個小伺服器，看完關掉黑色視窗即可）。
4. 電腦需在排程時間開機（睡眠會錯過該次）。執行紀錄在 `data\run.log`。

## 在 Spyder 裡手動跑

整個資料夾要一起下載（`tracker.py` 旁邊要有 `config.json`；沒有也能用內建預設值跑）。第一次先在 IPython 主控台執行 `%pip install playwright` 與 `!python -m playwright install chromium`，之後直接按 Run 即可；結果會寫進同資料夾的 `data/history.json`。

## 飯店自動查價（hotel_tracker.py）

`hotels.json` 列出要追蹤的飯店與入住日期。GitHub Actions 每次查完機票後會接著執行 `hotel_tracker.py`：

- **じゃらん**：指定日期的空房月曆、各方案（不含餐／附早餐／二食）兩人含稅總價。
- **Booking.com**：搜尋結果卡片的價格與是否客滿（輔助來源，失敗時略過）。

結果存進 `data/hotels.json`，網頁的住宿區會顯示最新價、漲跌、走勢與預算比較。價格下跌 ¥1,000 以上、由客滿變成有房、變成客滿，或じゃらん只剩 1 間時，會用同一組 Telegram 設定推播。要新增或移除飯店，直接編輯 `hotels.json`。

## 手機推播（選用，兩種方式都適用）

1. Telegram 搜尋 **@BotFather** → `/newbot` → 取得 **Bot Token**。
2. 對你的新機器人傳一句話，再用瀏覽器打開 `https://api.telegram.org/bot<Token>/getUpdates`，找到 `"chat":{"id":數字}`，即 **Chat ID**。
3. GitHub：**Settings → Secrets and variables → Actions → New repository secret**，新增 `TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`。
   Windows：編輯 `windows\run.bat`，把兩行 `REM set ...` 的 `REM` 拿掉並填入。
4. 預設只在「建議下訂」時推播（最低價 ≤ NT$21,000、比上次降 ≥ NT$800、或距出發 ≤ 7 天）。想每次都收到：GitHub 在 **Variables** 新增 `NOTIFY_EVERY_RUN` = `1`。

## 限制與注意

- 網頁顯示「符合行程」的條件是去程 14:00 前抵達、回程 10:00–15:00 起飛；原查價仍保留 16:00 前抵達、10:00 後起飛的全部合格選項。行程與當地費用是規劃估算，不是即時訂位報價。
- 可在頁面選航班、改當地兩人預算與日圓換算率，試算「機票＋當地費用」。輸入值僅保存在該瀏覽器。當地費用不包含已訂 RTI 天王寺；若煙火票或京都住宿尚未買到，請按實際方案調整。
- 航班列的 Google 連結會重新開啟同日期、同人數搜尋；請在搜尋結果中核對**同一班時間與航空公司**，再確認兩人付款總額。它不是價格鎖定或該班次的預訂連結。
- 價格來自 Google 航班，其他網站（Trip.com、官網）可能更便宜或更貴，下訂前請到官網核對。
- 行李費為估算值，可在 `config.json` 的 `lcc_bag_fee` 調整。
- Google 若改版頁面，程式可能讀不到資料；GitHub 會寄信通知執行失敗，屆時需調整 `tracker.py`。
- GitHub 的機器在美國，偶爾可能被 Google 要求驗證；若連續失敗，改用方式二（台灣家用網路較穩定）。
- 程式只讀取公開搜尋結果，不會登入、訂票或輸入任何付款資料。請合理控制頻率（預設每天 2 次）。

## 離線測試

```
python tests/make_fixtures.py
python tracker.py --fixture tests/fixtures --dry-run
```

## 旅程產生器（planner/）

網址：https://peterlee7410.github.io/flight-tracker_1/planner/

輸入目的地、日期、人數、預算與條件，產生整套行程（機票建議、住宿候選、每日行程與交通班次、費用試算）。

- 在 GitHub Pages 上：按「產生提示詞」→ 貼到你的 Claude（網頁或 App，用訂閱額度，不需 API 金鑰）→ 把回覆的 JSON 貼回頁面 →「套用結果」。
- 在 Claude 的 Artifact 版本裡：直接按「產生整套行程」即可。
- 已存行程存在該裝置瀏覽器（localStorage）；可「下載 trip.json」帶到別台裝置或交給 Claude 做深度查證。
- 價格與班次為 AI 估算，訂之前用頁面上的連結確認。

## 交接文件

- `docs/SESSION-HANDOFF.md`：整個規劃 session 的完整交接（需求、行程現況、系統、資料來源、待辦）
- `HANDOFF-claude-code.md`：在 Claude Code 用 `/plan-trip` agent 產生新行程
