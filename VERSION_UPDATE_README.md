# 🚀 POE2 Filter Installer - Version Update & Cleanup System

ระบบอัพเดท version และ cleanup releases เก่าอัตโนมัติสำหรับ POE2 Filter Installer

## 📋 คุณสมบัติ

- ✅ **อัพเดท Version อัตโนมัติ** ในทุกไฟล์ที่เกี่ยวข้อง
- ✅ **สร้าง Release Package** พร้อม installer และ zip file
- ✅ **Cleanup Releases เก่า** อัตโนมัติหลังสร้าง release ใหม่
- ✅ **Git Operations** อัตโนมัติ (commit, tag, push)
- ✅ **GitHub Release** อัตโนมัติ (ถ้ามี GITHUB_TOKEN)
- ✅ **Changelog Update** ใน README.md

## 🛠️ การติดตั้ง

### 1. ตรวจสอบ Prerequisites
```bash
# ตรวจสอบว่ามีไฟล์ที่จำเป็นครบ
ls -la update_version.py auto_cleanup.py config/settings.json
```

### 2. ตั้งค่า GitHub Token (ถ้าต้องการ)
```bash
export GITHUB_TOKEN=your_github_token_here
```

## 🚀 การใช้งาน

### **วิธีที่ 1: ใช้ Quick Update Script (แนะนำ)**

```bash
# อัพเดทเป็น version 1.2.0 (เก็บ 1 release ล่าสุด)
python quick_update.py 1.2.0

# อัพเดทเป็น version 1.2.0 (เก็บ 2 releases ล่าสุด)
python quick_update.py 1.2.0 --keep 2

# อัพเดทแบบอัตโนมัติ (ไม่ถามยืนยัน)
python quick_update.py 1.2.0 --auto

# อัพเดทโดยไม่ cleanup releases เก่า
python quick_update.py 1.2.0 --no-cleanup

# ดู help
python quick_update.py --help
```

### **วิธีที่ 2: ใช้ Update Version Script โดยตรง**

```bash
# อัพเดทเป็น version 1.2.0
python update_version.py 1.2.0

# อัพเดทเป็น version 1.2.0 (เก็บ 2 releases ล่าสุด)
python update_version.py 1.2.0 --keep-releases 2

# อัพเดทแบบอัตโนมัติ
python update_version.py 1.2.0 --auto

# อัพเดทโดยไม่ cleanup
python update_version.py 1.2.0 --no-cleanup
```

### **วิธีที่ 3: ใช้ Cleanup Script แยก**

```bash
# ลบ releases เก่า เหลือ 1 รายการล่าสุด
python auto_cleanup.py --auto

# เก็บ releases 2 รายการล่าสุด
python auto_cleanup.py --keep 2 --auto

# ทดสอบโดยไม่ลบจริง
python auto_cleanup.py --dry-run
```

## 📁 โครงสร้างไฟล์

```
dzx-filter-poe2/
├── update_version.py          # Script หลักสำหรับ update version
├── auto_cleanup.py            # Script สำหรับ cleanup releases เก่า
├── quick_update.py            # Wrapper script ใช้งานง่าย
├── cleanup_old_releases.py    # Script แบบ interactive
├── .gitattributes             # ตั้งค่า export-ignore
└── releases/                  # Folder สำหรับ releases
    ├── v1.0.13/              # Release เก่า (จะถูกลบ)
    └── v1.1.1/               # Release ล่าสุด (จะเก็บไว้)
```

## 🔄 ขั้นตอนการทำงาน

### **เมื่อรัน `python quick_update.py 1.2.0`:**

1. **📝 Update Version Files** - อัพเดท version ใน config และ source files
2. **📚 Update Changelog** - เพิ่ม changelog entry ใน README.md
3. **🔍 Verify Consistency** - ตรวจสอบ version consistency
4. **🔨 Build Installer** - สร้าง installer package
5. **📦 Create Release Package** - สร้าง release folder และ zip file
6. **🔧 Git Operations** - commit, tag, push
7. **🌐 GitHub Release** - สร้าง GitHub release (ถ้ามี token)
8. **🧹 Cleanup Old Releases** - ลบ releases เก่า เหลือเฉพาะล่าสุด

## ⚙️ การตั้งค่า

### **GitHub Release**
```bash
# ตั้งค่า GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# หรือเพิ่มใน .bashrc/.zshrc
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc
```

### **Cleanup Settings**
```bash
# เก็บ releases 1 รายการล่าสุด (default)
python quick_update.py 1.2.0

# เก็บ releases 3 รายการล่าสุด
python quick_update.py 1.2.0 --keep 3

# ไม่ cleanup releases เก่า
python quick_update.py 1.2.0 --no-cleanup
```

## 🎯 Use Cases

### **สำหรับ Developer:**
```bash
# อัพเดท version และ cleanup อัตโนมัติ
python quick_update.py 1.2.0 --auto
```

### **สำหรับ CI/CD Pipeline:**
```bash
# อัพเดทแบบอัตโนมัติใน CI/CD
python quick_update.py $NEW_VERSION --auto --keep 2
```

### **สำหรับ Manual Update:**
```bash
# อัพเดทแบบ interactive
python quick_update.py 1.2.0
```

## 🔧 การแก้ไขปัญหา

### **Error: "Missing required files"**
```bash
# ตรวจสอบว่าอยู่ใน directory ที่ถูกต้อง
pwd
ls -la update_version.py auto_cleanup.py
```

### **Error: "GitHub release creation failed"**
```bash
# ตรวจสอบ GitHub token
echo $GITHUB_TOKEN

# ตั้งค่า token ใหม่
export GITHUB_TOKEN=your_new_token
```

### **Error: "Cleanup failed"**
```bash
# ทดสอบ cleanup แยก
python auto_cleanup.py --dry-run

# ตรวจสอบ permissions
ls -la releases/
```

## 📊 ผลลัพธ์

### **หลังจากการ update version 1.2.0:**

```
releases/
└── v1.2.0/                           # Release ใหม่
    ├── POE2FilterInstaller_Package/   # Installer package
    ├── POE2FilterInstaller-v1.2.0.zip # Zip file
    └── RELEASE_NOTES.md               # Release notes

# releases เก่าจะถูกลบทิ้ง (ถ้าไม่ใช้ --no-cleanup)
```

### **Git Operations:**
- ✅ Commit changes
- ✅ Create tag v1.2.0
- ✅ Push to origin
- ✅ GitHub release (ถ้ามี token)

## 🚨 คำเตือน

- ⚠️ **Backup ก่อนใช้งาน** - ตรวจสอบ git status ก่อนรัน
- ⚠️ **Cleanup จะลบ releases เก่าทิ้ง** - ใช้ `--no-cleanup` ถ้าไม่ต้องการ
- ⚠️ **GitHub token** - ต้องมีสิทธิ์ในการสร้าง release
- ⚠️ **Version format** - ต้องเป็นรูปแบบ X.Y.Z (เช่น 1.2.0)

## 📞 การสนับสนุน

หากพบปัญหา:
1. ตรวจสอบ error messages
2. ใช้ `--dry-run` เพื่อทดสอบ
3. ตรวจสอบ prerequisites
4. ดู logs และ git status

---

**🎉 Happy Version Updating!** 🚀
