@echo off
REM --------------------------------------------------------------------------
REM  launch.bat - Launches the Advanced File Search Python application.
REM
REM  This script is designed to be portable. It automatically finds its own
REM  location, activates the local virtual environment, and then runs the
REM  main Python script.
REM --------------------------------------------------------------------------

REM --- Step 1: Set the script's directory as the current working directory ---
REM %~dp0 is a special variable that expands to the drive and path of this .bat file.
REM The 'cd /d' command ensures we change drive and directory, making it robust.
cd /d "%~dp0"
echo Changing directory to: %cd%


REM --- Step 2: Check for and activate the virtual environment ---
IF NOT EXIST ".\.venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at '.\.venv'.
    echo Please run the setup instructions in README.md first.
    pause
    exit /b
)

echo Activating virtual environment...
REM 'call' runs the activate script and then returns control to this script.
call .\.venv\Scripts\activate.bat


REM --- Step 3: Launch the Python application ---
IF NOT EXIST "main.py" (
    echo [ERROR] Main script 'main.py' not found.
    pause
    exit /b
)

echo Starting the application...
REM Use 'start "Title"' to run the Python script in a new window.
REM This prevents the main command prompt from being locked up.
start "Advanced File Search" python main.py


REM --- Step 4: Clean up and exit ---
exit /b
