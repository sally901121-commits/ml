@echo off
REM Spectrum Plotter - Auto Run Script
REM Check Python installation and run the application

echo.
echo ========================================
echo   Spectrum Plotter - Starting...
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

REM Check if required packages are installed
echo Checking required packages...
pip show pandas >nul 2>&1
if errorlevel 1 (
    echo Installing pandas...
    pip install pandas
)

pip show matplotlib >nul 2>&1
if errorlevel 1 (
    echo Installing matplotlib...
    pip install matplotlib
)

pip show numpy >nul 2>&1
if errorlevel 1 (
    echo Installing numpy...
    pip install numpy
)

echo.
echo All dependencies are ready!
echo.
echo Starting Spectrum Plotter Application...
echo.

REM Run the application
python spectrum_plotter_gui.py

if errorlevel 1 (
    echo.
    echo Error occurred while running the application
    pause
)

pause
