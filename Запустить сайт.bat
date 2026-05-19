@echo off
chcp 65001 > nul
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Виртуальное окружение .venv не найдено.
    echo Сначала создайте его командой:
    echo py -m venv .venv
    pause
    exit /b
)

echo Запуск сайта...
echo.

".venv\Scripts\python.exe" "start_site.py"

pause