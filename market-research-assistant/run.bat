@echo off
title IMRA - Intelligent Market Research Assistant
color 0B

echo.
echo  ============================================================
echo   IMRA - Intelligent Market Research Assistant
echo   Powered by IBM Granite LLM ^| Agentic AI
echo  ============================================================
echo.

:: ── Step 1: Find Python ───────────────────────────────────────────────────────
set PYTHON_CMD=

:: Try common Python executable names
for %%P in (python python3) do (
    %%P --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=%%P
        goto :python_found
    )
)

:: Try common install paths
for %%D in (
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%USERPROFILE%\Anaconda3\python.exe"
    "%USERPROFILE%\Miniconda3\python.exe"
    "C:\ProgramData\Anaconda3\python.exe"
    "C:\ProgramData\Miniconda3\python.exe"
) do (
    if exist %%D (
        set PYTHON_CMD=%%D
        goto :python_found
    )
)

:: Python not found
echo  [ERROR] Python 3.10+ is required but was not found.
echo.
echo  INSTALLATION STEPS:
echo  -------------------
echo  1. Open your browser and go to: https://www.python.org/downloads/
echo  2. Download Python 3.11 or 3.12 (Windows installer)
echo  3. Run the installer - IMPORTANT: check "Add Python to PATH"
echo  4. Restart this .bat file after installation
echo.
echo  Alternatively, install Anaconda from: https://www.anaconda.com/download
echo.
start https://www.python.org/downloads/
pause
exit /b 1

:python_found
echo  [OK] Python found: %PYTHON_CMD%
%PYTHON_CMD% --version

:: ── Step 2: Check Python version (must be 3.10+) ─────────────────────────────
for /f "tokens=2 delims= " %%V in ('%PYTHON_CMD% --version 2^>^&1') do set PYVER=%%V
for /f "tokens=1,2 delims=." %%A in ("%PYVER%") do (
    set PY_MAJOR=%%A
    set PY_MINOR=%%B
)
if %PY_MAJOR% LSS 3 (
    echo  [ERROR] Python 3.10+ required. Found: %PYVER%
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 10 (
    echo  [WARNING] Python 3.10+ recommended. Found: %PYVER%
    echo  The application may still work, but upgrading is advised.
    echo.
)

:: ── Step 3: Create virtual environment ───────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo  [SETUP] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo  [ERROR] Failed to create virtual environment.
        echo  Try: %PYTHON_CMD% -m pip install --upgrade pip
        pause
        exit /b 1
    )
    echo  [OK] Virtual environment created.
) else (
    echo  [OK] Virtual environment exists.
)

:: ── Step 4: Activate virtual environment ─────────────────────────────────────
call venv\Scripts\activate.bat
echo  [OK] Virtual environment activated.

:: ── Step 5: Upgrade pip silently ─────────────────────────────────────────────
python -m pip install --upgrade pip --quiet --disable-pip-version-check

:: ── Step 6: Install dependencies ─────────────────────────────────────────────
echo  [SETUP] Installing/verifying dependencies (this may take a minute the first time)...
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo.
    echo  [ERROR] Failed to install dependencies.
    echo  Trying with verbose output for diagnostics...
    pip install -r requirements.txt
    pause
    exit /b 1
)
echo  [OK] All dependencies installed.

:: ── Step 7: Check for .env file ──────────────────────────────────────────────
if not exist ".env" (
    echo.
    echo  [INFO] No .env file found — creating from template...
    copy .env.example .env >nul
    echo  [INFO] Created .env file. Running in DEMO MODE.
    echo  [INFO] To enable IBM Granite Live mode:
    echo         1. Edit .env with your IBM watsonx credentials
    echo         2. Restart this launcher
    echo.
) else (
    echo  [OK] .env configuration file found.
)

:: ── Step 8: Launch application ────────────────────────────────────────────────
echo.
echo  ============================================================
echo   Starting IMRA...
echo.
echo   Application URL : http://localhost:5000
echo   API Health Check: http://localhost:5000/api/health
echo   Log file        : logs\app.log
echo.
echo   Press Ctrl+C to stop the server
echo  ============================================================
echo.

:: Open browser after 3 seconds (background)
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Start Flask server
python app.py

:: Server stopped
echo.
echo  ============================================================
echo   IMRA server stopped.
echo   Check logs\app.log for details.
echo  ============================================================
echo.
pause
