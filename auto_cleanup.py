#!/usr/bin/env python3
"""
Script automation สำหรับ cleanup releases เก่าอัตโนมัติ
ใช้ใน CI/CD หรือเมื่อมีการ build release ใหม่
"""

import os
import shutil
import re
from pathlib import Path
import json
import argparse

def get_latest_release():
    """หา release ล่าสุดจาก folder releases"""
    releases_dir = Path('releases')
    if not releases_dir.exists():
        return None
    
    version_folders = []
    for folder in releases_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('v'):
            version_match = re.match(r'v(\d+\.\d+\.\d+)', folder.name)
            if version_match:
                version = version_match.group(1)
                version_folders.append((version, folder))
    
    if not version_folders:
        return None
    
    version_folders.sort(key=lambda x: [int(n) for n in x[0].split('.')], reverse=True)
    return version_folders[0][1]

def auto_cleanup_releases(keep_count=1, dry_run=False):
    """Cleanup releases เก่าอัตโนมัติ"""
    latest_release = get_latest_release()
    
    if not latest_release:
        print("❌ ไม่พบ releases folder")
        return
    
    releases_dir = Path('releases')
    version_folders = []
    
    # รวบรวม releases ทั้งหมด
    for folder in releases_dir.iterdir():
        if folder.is_dir() and folder.name.startswith('v'):
            version_match = re.match(r'v(\d+\.\d+\.\d+)', folder.name)
            if version_match:
                version = version_match.group(1)
                version_folders.append((version, folder))
    
    if len(version_folders) <= keep_count:
        print(f"✨ มี releases {len(version_folders)} รายการ ไม่เกิน {keep_count} ที่ต้องการเก็บ")
        return
    
    # เรียงลำดับตาม version
    version_folders.sort(key=lambda x: [int(n) for n in x[0].split('.')], reverse=True)
    
    # แยก releases ที่จะเก็บและลบ
    keep_folders = version_folders[:keep_count]
    delete_folders = version_folders[keep_count:]
    
    print(f"🔍 Releases ที่จะเก็บ: {[f[1].name for f in keep_folders]}")
    print(f"🗑️  Releases ที่จะลบ: {[f[1].name for f in delete_folders]}")
    
    if dry_run:
        print("🔍 Dry run mode - ไม่มีการลบจริง")
        return
    
    # ลบ releases เก่า
    deleted_count = 0
    for version, folder in delete_folders:
        try:
            print(f"🗑️  ลบ {folder.name}...")
            shutil.rmtree(folder)
            deleted_count += 1
            print(f"✅ ลบ {folder.name} เสร็จแล้ว")
        except Exception as e:
            print(f"❌ ไม่สามารถลบ {folder.name}: {e}")
    
    print(f"\n🎉 ลบ releases เก่าเสร็จแล้ว {deleted_count} รายการ")
    print(f"📁 เหลือเพียง: {[f[1].name for f in keep_folders]}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Auto cleanup old releases')
    parser.add_argument('--keep', type=int, default=1, 
                       help='จำนวน releases ที่ต้องการเก็บ (default: 1)')
    parser.add_argument('--dry-run', action='store_true',
                       help='แสดงผลลัพธ์โดยไม่ลบจริง')
    parser.add_argument('--auto', action='store_true',
                       help='ทำงานอัตโนมัติโดยไม่ถามยืนยัน')
    
    args = parser.parse_args()
    
    print("🧹 เริ่มต้นการ cleanup releases อัตโนมัติ...")
    print("=" * 60)
    
    if not args.auto:
        response = input(f"⚠️  จะลบ releases เก่า เหลือ {args.keep} รายการล่าสุด? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ ยกเลิกการ cleanup")
            return
    
    auto_cleanup_releases(keep_count=args.keep, dry_run=args.dry_run)
    
    print("\n" + "=" * 60)
    print("🏁 เสร็จสิ้นการ cleanup releases")

if __name__ == "__main__":
    main()
