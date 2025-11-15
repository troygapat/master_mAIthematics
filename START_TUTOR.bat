@echo off
REM AI Math Tutor - Easy Launcher
REM Double-click this file to start the application

title AI Math Tutor

echo.
echo ========================================
echo   AI Math Tutor - Starting...
echo ========================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy env_template.txt .env
    echo.
    echo IMPORTANT: Please edit .env and add your ANTHROPIC_API_KEY
    echo Then run this file again.
    echo.
    notepad .env
    pause
    exit /b 0
)

REM Check if dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo First time setup - Installing dependencies...
    echo This may take a few minutes...
    echo.
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo.
    echo Setup complete!
    echo.
)

REM Initialize database if needed
if not exist "data\tutoring.db" (
    echo Initializing database...
    python src\database\init_db.py
    echo.
)

REM Launch the application
echo Starting AI Math Tutor...
echo.
echo The app will open in your web browser.
echo Press Ctrl+C in this window to stop the application.
echo.
echo ========================================
echo.

python -m streamlit run app.py

REM If streamlit exits, pause so user can see any errors
if errorlevel 1 (
    echo.
    echo ========================================
    echo   Application stopped with an error
    echo ========================================
    echo.
    pause
)

