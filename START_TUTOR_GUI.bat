@echo off
REM AI Math Tutor - GUI Launcher
REM Double-click this file to open the graphical launcher

cd /d "%~dp0"
python gui_launcher.py

if errorlevel 1 (
    echo Failed to start GUI launcher
    echo.
    echo Falling back to direct launch...
    echo.
    pause
    python -m streamlit run app.py
)

