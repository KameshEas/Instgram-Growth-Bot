#!/usr/bin/env pwsh
<#
.SYNOPSIS
Start Telegram Bot - PowerShell Launcher Script

.DESCRIPTION
Sets up virtual environment, installs dependencies, and runs the Telegram bot
#>

# Colors for output
$SuccessColor = "Green"
$WarningColor = "Yellow"
$ErrorColor = "Red"
$InfoColor = "Cyan"

Write-Host "`n" -ForegroundColor $InfoColor
Write-Host "============================================================" -ForegroundColor $InfoColor
Write-Host "Instagram Growth Bot - Telegram Interface" -ForegroundColor $InfoColor
Write-Host "============================================================" -ForegroundColor $InfoColor
Write-Host

# Check if we're in the correct directory
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor $ErrorColor
    Write-Host "[INFO] Create it with: python -m venv venv" -ForegroundColor $InfoColor
    Write-Host
    exit 1
}

Write-Host "[INFO] Activating virtual environment..." -ForegroundColor $InfoColor

# Activate venv
& ".\venv\Scripts\Activate.ps1"

# Check if we successfully activated
$pythonPath = (python -c "import sys; print(sys.executable)") 2>$null
if ($pythonPath -match "venv") {
    Write-Host "[OK] Virtual environment activated" -ForegroundColor $SuccessColor
    Write-Host "[INFO] Python: $pythonPath" -ForegroundColor $InfoColor
} else {
    Write-Host "[ERROR] Failed to activate virtual environment" -ForegroundColor $ErrorColor
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor $ErrorColor
    Write-Host "[INFO] Create it from .env.example or add:" -ForegroundColor $InfoColor
    Write-Host
    Write-Host "  TELEGRAM_BOT_TOKEN=your_token_here" -ForegroundColor $WarningColor
    Write-Host "  GROQ_API_KEY=your_key_here" -ForegroundColor $WarningColor
    Write-Host
    exit 1
}

Write-Host "[OK] .env file found" -ForegroundColor $SuccessColor
Write-Host

# Check dependencies
Write-Host "[INFO] Checking dependencies..." -ForegroundColor $InfoColor

$deps = @("python-telegram-bot", "groq", "requests", "python-dotenv")

foreach ($dep in $deps) {
    $pipDep = $dep -replace "python-dotenv", "dotenv"
    $installed = pip show $pipDep 2>$null
    
    if ($installed) {
        Write-Host "[OK] $dep is installed" -ForegroundColor $SuccessColor
    } else {
        Write-Host "[WARN] Installing $dep..." -ForegroundColor $WarningColor
        pip install $dep
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] $dep installed" -ForegroundColor $SuccessColor
        } else {
            Write-Host "[ERROR] Failed to install $dep" -ForegroundColor $ErrorColor
            exit 1
        }
    }
}

Write-Host
Write-Host "============================================================" -ForegroundColor $InfoColor
Write-Host "[OK] All dependencies ready!" -ForegroundColor $SuccessColor
Write-Host "============================================================" -ForegroundColor $InfoColor
Write-Host

Write-Host "[INFO] Starting Telegram bot..." -ForegroundColor $InfoColor
Write-Host "[INFO] Press Ctrl+C to stop" -ForegroundColor $InfoColor
Write-Host

# Run the launcher script
try {
    python run_telegram_bot.py
} catch {
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor $ErrorColor
    exit 1
}
