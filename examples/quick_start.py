#!/usr/bin/env python3
"""
Quick Start Example for POE2 Filter Installer
ตัวอย่างการใช้งานอย่างรวดเร็ว
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def quick_install():
    """Quick install example"""
    try:
        from installer import POE2FilterInstaller
        
        print("🚀 POE2 Filter Installer - Quick Start")
        print("=" * 40)
        
        # Create installer instance
        installer = POE2FilterInstaller()
        
        # Find POE2 directory
        print("🔍 กำลังค้นหาโฟลเดอร์ POE2...")
        poe2_path = installer.find_poe2_directory()
        
        if not poe2_path:
            print("❌ ไม่พบโฟลเดอร์ POE2 กรุณาติดตั้งเกมก่อน")
            return False
        
        print(f"✅ พบโฟลเดอร์ POE2: {poe2_path}")
        
        # Check for updates
        print("🔄 กำลังตรวจสอบอัพเดท...")
        if installer.check_for_updates():
            print("📦 มีอัพเดทใหม่ กำลังอัพเดท...")
            if installer.update_filters():
                print("✅ อัพเดทสำเร็จ!")
            else:
                print("⚠️  อัพเดทล้มเหลว กำลังติดตั้งเวอร์ชันปัจจุบัน...")
                if installer.install_filters(poe2_path):
                    print("✅ ติดตั้งสำเร็จ!")
                else:
                    print("❌ ติดตั้งล้มเหลว")
                    return False
        else:
            print("📦 ไม่มีอัพเดทใหม่ กำลังติดตั้งเวอร์ชันปัจจุบัน...")
            if installer.install_filters(poe2_path):
                print("✅ ติดตั้งสำเร็จ!")
            else:
                print("❌ ติดตั้งล้มเหลว")
                return False
        
        return True
        
    except Exception as e:
        print(f"💥 เกิดข้อผิดพลาด: {e}")
        return False

def check_status():
    """Check installation status"""
    try:
        from installer import POE2FilterInstaller
        from filter_manager import FilterManager
        
        installer = POE2FilterInstaller()
        manager = FilterManager()
        
        poe2_path = installer.find_poe2_directory()
        if poe2_path:
            status = manager.get_installation_status(poe2_path)
            
            print("\n📊 สถานะการติดตั้ง:")
            print(f"   Filters ติดตั้งแล้ว: {'✅' if status['filters_installed'] else '❌'}")
            print(f"   dzx_filter ติดตั้งแล้ว: {'✅' if status['dzx_filter_installed'] else '❌'}")
            print(f"   จำนวน filters: {status['filters_count']}")
            print(f"   ขนาด dzx_filter: {status['dzx_filter_size']} bytes")
            
            if status['last_modified']:
                print(f"   แก้ไขล่าสุด: {status['last_modified']}")
        
        # List backups
        backups = manager.list_backups()
        print(f"\n💾 จำนวน backups: {len(backups)}")
        
        return True
        
    except Exception as e:
        print(f"💥 เกิดข้อผิดพลาดในการตรวจสอบสถานะ: {e}")
        return False

if __name__ == "__main__":
    print("POE2 Filter Installer - Quick Start Examples")
    print("=" * 50)
    
    # Quick install
    if quick_install():
        print("\n🎉 การติดตั้งเสร็จสิ้น!")
        
        # Check status
        check_status()
    else:
        print("\n❌ การติดตั้งล้มเหลว")
        sys.exit(1)
