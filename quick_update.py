#!/usr/bin/env python3
"""
Quick Update Script สำหรับ POE2 Filter Installer
ใช้งานง่ายสำหรับการ update version และ cleanup releases
"""

import sys
import subprocess
from pathlib import Path

def show_usage():
    """แสดงวิธีการใช้งาน"""
    print("🚀 POE2 Filter Installer - Quick Update")
    print("=" * 50)
    print("Usage:")
    print("  python quick_update.py <new_version> [options]")
    print()
    print("Examples:")
    print("  python quick_update.py 1.2.0                    # Update to 1.2.0, keep 1 release")
    print("  python quick_update.py 1.2.0 --keep 2          # Update to 1.2.0, keep 2 releases")
    print("  python quick_update.py 1.2.0 --no-cleanup      # Update without cleanup")
    print("  python quick_update.py 1.2.0 --auto            # Auto update without prompts")
    print()
    print("Options:")
    print("  --keep <number>     Keep N latest releases (default: 1)")
    print("  --no-cleanup        Skip cleanup of old releases")
    print("  --auto              Run automatically without confirmation")
    print("  --help              Show this help message")

def check_prerequisites():
    """ตรวจสอบ prerequisites"""
    required_files = [
        "update_version.py",
        "auto_cleanup.py",
        "config/settings.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease make sure you're in the correct directory.")
        return False
    
    return True

def main():
    """Main function"""
    if len(sys.argv) < 2 or "--help" in sys.argv:
        show_usage()
        sys.exit(0)
    
    # ตรวจสอบ prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # สร้าง command arguments
    cmd = [sys.executable, "update_version.py"] + sys.argv[1:]
    
    try:
        print("🚀 Starting version update...")
        print(f"📝 Command: {' '.join(cmd)}")
        print("=" * 50)
        
        # รัน update script
        result = subprocess.run(cmd, check=True)
        
        print("=" * 50)
        print("🎉 Update completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Update failed with exit code: {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n⏹️  Update cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
