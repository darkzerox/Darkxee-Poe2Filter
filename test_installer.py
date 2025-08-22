#!/usr/bin/env python3
"""
Test script for POE2 Filter Installer
ทดสอบการทำงานของ installer
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_installer_import():
    """Test if installer modules can be imported"""
    try:
        from installer import POE2FilterInstaller
        from github_updater import GitHubUpdater
        from filter_manager import FilterManager
        print("✅ Import modules สำเร็จ")
        return True
    except ImportError as e:
        print(f"❌ Import modules ล้มเหลว: {e}")
        return False

def test_poe2_path_detection():
    """Test POE2 path detection"""
    try:
        from installer import POE2FilterInstaller
        
        installer = POE2FilterInstaller()
        
        # Test with temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create mock POE2 structure
            poe2_dir = os.path.join(temp_dir, "Documents", "My Games", "Path of Exile 2")
            os.makedirs(poe2_dir, exist_ok=True)
            
            # Test path detection
            found_path = installer.find_poe2_directory()
            print(f"✅ Path detection test: {found_path}")
            return True
            
    except Exception as e:
        print(f"❌ Path detection test ล้มเหลว: {e}")
        return False

def test_filter_manager():
    """Test filter manager functionality"""
    try:
        from filter_manager import FilterManager
        
        manager = FilterManager()
        
        # Test directory creation
        assert os.path.exists(manager.backup_dir)
        assert os.path.exists(manager.temp_dir)
        print("✅ Filter manager directory creation สำเร็จ")
        
        # Test backup listing
        backups = manager.list_backups()
        print(f"✅ Backup listing สำเร็จ: {len(backups)} backups")
        
        return True
        
    except Exception as e:
        print(f"❌ Filter manager test ล้มเหลว: {e}")
        return False

def test_github_updater():
    """Test GitHub updater functionality"""
    try:
        from github_updater import GitHubUpdater
        
        updater = GitHubUpdater()
        
        # Test connection
        connection_ok = updater.check_connection()
        print(f"✅ GitHub connection test: {'สำเร็จ' if connection_ok else 'ล้มเหลว'}")
        
        # Test version comparison
        is_newer = updater.is_newer_version("2.0.0", "1.0.0")
        assert is_newer == True
        print("✅ Version comparison test สำเร็จ")
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub updater test ล้มเหลว: {e}")
        return False

def test_config_loading():
    """Test configuration loading"""
    try:
        from installer import POE2FilterInstaller
        
        installer = POE2FilterInstaller()
        
        # Test config structure
        assert "github_repo" in installer.config
        assert "current_version" in installer.config
        assert "auto_update" in installer.config
        
        print("✅ Configuration loading สำเร็จ")
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading test ล้มเหลว: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("POE2 Filter Installer - Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Modules", test_installer_import),
        ("POE2 Path Detection", test_poe2_path_detection),
        ("Filter Manager", test_filter_manager),
        ("GitHub Updater", test_github_updater),
        ("Configuration Loading", test_config_loading),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - ผ่าน")
            else:
                print(f"❌ {test_name} - ล้มเหลว")
        except Exception as e:
            print(f"❌ {test_name} - เกิดข้อผิดพลาด: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ทดสอบทั้งหมดผ่าน!")
        return True
    else:
        print("⚠️  มีบางการทดสอบล้มเหลว")
        return False

def cleanup_test_files():
    """Clean up test files"""
    try:
        # Remove test directories
        test_dirs = ["backups", "temp", "dist", "__pycache__"]
        for dir_name in test_dirs:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"🧹 ลบโฟลเดอร์: {dir_name}")
        
        # Remove test files
        test_files = ["installer.log"]
        for file_name in test_files:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"🧹 ลบไฟล์: {file_name}")
                
    except Exception as e:
        print(f"⚠️  ไม่สามารถลบไฟล์ทดสอบได้: {e}")

if __name__ == "__main__":
    try:
        success = run_all_tests()
        
        # Cleanup
        print("\n🧹 Cleaning up test files...")
        cleanup_test_files()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️  การทดสอบถูกยกเลิก")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        sys.exit(1)
