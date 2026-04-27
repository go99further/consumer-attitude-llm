@echo off
chcp 65001 >nul
echo ========================================
echo Variable Extraction Script Runner
echo ========================================
echo.

REM 切换到脚本目录
cd /d "%~dp0"

REM 检查 Python 是否安装（先尝试 python，再尝试 py）
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)

echo [ERROR] Python not found. Please install Python 3.7 or higher
echo.
echo Solutions:
echo 1. Download and install Python from https://www.python.org/downloads/
echo 2. Check "Add Python to PATH" during installation
echo 3. Or use py command: py variable_extraction.py
pause
exit /b 1

:python_found
echo [INFO] Python version:
%PYTHON_CMD% --version
echo.

REM 检查脚本文件是否存在
if not exist "variable_extraction.py" (
    echo [ERROR] variable_extraction.py not found
    echo [INFO] Current directory: %CD%
    pause
    exit /b 1
)

REM 检查配置文件
if not exist "config.py" (
    echo [WARNING] config.py not found
    echo [INFO] Please ensure API key is configured correctly
    echo.
)

REM 检查数据文件
if not exist "..\data\cleaned_reviews.csv" (
    if not exist "data\cleaned_reviews.csv" (
        echo [WARNING] cleaned_reviews.csv not found
        echo [INFO] Please ensure data file exists in data directory
        echo.
    )
)

echo ========================================
echo Starting variable extraction script
echo ========================================
echo.

REM 运行 Python 脚本
%PYTHON_CMD% variable_extraction.py

REM 检查运行结果
if errorlevel 1 (
    echo.
    echo [ERROR] Script failed with error code: %errorlevel%
    echo.
    pause
    exit /b %errorlevel%
) else (
    echo.
    echo [SUCCESS] Script completed successfully!
    echo.
)

pause

