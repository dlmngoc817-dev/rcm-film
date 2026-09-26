@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto install
where py >nul 2>nul
if errorlevel 1 goto try_python
py -3 -m venv .venv
if errorlevel 1 goto failed
goto install
:try_python
where python >nul 2>nul
if errorlevel 1 goto missing
python -m venv .venv
if errorlevel 1 goto failed
:install
if exist ".venv\.rcm-installed" goto launch
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
type nul > ".venv\.rcm-installed"
:launch
echo Opening RCM Film. Keep this window open. Press Ctrl+C to stop.
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 goto failed
exit /b 0
:missing
echo Python was not found. Install Python 3.11 or 3.12 from python.org.
echo Enable Add Python to PATH, then run this file again.
pause
exit /b 1
:failed
echo Setup or launch failed. Read the error above and consult README.md.
pause
exit /b 1
