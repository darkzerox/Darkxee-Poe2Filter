# GitHub Setup Guide

## 🔑 การตั้งค่า GitHub Token

### 1. สร้าง Personal Access Token

1. ไปที่ [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. คลิก "Generate new token (classic)"
3. เลือก scopes:
   - `repo` (สำหรับ private repository)
   - `public_repo` (สำหรับ public repository)
4. คลิก "Generate token"
5. คัดลอก token ที่ได้ (เก็บไว้ให้ดี!)

### 2. ตั้งค่า Environment Variable

#### macOS/Linux:
```bash
# ตั้งค่าใน terminal
export GITHUB_TOKEN=your_token_here

# หรือเพิ่มในไฟล์ profile
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.zshrc
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc

# Reload profile
source ~/.zshrc
# หรือ
source ~/.bashrc
```

#### Windows:
```cmd
# Command Prompt
set GITHUB_TOKEN=your_token_here

# PowerShell
$env:GITHUB_TOKEN="your_token_here"

# หรือตั้งค่าใน System Environment Variables
```

### 3. ตรวจสอบการตั้งค่า

```bash
# ตรวจสอบว่า token ถูกตั้งค่าแล้ว
echo $GITHUB_TOKEN

# รัน version update script
python3 update_version.py 1.2.0
```

## 🚀 การใช้งาน

### อัพเดท Version พร้อม GitHub Release:

```bash
# อัพเดทเป็น version 1.2.0
python3 update_version.py 1.2.0
```

### สิ่งที่ script จะทำ:

1. ✅ อัพเดท version ในทุกไฟล์
2. ✅ อัพเดท changelog
3. ✅ Build installer
4. ✅ สร้าง release package
5. ✅ Git commit และ tag
6. ✅ สร้าง GitHub release
7. ✅ อัพโหลด assets (zip, tar.gz)

## 📁 โครงสร้าง Release

```
releases/
└── v1.2.0/
    ├── POE2FilterInstaller_Package/     # Installer package
    ├── POE2FilterInstaller-v1.2.0.zip  # Main zip file
    └── RELEASE_NOTES.md                 # Release notes
```

## 🔧 การแก้ไขปัญหา

### Token ไม่ทำงาน:
- ตรวจสอบว่า token ถูกต้อง
- ตรวจสอบ scopes ที่เลือก
- ตรวจสอบ repository permissions

### Repository ไม่พบ:
- ตรวจสอบ git remote origin
- ตรวจสอบ URL format
- ตรวจสอบ repository access

### Upload ล้มเหลว:
- ตรวจสอบ file size (GitHub limit: 100MB)
- ตรวจสอบ network connection
- ตรวจสอบ token permissions

## 📋 ตัวอย่าง Output

```
🚀 Starting version update to 1.2.0
==================================================

📝 Step 1: Updating version in files...
✅ Updated config/settings.json to version 1.2.0
✅ Updated src/__init__.py to version 1.2.0

📚 Step 2: Updating changelog...
✅ Updated README.md changelog for version 1.2.0

🔍 Step 3: Verifying version consistency...
✅ config/settings.json: 1.2.0
✅ src/__init__.py: 1.2.0
🎯 All version files are consistent!

🔨 Step 4: Building installer...
✅ Installer built successfully

📦 Step 5: Creating release package...
📁 Copied installer to: releases/v1.2.0/POE2FilterInstaller_Package
📦 Created zip file: releases/v1.2.0/POE2FilterInstaller-v1.2.0.zip
📝 Created release notes: releases/v1.2.0/RELEASE_NOTES.md

🎉 Release package created successfully!
📦 Package: releases/v1.2.0/POE2FilterInstaller-v1.2.0.zip
📊 Size: 15.2 MB
📁 Directory: releases/v1.2.0

🔧 Step 6: Git operations...
📝 Staging changes...
💾 Committing changes...
✅ Changes committed successfully
🏷️  Creating tag: v1.2.0
📤 Pushing tag to origin...
✅ Git operations completed successfully

🌐 Step 7: Creating GitHub release...
✅ GitHub release created: https://github.com/username/repo/releases/tag/v1.2.0
📤 Uploading release assets...
✅ Uploaded: POE2FilterInstaller-v1.2.0.zip
✅ Uploaded: POE2FilterInstaller-v1.2.0-package.tar.gz
✅ All assets uploaded successfully

🎉 Version update completed successfully!
📋 Next steps:
   1. Test installer on different systems
   2. Announce release to users
   3. Monitor download statistics
```

## 🎯 Tips

- **Token Security**: อย่าแชร์ token กับใคร
- **Regular Updates**: อัพเดท token ทุก 90 วัน
- **Scope Minimization**: เลือกเฉพาะ scopes ที่จำเป็น
- **Backup**: เก็บ token ไว้ในที่ปลอดภัย
- **Testing**: ทดสอบใน test repository ก่อน
