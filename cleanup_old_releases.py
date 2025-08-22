#!/usr/bin/env python3
"""
Script สำหรับลบ releases เก่าทิ้ง เหลือเฉพาะปัจจุบัน
ใช้เมื่อมีการอัพเดท version ใหม่
"""

import os
import shutil
import re
from pathlib import Path
import json

def get_current_version():
    """อ่าน version ปัจจุบันจาก config"""
    try:
        with open('config/settings.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('version', '1.0.0')
    except:
        return '1.0.0'

def get_latest_release():
    """หา release ล่าสุดจาก folder releases"""
    releases_dir = Path('releases')
    if not releases_dir.exists():
        return None
    
    # หา folder ที่ขึ้นต้นด้วย v และมี version number
    version_folders = []
    for folder in releases_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('v'):
            # แยก version number ออกมา
            version_match = re.match(r'v(\d+\.\d+\.\d+)', folder.name)
            if version_match:
                version = version_match.group(1)
                version_folders.append((version, folder))
    
    if not version_folders:
        return None
    
    # เรียงลำดับตาม version และเอาใหม่สุด
    version_folders.sort(key=lambda x: [int(n) for n in x[0].split('.')], reverse=True)
    return version_folders[0][1]

def cleanup_old_releases():
    """ลบ releases เก่าทิ้ง เหลือเฉพาะปัจจุบัน"""
    current_version = get_current_version()
    latest_release = get_latest_release()
    
    if not latest_release:
        print("❌ ไม่พบ releases folder")
        return
    
    print(f"🔍 Version ปัจจุบัน: {current_version}")
    print(f"🔍 Release ล่าสุด: {latest_release.name}")
    
    releases_dir = Path('releases')
    deleted_count = 0
    
    for folder in releases_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('v'):
            if folder != latest_release:
                try:
                    print(f"🗑️  ลบ {folder.name}...")
                    shutil.rmtree(folder)
                    deleted_count += 1
                    print(f"✅ ลบ {folder.name} เสร็จแล้ว")
                except Exception as e:
                    print(f"❌ ไม่สามารถลบ {folder.name}: {e}")
    
    if deleted_count > 0:
        print(f"\n🎉 ลบ releases เก่าเสร็จแล้ว {deleted_count} รายการ")
        print(f"📁 เหลือเพียง: {latest_release.name}")
    else:
        print("\n✨ ไม่มี releases เก่าที่ต้องลบ")

def main():
    """Main function"""
    print("🧹 เริ่มต้นการลบ releases เก่า...")
    print("=" * 50)
    
    # ยืนยันก่อนลบ
    response = input("⚠️  คุณแน่ใจหรือไม่ที่จะลบ releases เก่าทิ้ง? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ ยกเลิกการลบ")
        return
    
    cleanup_old_releases()
    
    print("\n" + "=" * 50)
    print("🏁 เสร็จสิ้นการลบ releases เก่า")

if __name__ == "__main__":
    main()
