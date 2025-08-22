#!/usr/bin/env python3
"""
Version Check Script
ตรวจสอบ version ใน files ต่างๆ ให้ตรงกัน
"""

import json
import re
from pathlib import Path

def get_versions():
    """Get versions from different files"""
    versions = {}
    
    # Get from config/settings.json
    try:
        with open("config/settings.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
            versions['config'] = config.get("current_version", "unknown")
    except Exception as e:
        versions['config'] = f"error: {e}"
    
    # Get from src/__init__.py
    try:
        with open("src/__init__.py", 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            versions['src'] = match.group(1) if match else "not found"
    except Exception as e:
        versions['src'] = f"error: {e}"
    
    # Get from README.md changelog
    try:
        with open("README.md", 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'### v(\d+\.\d+\.\d+)', content)
            versions['readme'] = match.group(1) if match else "not found"
    except Exception as e:
        versions['readme'] = f"error: {e}"
    
    return versions

def check_version_consistency():
    """Check if all versions are consistent"""
    versions = get_versions()
    
    print("🔍 Version Check Results")
    print("=" * 30)
    
    for source, version in versions.items():
        print(f"{source:10}: {version}")
    
    # Check consistency
    version_values = [v for v in versions.values() if not v.startswith("error") and v != "not found"]
    
    if len(set(version_values)) == 1:
        print(f"\n✅ All versions are consistent: {version_values[0]}")
        return True
    else:
        print(f"\n❌ Version mismatch detected!")
        print(f"   Unique versions found: {set(version_values)}")
        return False

def update_version(new_version):
    """Update version in all files"""
    print(f"🔄 Updating version to: {new_version}")
    
    # Update config/settings.json
    try:
        with open("config/settings.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config["current_version"] = new_version
        
        with open("config/settings.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Updated config/settings.json")
    except Exception as e:
        print(f"❌ Failed to update config: {e}")
    
    # Update src/__init__.py
    try:
        with open("src/__init__.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(
            r'__version__\s*=\s*["\'][^"\']+["\']',
            f'__version__ = "{new_version}"',
            content
        )
        
        with open("src/__init__.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated src/__init__.py")
    except Exception as e:
        print(f"❌ Failed to update src/__init__.py: {e}")
    
    print(f"🎯 Version updated to: {new_version}")
    print("📝 Don't forget to update README.md changelog manually!")

def main():
    """Main version check"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "update":
            if len(sys.argv) > 2:
                new_version = sys.argv[2]
                update_version(new_version)
            else:
                print("❌ Please provide new version: python version_check.py update 1.2.0")
        else:
            print("❌ Unknown command. Use 'update' or no arguments for check")
    else:
        check_version_consistency()

if __name__ == "__main__":
    main()
