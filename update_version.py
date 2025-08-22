#!/usr/bin/env python3
"""
POE2 Filter Installer - Version Update Script
อัพเดท version ในทุกไฟล์ที่เกี่ยวข้อง พร้อมสร้าง release package และ cleanup releases เก่า
"""

import os
import sys
import json
import re
import subprocess
import shutil
import zipfile
import requests
from pathlib import Path
from datetime import datetime

# Import cleanup functions
from auto_cleanup import auto_cleanup_releases

class VersionUpdater:
    """Version updater for POE2 Filter Installer"""
    
    def __init__(self):
        self.version_files = {
            "config/settings.json": {
                "pattern": r'"current_version":\s*"[^"]*"',
                "replacement": '"current_version": "{version}"'
            },
            "src/__init__.py": {
                "pattern": r'__version__\s*=\s*["\'][^"\']+["\']',
                "replacement": '__version__ = "{version}"'
            }
        }
        
        self.changelog_template = """
### v{version}
- 🎯 Version update: {version}
- 📅 Release date: {date}
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

"""
        
        # GitHub configuration
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = self.get_github_repo()
    
    def get_current_version(self):
        """Get current version from config"""
        try:
            with open("config/settings.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get("current_version", "unknown")
        except Exception as e:
            print(f"❌ Error reading current version: {e}")
            return None
    
    def update_version_in_file(self, file_path, new_version):
        """Update version in specific file"""
        try:
            if not os.path.exists(file_path):
                print(f"⚠️  File not found: {file_path}")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_config = self.version_files[file_path]
            old_pattern = file_config["pattern"]
            new_replacement = file_config["replacement"].format(version=new_version)
            
            # Check if version needs updating
            if re.search(old_pattern, content):
                new_content = re.sub(old_pattern, new_replacement, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Updated {file_path} to version {new_version}")
                return True
            else:
                print(f"⚠️  Version pattern not found in {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
            return False
    
    def update_changelog(self, new_version):
        """Update changelog in README.md"""
        try:
            readme_path = "README.md"
            if not os.path.exists(readme_path):
                print("⚠️  README.md not found")
                return False
            
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find changelog section
            changelog_start = content.find("## Changelog")
            if changelog_start == -1:
                print("⚠️  Changelog section not found in README.md")
                return False
            
            # Find the first version entry
            version_pattern = r'### v\d+\.\d+\.\d+'
            first_version_match = re.search(version_pattern, content[changelog_start:])
            
            if first_version_match:
                insert_pos = changelog_start + first_version_match.start()
                
                # Create new changelog entry
                new_entry = self.changelog_template.format(
                    version=new_version,
                    date=datetime.now().strftime("%Y-%m-%d")
                )
                
                # Insert new changelog entry
                new_content = content[:insert_pos] + new_entry + content[insert_pos:]
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Updated README.md changelog for version {new_version}")
                return True
            else:
                print("⚠️  No version entries found in changelog")
                return False
                
        except Exception as e:
            print(f"❌ Error updating changelog: {e}")
            return False
    
    def build_installer(self):
        """Build installer using build script"""
        try:
            print("🔨 Building installer...")
            result = subprocess.run([sys.executable, "build_installer.py"], 
                                 capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Installer built successfully")
                return True
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Build timed out")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def create_release_package(self, new_version):
        """Create release package"""
        try:
            print("📦 Creating release package...")
            
            # Create release directory
            release_dir = Path(f"releases/v{new_version}")
            release_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy installer package
            installer_src = Path("dist/POE2FilterInstaller_Package")
            installer_dest = release_dir / "POE2FilterInstaller_Package"
            
            if installer_dest.exists():
                shutil.rmtree(installer_dest)
            
            if installer_src.exists():
                shutil.copytree(installer_src, installer_dest)
                print(f"📁 Copied installer to: {installer_dest}")
            else:
                print("❌ Installer package not found")
                return False
            
            # Create zip file
            zip_path = release_dir / f"POE2FilterInstaller-v{new_version}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(installer_dest):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, installer_dest.parent)
                        zipf.write(file_path, arcname)
            
            print(f"📦 Created zip file: {zip_path}")
            
            # Create release notes
            release_notes = self.create_release_notes(new_version)
            notes_path = release_dir / "RELEASE_NOTES.md"
            with open(notes_path, 'w', encoding='utf-8') as f:
                f.write(release_notes)
            
            print(f"📝 Created release notes: {notes_path}")
            
            # Show summary
            zip_size = zip_path.stat().st_size / (1024 * 1024)
            print(f"\n🎉 Release package created successfully!")
            print(f"📦 Package: {zip_path}")
            print(f"📊 Size: {zip_size:.1f} MB")
            print(f"📁 Directory: {release_dir}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating release package: {e}")
            return False
    
    def create_release_notes(self, new_version):
        """Create release notes content"""
        return f"""# POE2 Filter Installer v{new_version}

## 🎯 สิ่งที่เปลี่ยนแปลง

### ✅ คุณสมบัติใหม่
- Version update to {new_version}
- Performance improvements
- Bug fixes and stability enhancements

### 🚀 การปรับปรุง
- Optimized installation process
- Enhanced error handling
- Improved user experience

## 📥 วิธีการติดตั้ง

### สำหรับ Windows:
1. ดาวน์โหลด `POE2FilterInstaller-v{new_version}.zip`
2. แตกไฟล์และรัน `install.bat`
3. หรือรัน `POE2FilterInstaller.exe --gui`

### สำหรับ macOS/Linux:
1. ดาวน์โหลด `POE2FilterInstaller-v{new_version}.zip`
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
🏷️ Version: v{new_version}
"""
    
    def git_operations(self, new_version):
        """Perform git operations"""
        try:
            print("🔧 Performing git operations...")
            
            # Check git status
            result = subprocess.run(["git", "status", "--porcelain"], 
                                 capture_output=True, text=True)
            
            if result.stdout.strip():
                print("📝 Staging changes...")
                subprocess.run(["git", "add", "."], check=True)
                
                print("💾 Committing changes...")
                subprocess.run(["git", "commit", "-m", f"chore: bump version to {new_version}"], 
                             check=True)
                
                print("✅ Changes committed successfully")
            else:
                print("ℹ️  No changes to commit")
            
            # Create and push tag
            tag_name = f"v{new_version}"
            print(f"🏷️  Creating tag: {tag_name}")
            
            subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], 
                         check=True)
            
            print(f"📤 Pushing tag to origin...")
            subprocess.run(["git", "push", "origin", tag_name], check=True)
            
            print("✅ Git operations completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error in git operations: {e}")
            return False
    
    def verify_version_consistency(self, new_version):
        """Verify that all files have the same version"""
        print("🔍 Verifying version consistency...")
        
        all_consistent = True
        
        # Check config file
        current_version = self.get_current_version()
        if current_version == new_version:
            print(f"✅ config/settings.json: {current_version}")
        else:
            print(f"❌ config/settings.json: {current_version} (expected: {new_version})")
            all_consistent = False
        
        # Check src/__init__.py
        try:
            with open("src/__init__.py", 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                if match and match.group(1) == new_version:
                    print(f"✅ src/__init__.py: {match.group(1)}")
                else:
                    print(f"❌ src/__init__.py: {match.group(1) if match else 'not found'} (expected: {new_version})")
                    all_consistent = False
        except Exception as e:
            print(f"❌ Error checking src/__init__.py: {e}")
            all_consistent = False
        
        if all_consistent:
            print("🎯 All version files are consistent!")
        else:
            print("⚠️  Version inconsistency detected!")
        
        return all_consistent
    
    def get_github_repo(self):
        """Get GitHub repository from git remote"""
        try:
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                # Extract repo from git@github.com:username/repo.git or https://github.com/username/repo.git
                if 'github.com' in remote_url:
                    if remote_url.startswith('git@'):
                        repo = remote_url.split(':')[1].replace('.git', '')
                    else:
                        repo = remote_url.split('github.com/')[1].replace('.git', '')
                    return repo
            return None
        except Exception:
            return None
    
    def create_github_release(self, new_version, release_notes):
        """Create GitHub release"""
        if not self.github_token:
            print("⚠️  GITHUB_TOKEN not set. Skipping GitHub release creation.")
            return False
        
        if not self.github_repo:
            print("⚠️  Could not determine GitHub repository. Skipping GitHub release creation.")
            return False
        
        try:
            print("🌐 Creating GitHub release...")
            
            # GitHub API endpoint
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases"
            
            # Release data
            release_data = {
                "tag_name": f"v{new_version}",
                "name": f"POE2 Filter Installer v{new_version}",
                "body": release_notes,
                "draft": False,
                "prerelease": False
            }
            
            # Create release
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.post(api_url, json=release_data, headers=headers)
            response.raise_for_status()
            
            release_info = response.json()
            release_id = release_info["id"]
            print(f"✅ GitHub release created: {release_info['html_url']}")
            
            # Upload assets
            self.upload_release_assets(release_id, new_version)
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating GitHub release: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def upload_release_assets(self, release_id, new_version):
        """Upload release assets to GitHub"""
        try:
            print("📤 Uploading release assets...")
            
            # Path to release assets
            release_dir = Path(f"releases/v{new_version}")
            zip_file = release_dir / f"POE2FilterInstaller-v{new_version}.zip"
            
            if not zip_file.exists():
                print("⚠️  Release zip file not found")
                return False
            
            # GitHub API endpoint for assets
            upload_url = f"https://uploads.github.com/repos/{self.github_repo}/releases/{release_id}/assets"
            
            # Upload zip file
            with open(zip_file, 'rb') as f:
                params = {"name": zip_file.name}
                headers = {
                    "Authorization": f"token {self.github_token}",
                    "Content-Type": "application/zip"
                }
                
                response = requests.post(upload_url, params=params, data=f, headers=headers)
                response.raise_for_status()
                
                print(f"✅ Uploaded: {zip_file.name}")
            
            # Upload installer package folder as additional asset
            installer_dir = release_dir / "POE2FilterInstaller_Package"
            if installer_dir.exists():
                # Create a tar.gz of the installer package
                tar_file = release_dir / f"POE2FilterInstaller-v{new_version}-package.tar.gz"
                
                import tarfile
                with tarfile.open(tar_file, "w:gz") as tar:
                    tar.add(installer_dir, arcname=installer_dir.name)
                
                # Upload tar.gz file
                with open(tar_file, 'rb') as f:
                    params = {"name": tar_file.name}
                    headers = {
                        "Authorization": f"token {self.github_token}",
                        "Content-Type": "application/gzip"
                    }
                    
                    response = requests.post(upload_url, params=params, data=f, headers=headers)
                    response.raise_for_status()
                    
                    print(f"✅ Uploaded: {tar_file.name}")
                
                # Clean up tar file
                tar_file.unlink()
            
            print("✅ All assets uploaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading assets: {e}")
            return False
    
    def cleanup_old_releases(self, keep_count=1):
        """Cleanup old releases after creating new one"""
        try:
            print("\n🧹 Step 8: Cleaning up old releases...")
            auto_cleanup_releases(keep_count=keep_count, dry_run=False)
            print("✅ Cleanup completed successfully")
            return True
        except Exception as e:
            print(f"⚠️  Cleanup failed: {e}")
            return False

    def update_version(self, new_version, keep_releases=1, skip_cleanup=False):
        """Main version update process"""
        print(f"🚀 Starting version update to {new_version}")
        print("=" * 50)
        
        # 1. Update version in all files
        print("\n📝 Step 1: Updating version in files...")
        all_updated = True
        for file_path in self.version_files:
            if not self.update_version_in_file(file_path, new_version):
                all_updated = False
        
        if not all_updated:
            print("❌ Failed to update all files")
            return False
        
        # 2. Update changelog
        print("\n📚 Step 2: Updating changelog...")
        if not self.update_changelog(new_version):
            print("⚠️  Failed to update changelog")
        
        # 3. Verify consistency
        print("\n🔍 Step 3: Verifying version consistency...")
        if not self.verify_version_consistency(new_version):
            print("❌ Version inconsistency detected")
            return False
        
        # 4. Build installer
        print("\n🔨 Step 4: Building installer...")
        if not self.build_installer():
            print("❌ Failed to build installer")
            return False
        
        # 5. Create release package
        print("\n📦 Step 5: Creating release package...")
        if not self.create_release_package(new_version):
            print("❌ Failed to create release package")
            return False
        
        # 6. Git operations
        print("\n🔧 Step 6: Git operations...")
        if not self.git_operations(new_version):
            print("⚠️  Git operations failed")
        
        # 7. Create GitHub release
        print("\n🌐 Step 7: Creating GitHub release...")
        release_notes = self.create_release_notes(new_version)
        if self.create_github_release(new_version, release_notes):
            print("✅ GitHub release created successfully")
        else:
            print("⚠️  GitHub release creation failed")
        
        # 8. Cleanup old releases
        print("\n🧹 Step 8: Cleaning up old releases...")
        if not skip_cleanup:
            self.cleanup_old_releases(keep_count=keep_releases)

        print("\n🎉 Version update completed successfully!")
        print(f"📋 Next steps:")
        print(f"   1. Test installer on different systems")
        print(f"   2. Announce release to users")
        print(f"   3. Monitor download statistics")
        
        return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='POE2 Filter Installer Version Updater')
    parser.add_argument('new_version', help='New version to update to (e.g., 1.2.0)')
    parser.add_argument('--keep-releases', type=int, default=1, 
                       help='Number of releases to keep after cleanup (default: 1)')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='Skip cleanup of old releases')
    parser.add_argument('--auto', action='store_true',
                       help='Run automatically without confirmation prompts')
    
    args = parser.parse_args()
    new_version = args.new_version
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("❌ Invalid version format. Use format: X.Y.Z (e.g., 1.2.0)")
        sys.exit(1)
    
    updater = VersionUpdater()
    
    # Check GitHub configuration
    if not updater.github_token:
        print("⚠️  GITHUB_TOKEN not set")
        print("📝 To enable automatic GitHub releases, set the environment variable:")
        print("   export GITHUB_TOKEN=your_github_token_here")
        print("   or add to your shell profile (.bashrc, .zshrc, etc.)")
        print()
    
    if not updater.github_repo:
        print("⚠️  Could not determine GitHub repository")
        print("📝 Make sure you have a git remote 'origin' pointing to GitHub")
        print()
    
    # Show current version
    current_version = updater.get_current_version()
    if current_version:
        print(f"📋 Current version: {current_version}")
        print(f"🎯 Target version: {new_version}")
        
        if current_version == new_version:
            print("⚠️  Version is already {new_version}")
            if not args.auto:
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    print("❌ Update cancelled")
                    sys.exit(0)
    
    # Show cleanup settings
    if not args.no_cleanup:
        print(f"🧹 Cleanup settings: Keep {args.keep_releases} latest release(s)")
    else:
        print("🧹 Cleanup: Disabled")
    
    # Confirm update
    if not args.auto:
        response = input(f"\nProceed with version update to {new_version}? (y/N): ")
        if response.lower() != 'y':
            print("❌ Update cancelled")
            sys.exit(0)
    
    # Perform update
    try:
        success = updater.update_version(new_version, keep_releases=args.keep_releases, skip_cleanup=args.no_cleanup)
        if success:
            print("\n✅ Version update completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Version update failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Update cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
