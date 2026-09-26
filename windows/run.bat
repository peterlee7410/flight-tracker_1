@echo off
chcp 65001 >nul
cd /d "%~dp0.."
REM 若要 Telegram 推播，取消下面兩行的 REM 並填入
REM set TELEGRAM_BOT_TOKEN=你的BotToken
REM set TELEGRAM_CHAT_ID=你的ChatID
set PYTHONIOENCODING=utf-8
if not exist data mkdir data
python tracker.py >> data\run.log 2>&1
