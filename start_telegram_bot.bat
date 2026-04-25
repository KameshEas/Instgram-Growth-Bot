@echo off
REM Start Telegram Bot - Windows Batch Script

echo.
echo ============================================================
echo Instagram Growth Bot - Telegram Interface
echo ============================================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found
    echo [INFO] Create it first:
    echo.
    echo   python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate venv
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found
    echo [INFO] Create it from .env.example or add:
    echo.
    echo   TELEGRAM_BOT_TOKEN=your_token_here
    echo   GROQ_API_KEY=your_key_here
    echo.
    pause
    exit /b 1
)

REM Install dependencies
echo [INFO] Checking dependencies...
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo [WARN] Installing python-telegram-bot...
    pip install python-telegram-bot==20.3
)

REM Check if groq is installed
pip show groq >nul 2>&1
if errorlevel 1 (
    echo [WARN] Installing groq...
    pip install groq==1.2.0
)

REM Run the launcher script (which will run the bot)
echo.
echo [OK] All dependencies ready
echo [INFO] Starting Telegram bot...
echo.
echo [INFO] Press Ctrl+C to stop
echo.

python run_telegram_bot.py

if errorlevel 1 (
    echo.
    echo [ERROR] Bot exited with error code %errorlevel%
    pause
)

