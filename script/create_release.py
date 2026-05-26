#!/usr/bin/env python3
"""
DZX PoE2 Filter Release Automation Script
========================================

This script automates the release process entirely on the local machine:
1. Reads the version from config.json
2. Runs the filter build script (start_build.py)
3. Bundles compiled filters into a ZIP archive
4. Compiles the Windows EXE Launcher using PyInstaller
5. Creates git tags (vX.Y.Z and X.Y.Z) locally
6. Pushes branches and tags to GitHub
7. Publishes a GitHub Release with the zip and exe assets using the GitHub CLI

Usage:
  python script/create_release.py
"""

import os
import sys
import json
import shutil
import zipfile
import subprocess
from pathlib import Path

# Setup paths
script_dir = Path(__file__).parent
project_root = script_dir.parent

def run_command(cmd, cwd=project_root):
    """Helper to run a shell command and check for errors"""
    print(f"🚀 Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(f"❌ Command failed with exit code {res.returncode}: {' '.join(cmd)}")
        sys.exit(res.returncode)
    return res

def load_version():
    """Load current version from config.json"""
    config_path = project_root / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config["project"]["version"]

def zip_filters():
    """Create a ZIP archive of the compiled filter files"""
    zip_path = project_root / "dzx-poe2-filter.zip"
    filter_dir = project_root / "dist" / "filter"
    
    print(f"📦 Packaging filters to {zip_path.name}...")
    
    if not filter_dir.exists():
        print(f"❌ Filter directory {filter_dir} does not exist. Run start_build.py first.")
        sys.exit(1)
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in filter_dir.rglob('*'):
            if file.is_file():
                # Write file with a relative path inside the zip
                zipf.write(file, file.relative_to(filter_dir))
                
    print(f"✅ Successfully created {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return zip_path

def check_gh_cli():
    """Verify that gh CLI is installed and authenticated"""
    try:
        res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        if res.returncode != 0:
            print("❌ GitHub CLI (gh) is not authenticated. Please run 'gh auth login'.")
            sys.exit(1)
        print("✅ GitHub CLI authenticated successfully.")
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) is not installed. Please install it first.")
        sys.exit(1)

def main():
    version = load_version()
    print(f"🌟 DZX PoE2 Filter Local Release System")
    print(f"======================================")
    print(f"Target Version: {version}")
    
    # Confirm release
    confirm = input(f"Are you sure you want to release version {version}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Build cancelled.")
        sys.exit(0)
        
    # Check GitHub CLI authentication
    check_gh_cli()
    
    # Step 1: Run filter compilation
    print("\n[Step 1/5] Compiling filter files...")
    run_command([sys.executable, "-X", "utf8", "script/start_build.py"])
    
    # Step 2: Zip filters
    print("\n[Step 2/5] Zipping compiled filters...")
    zip_path = zip_filters()
    
    # Step 3: Build EXE Launcher
    print("\n[Step 3/5] Compiling Windows EXE Launcher...")
    run_command([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name", "DZX-PoE2-Filter-Launcher",
        "--add-data", "dist/filter;filters",
        "--add-data", "dzx_filter/images;dzx_filter/images",
        "--add-data", "config.json;.",
        "script/installer_gui.py"
    ])
    exe_path = project_root / "dist" / "DZX-PoE2-Filter-Launcher.exe"
    if not exe_path.exists():
        print(f"❌ Launcher compilation failed. Executable not found at {exe_path}")
        sys.exit(1)
    print(f"✅ Successfully compiled launcher: {exe_path.name}")
    
    # Step 4: Tag commits locally
    print("\n[Step 4/5] Creating local git tags...")
    tag_v = f"v{version}"
    tag_no_v = version
    
    # Delete tags if they exist locally
    subprocess.run(["git", "tag", "-d", tag_v], capture_output=True)
    subprocess.run(["git", "tag", "-d", tag_no_v], capture_output=True)
    
    # Create tags
    run_command(["git", "tag", "-a", tag_v, "-m", f"Release {tag_v}"])
    run_command(["git", "tag", "-a", tag_no_v, "-m", f"Release {tag_no_v}"])
    
    # Step 5: Push tags/branches and create GitHub release
    print("\n[Step 5/5] Pushing to GitHub and creating release...")
    # Delete remote tags first to prevent conflicts
    print(f"🧹 Cleaning remote tags {tag_v} and {tag_no_v} on origin...")
    subprocess.run(["git", "push", "origin", "--delete", tag_v], capture_output=True)
    subprocess.run(["git", "push", "origin", "--delete", tag_no_v], capture_output=True)
    
    # Delete old GitHub release if it exists
    print(f"🧹 Cleaning old GitHub release {tag_v} if exists...")
    subprocess.run(["gh", "release", "delete", tag_v, "-y"], capture_output=True)
    
    # Push master, develop, and the tags
    run_command(["git", "push", "origin", "master", "develop", tag_v, tag_no_v])
    
    # Create the release on GitHub
    release_cmd = [
        "gh", "release", "create", tag_v,
        str(zip_path),
        str(exe_path),
        "--repo", "darkzerox/Darkxee-Poe2Filter",
        "--title", f"Darkxee-Poe2Filter {version}",
        "--generate-notes"
    ]
    
    # Check if prerelease
    if "beta" in version.lower() or "alpha" in version.lower():
        release_cmd.append("--prerelease")
        print("ℹ️ Tag marked as pre-release because version name contains 'beta' or 'alpha'")
        
    run_command(release_cmd)
    
    print(f"\n🎉 Successfully created and published release {tag_v} on GitHub!")
    print(f"Check it out at: https://github.com/darkzerox/Darkxee-Poe2Filter/releases/tag/{tag_v}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Release process cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
