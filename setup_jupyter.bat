@echo off
echo ========================================
echo    JUPYTER NOTEBOOK SETUP & LAUNCH
echo ========================================
echo.

echo Step 1: Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing Python 3.11.9...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    if exist "python_installer.exe" (
        echo Installing Python... This takes 2-3 minutes.
        python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
        timeout /t 10
        del python_installer.exe
        echo Python installed! Please RESTART your computer and run this script again.
        pause
        exit
    ) else (
        echo Download failed! Install Python manually from python.org
        pause
        exit
    )
)

echo Step 2: Creating virtual environment...
if exist "retail_env" rmdir /s /q retail_env
python -m venv retail_env

echo Step 3: Installing packages...
call retail_env\Scripts\activate.bat
pip install --upgrade pip
pip install pandas numpy pyodbc Faker jupyter matplotlib seaborn plotly openpyxl scipy


echo Step 4: Creating Jupyter notebook...
python -c "
import json

notebook_content = {
    'cells': [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '# Retail Data Analysis Notebook\\n',
                '## Comprehensive Data Exploration, Quality Checks, and Cleaning\\n',
                'This notebook will help you explore, clean, and prepare your retail data for analysis and BI.'
            ]
        }
    ],
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {'name': 'ipython', 'version': 3},
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.11.9'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4
}

with open('Retail_Data_Analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=2)

print('Jupyter notebook created!')
"

echo Step 6: Launching Jupyter Notebook...
echo Jupyter will open in your web browser...
echo Keep this window open while working with Jupyter.
echo.
echo Press Ctrl+C to stop Jupyter when done.
echo.
call retail_env\Scripts\activate.bat
jupyter notebook