#!/bin/bash

echo "========================================"
echo "    POE2 Filter Installer"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ไม่พบ Python กรุณาติดตั้ง Python 3.8+ ก่อน"
    echo "macOS: brew install python3"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ พบ Python แล้ว"
echo

# Check Python version
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version ต้องเป็น 3.8+ (ปัจจุบัน: $python_version)"
    exit 1
fi

echo "✅ Python version: $python_version"
echo

# Install dependencies
echo "กำลังติดตั้ง dependencies..."
if ! python3 -m pip install -r requirements.txt; then
    echo "❌ ไม่สามารถติดตั้ง dependencies ได้"
    exit 1
fi

echo "✅ ติดตั้ง dependencies สำเร็จ"
echo

# Run installer
echo "กำลังเปิด installer..."
python3 run_installer.py --gui

echo
echo "การติดตั้งเสร็จสิ้น"
