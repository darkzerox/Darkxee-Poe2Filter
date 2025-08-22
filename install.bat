@echo off
chcp 65001 >nul
echo ========================================
echo    POE2 Filter Installer
echo ========================================
echo.
echo กำลังตรวจสอบ Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ Python กรุณาติดตั้ง Python 3.8+ ก่อน
    echo ดาวน์โหลดได้ที่: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ พบ Python แล้ว
echo.
echo กำลังติดตั้ง dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ไม่สามารถติดตั้ง dependencies ได้
    pause
    exit /b 1
)

echo ✅ ติดตั้ง dependencies สำเร็จ
echo.
echo กำลังเปิด installer...
python run_installer.py --gui

echo.
echo กด Enter เพื่อปิด...
pause
