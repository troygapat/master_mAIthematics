@echo off
echo.
echo ================================================
echo   NUCLEAR RESTART - Math Tutor App
echo ================================================
echo.
echo Step 1: Stopping any running Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Clearing Streamlit cache...
rmdir /S /Q "%USERPROFILE%\.streamlit\cache" 2>nul
echo Cache cleared!

echo.
echo Step 3: Starting fresh app...
echo.
echo IMPORTANT: After app starts:
echo   1. Clear browser cache (Ctrl+Shift+Delete)
echo   2. Hard refresh browser (Ctrl+Shift+R) 3 times
echo   3. Try INCOGNITO mode if still issues
echo.
echo ================================================
echo.

cd /d "%~dp0"
streamlit run app.py

pause

