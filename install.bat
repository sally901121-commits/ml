@echo off
REM Spectrum Plotter - Install Dependencies Script

echo.
echo ========================================
echo   Spectrum Plotter - Installing...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.
echo Installing required packages...
echo.

REM Install all required packages
pip install tkinterdnd pandas matplotlib

echo.
echo Installation complete!
echo You can now run the application by double-clicking run.bat
echo.
pause
