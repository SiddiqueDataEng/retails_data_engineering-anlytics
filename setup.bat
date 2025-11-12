@echo off
title ONE-CLICK PYTHON ANALYTICS SETUP & RUN
color 0A

echo ========================================
echo    ONE-CLICK PYTHON SETUP & RUN
echo ========================================
echo.

REM === STEP 1: CHECK PYTHON ===
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing Python 3.11.9...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    if exist "python_installer.exe" (
        echo Installing Python... Please wait 2-3 minutes.
        python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        timeout /t 10
        del python_installer.exe
        echo Python installed! Please RESTART your computer and run this script again.
        pause
        exit
    ) else (
        echo Download failed! Please install Python manually from https://www.python.org/downloads/
        pause
        exit
    )
)

echo Python detected!
python --version
echo.

REM === STEP 2: CREATE VIRTUAL ENVIRONMENT ===
echo Step 2: Setting up virtual environment...
if exist "retail_env" (
    echo Virtual environment already exists. Updating...
) else (
    python -m venv retail_env
)
call retail_env\Scripts\activate.bat

echo Virtual environment activated.
echo.

REM === STEP 3: INSTALL OR UPDATE REQUIRED PACKAGES ===
echo Step 3: Installing/updating required libraries...
pip install --upgrade pip >nul

REM You can modify or extend this list as needed
set packages=pandas==2.0.3 numpy==1.24.3 pyodbc==4.0.39 Faker==19.6.2 squarify==0.4.3 matplotlib seaborn plotly scipy openpyxl XlsxWriter tqdm python-dotenv

for %%p in (%packages%) do (
    echo Installing/updating %%p ...
    pip install --upgrade --no-warn-script-location --upgrade-strategy only-if-needed %%p >nul
)

echo.
echo ✅ All required packages installed or updated!
echo.

REM === STEP 4: RUN THE PYTHON SCRIPT ===
if exist datagenerator.py (
    echo Step 4: Running datagenerator.py...
    python datagenerator.py
) else (
    echo datagenerator.py not found! Please ensure your script is in the same folder.
)

echo.
echo ========================================
echo    ✅ SETUP & EXECUTION COMPLETE
echo ========================================
echo.
echo You can now start analyzing your data!
echo To deactivate the environment, type: deactivate
echo.
pause