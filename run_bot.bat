@echo off
setlocal

REM Check if venv exists
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating 'venv'...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment. Please check your Python installation.
        pause
        exit /b 1
    )
    
    echo [INFO] Activating venv and installing requirements...
    call venv\Scripts\activate
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Virtual environment found. Activating...
    call venv\Scripts\activate
)

REM Run the bot
echo [INFO] Starting PolyCord Bot...
python src/main.py

if errorlevel 1 (
    echo [ERROR] Bot crashed or stopped with an error.
    pause
)

deactivate
endlocal
