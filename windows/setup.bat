@echo off
chcp 65001 >nul
REM 一次性安裝：Playwright + Chromium，並建立每天 08:47 / 20:47 的 Windows 排程
cd /d "%~dp0.."

python --version >nul 2>&1 || (echo 找不到 Python，請先安裝 https://www.python.org/downloads/ 並勾選 Add to PATH & pause & exit /b 1)

python -m pip install --upgrade playwright || goto :err
python -m playwright install chromium || goto :err

schtasks /Create /F /TN "FlightTracker-AM" /SC DAILY /ST 08:47 /TR "\"%~dp0run.bat\"" || goto :err
schtasks /Create /F /TN "FlightTracker-PM" /SC DAILY /ST 20:47 /TR "\"%~dp0run.bat\"" || goto :err

echo.
echo 安裝完成，先跑一次測試…
call "%~dp0run.bat"
echo.
echo 之後每天 08:47、20:47 會自動查價。打開 windows\open_page.bat 看追蹤頁。
pause
exit /b 0

:err
echo 安裝失敗，請把上面的錯誤訊息截圖。
pause
exit /b 1
