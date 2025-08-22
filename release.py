#!/usr/bin/env python3
"""
Release Script for POE2 Filter Installer
สร้าง release ใหม่และ package สำหรับการแจกจ่าย
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def get_current_version():
    """Get current version from config"""
    import json
    with open("config/settings.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config["current_version"]

def create_release_package():
    """Create release package"""
    version = get_current_version()
    print(f"🚀 Creating release package for version {version}")
    
    # Build installer
    print("📦 Building installer...")
    result = subprocess.run([sys.executable, "build_installer.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Build failed: {result.stderr}")
        return False
    
    print("✅ Build completed successfully")
    
    # Create release directory
    release_dir = Path(f"releases/v{version}")
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy installer package
    installer_src = Path("dist/POE2FilterInstaller_Package")
    installer_dest = release_dir / "POE2FilterInstaller_Package"
    
    if installer_dest.exists():
        shutil.rmtree(installer_dest)
    
    shutil.copytree(installer_src, installer_dest)
    print(f"📁 Copied installer to: {installer_dest}")
    
    # Create zip file
    zip_path = release_dir / f"POE2FilterInstaller-v{version}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(installer_dest):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, installer_dest.parent)
                zipf.write(file_path, arcname)
    
    print(f"📦 Created zip file: {zip_path}")
    
    # Create release notes
    release_notes = f"""# POE2 Filter Installer v{version}

## 🎯 สิ่งที่เปลี่ยนแปลง

### ✅ คุณสมบัติใหม่
- ปรับปรุง installer ให้ติดตั้งเฉพาะไฟล์ที่จำเป็น
- ติดตั้งเฉพาะ dzx-poe2.filter และ dzx-poe2-*.filter
- ติดตั้งเฉพาะ /dzx_filter/soundeffect/**/**
- ปรับปรุง GUI ให้แสดง default paths และ browse ได้
- เพิ่มการ validate โฟลเดอร์ที่เลือก

### 🚀 การปรับปรุง
- ลดขนาด package ลงอย่างมาก
- ติดตั้งเร็วขึ้น
- ติดตั้งเฉพาะสิ่งที่จำเป็น
- รองรับการ backup และ restore ที่ถูกต้อง

## 📥 วิธีการติดตั้ง

### สำหรับ Windows:
1. ดาวน์โหลด `POE2FilterInstaller-v{version}.zip`
2. แตกไฟล์และรัน `install.bat`
3. หรือรัน `POE2FilterInstaller.exe --gui`

### สำหรับ macOS/Linux:
1. ดาวน์โหลด `POE2FilterInstaller-v{version}.zip`
2. แตกไฟล์และรัน `./install.sh`
3. หรือรัน `./POE2FilterInstaller --gui`

## 🎮 ไฟล์ที่ติดตั้ง

- **Filter Files:** dzx-poe2.filter และ dzx-poe2-*.filter
- **Sound Effects:** /dzx_filter/soundeffect/**/**
- **Location:** %userprofile%\\Documents\\My Games\\Path of Exile 2

## 🔧 การแก้ไขปัญหา

หากพบปัญหา:
1. ตรวจสอบ installer.log
2. ใช้ปุ่ม "ตรวจหาอัตโนมัติ" ใน GUI
3. เลือกโฟลเดอร์ด้วยตนเองหากจำเป็น

---

📅 Release Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🏷️ Version: v{version}
"""
    
    notes_path = release_dir / "RELEASE_NOTES.md"
    with open(notes_path, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print(f"📝 Created release notes: {notes_path}")
    
    # Show summary
    print("\n🎉 Release package created successfully!")
    print(f"📦 Package: {zip_path}")
    print(f"📝 Notes: {notes_path}")
    print(f"📁 Directory: {release_dir}")
    
    # Show file sizes
    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"📊 Package size: {zip_size:.1f} MB")
    
    return True

def create_git_tag():
    """Create git tag for release"""
    version = get_current_version()
    tag_name = f"v{version}"
    
    try:
        # Check if tag already exists
        result = subprocess.run(["git", "tag", "-l", tag_name], capture_output=True, text=True)
        if tag_name in result.stdout:
            print(f"⚠️  Tag {tag_name} already exists")
            return False
        
        # Create tag
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], check=True)
        print(f"🏷️  Created git tag: {tag_name}")
        
        # Push tag
        subprocess.run(["git", "push", "origin", tag_name], check=True)
        print(f"📤 Pushed tag to origin: {tag_name}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

def main():
    """Main release process"""
    print("🚀 POE2 Filter Installer - Release Process")
    print("=" * 50)
    
    # Get current version
    version = get_current_version()
    print(f"📋 Current version: {version}")
    
    # Ask for confirmation
    response = input(f"Create release for version {version}? (y/N): ")
    if response.lower() != 'y':
        print("❌ Release cancelled")
        return
    
    # Create release package
    if not create_release_package():
        print("❌ Release package creation failed")
        return
    
    # Ask for git tag
    response = input("Create git tag? (y/N): ")
    if response.lower() == 'y':
        create_git_tag()
    
    print("\n✅ Release process completed!")
    print(f"🎯 Next steps:")
    print(f"   1. Upload zip file to GitHub releases")
    print(f"   2. Copy release notes to GitHub")
    print(f"   3. Test installer on different systems")
    print(f"   4. Announce release to users")

if __name__ == "__main__":
    main()
