@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found: .venv\Scripts\python.exe
    echo         Create the project venv first, then re-run this launcher.
    pause
    exit /b 1
)

echo Starting Isaac Offline Map Preview...
".venv\Scripts\python.exe" "scripts\launch_preview.py"
if errorlevel 1 (
    echo.
    echo [ERROR] The preview UI exited with an error.
    pause
)
endlocal
