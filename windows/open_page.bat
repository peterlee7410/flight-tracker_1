@echo off
chcp 65001 >nul
REM 瀏覽器不允許 file:// 直接讀 JSON，所以用 Python 起一個本機小伺服器
cd /d "%~dp0.."
start "" http://localhost:8765/
python -m http.server 8765
