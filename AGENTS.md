# POE2 Filter Installer - AGENTS.md

## Project Overview
POE2 Filter Installer เป็นโปรแกรมที่ช่วยติดตั้งและอัพเดท filter สำหรับ Path of Exile 2 โดยอัตโนมัติ

## Build and Test Commands
```bash
# Build installer
python build_installer.py

# Test installer
python test_installer.py

# Run installer
python poe2_filter_installer.py
```

## Code Style Guidelines
- ใช้ Python 3.8+
- ใช้ snake_case สำหรับชื่อตัวแปรและฟังก์ชัน
- ใช้ docstring สำหรับฟังก์ชัน
- ใช้ type hints
- ใช้ logging สำหรับ debug

## Testing Instructions
- ทดสอบการติดตั้ง filter ในโฟลเดอร์ที่ถูกต้อง
- ทดสอบการเช็ค version จาก GitHub
- ทดสอบการอัพเดทอัตโนมัติ
- ทดสอบการ rollback หากเกิดปัญหา

## Security Considerations
- ตรวจสอบ checksum ของไฟล์ที่ดาวน์โหลด
- ใช้ HTTPS สำหรับการเชื่อมต่อ GitHub API
- ตรวจสอบสิทธิ์การเขียนไฟล์ก่อนติดตั้ง
- สร้าง backup ก่อนอัพเดท

## Dependencies
- requests (สำหรับ GitHub API)
- tkinter (สำหรับ GUI)
- zipfile (สำหรับการจัดการไฟล์)
- hashlib (สำหรับ checksum)

## File Structure
```
poe2_filter_installer/
├── src/
│   ├── installer.py
│   ├── github_updater.py
│   ├── filter_manager.py
│   └── gui.py
├── config/
│   └── settings.json
├── tests/
│   └── test_installer.py
├── build/
│   └── dist/
└── requirements.txt
```
