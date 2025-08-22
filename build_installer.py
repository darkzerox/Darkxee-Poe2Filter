#!/usr/bin/env python3
"""
Build script for POE2 Filter Installer
สร้าง executable file สำหรับ installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("กำลังติดตั้ง dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("ติดตั้ง dependencies สำเร็จ")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ข้อผิดพลาดในการติดตั้ง dependencies: {e}")
        return False

def build_executable():
    """Build executable using PyInstaller"""
    print("กำลังสร้าง executable...")
    
    try:
        # PyInstaller command
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=POE2FilterInstaller",
            "--add-data=config:config",
            "--add-data=dzx_filter:dzx_filter",
            "--add-data=*.filter:.",
            "src/installer.py"
        ]
        
        subprocess.check_call(cmd)
        print("สร้าง executable สำเร็จ")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ข้อผิดพลาดในการสร้าง executable: {e}")
        return False

def create_installer_package():
    """Create installer package with all necessary files"""
    print("กำลังสร้าง installer package...")
    
    try:
        # Create dist directory
        dist_dir = Path("dist/POE2FilterInstaller_Package")
        
        # Remove existing directory if it exists
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
            print("ลบโฟลเดอร์เก่าแล้ว")
        
        dist_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy executable (check for both .exe and macOS executable)
        exe_src = Path("dist/POE2FilterInstaller.exe")
        if not exe_src.exists():
            # Try macOS executable
            exe_src = Path("dist/POE2FilterInstaller")
        
        if exe_src.exists() and exe_src.is_file():
            shutil.copy2(exe_src, dist_dir)
            print(f"คัดลอก executable: {exe_src.name}")
        else:
            print("⚠️  ไม่พบ executable file")
        
        # Copy config
        config_src = Path("config")
        if config_src.exists():
            shutil.copytree(config_src, dist_dir / "config", dirs_exist_ok=True)
            print("คัดลอก config folder")
        
        # Copy filter files
        filter_count = 0
        for filter_file in Path(".").glob("*.filter"):
            shutil.copy2(filter_file, dist_dir)
            filter_count += 1
        
        if filter_count > 0:
            print(f"คัดลอก filter files: {filter_count} ไฟล์")
        
        # Copy dzx_filter folder
        dzx_filter_src = Path("dzx_filter")
        if dzx_filter_src.exists():
            shutil.copytree(dzx_filter_src, dist_dir / "dzx_filter", dirs_exist_ok=True)
            print("คัดลอก dzx_filter folder")
        
        # Copy README and LICENSE
        for file in ["README.md", "LICENSE"]:
            if Path(file).exists():
                shutil.copy2(file, dist_dir)
                print(f"คัดลอก {file}")
        
        # Create batch file for easy installation (Windows)
        batch_content = """@echo off
chcp 65001 >nul
echo ========================================
echo    POE2 Filter Installer
echo ========================================
echo.
echo กำลังเปิด installer...
POE2FilterInstaller.exe --gui
echo.
echo กด Enter เพื่อปิด...
pause
"""
        
        with open(dist_dir / "install.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        
        # Create shell script for macOS/Linux
        shell_content = """#!/bin/bash
echo "========================================"
echo "    POE2 Filter Installer"
echo "========================================"
echo.
echo "กำลังเปิด installer..."
./POE2FilterInstaller --gui
echo.
echo "การติดตั้งเสร็จสิ้น"
"""
        
        with open(dist_dir / "install.sh", "w", encoding="utf-8") as f:
            f.write(shell_content)
        
        # Make shell script executable
        os.chmod(dist_dir / "install.sh", 0o755)
        
        print("สร้าง installer package สำเร็จ")
        return True
        
    except Exception as e:
        print(f"ข้อผิดพลาดในการสร้าง installer package: {e}")
        return False

def main():
    """Main build process"""
    print("POE2 Filter Installer - Build Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("src/installer.py").exists():
        print("ข้อผิดพลาด: กรุณารัน script นี้จากโฟลเดอร์หลักของโปรเจค")
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Create installer package
    if not create_installer_package():
        return False
    
    print("\nBuild เสร็จสิ้น!")
    print("ไฟล์ installer อยู่ในโฟลเดอร์: dist/POE2FilterInstaller/")
    print("รัน install.bat เพื่อติดตั้ง")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
