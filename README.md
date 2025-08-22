<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png">
    <img alt="Darkxee Poe2 Filter" src="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png" width="800" style="max-width: 100%">
  </picture>

  <h1 align="center">DZX Poe2 Filter</h1>
  
  <p>
    เป็นโปรเจคที่ทำขึ้นสำหรับกรอง Item จากเกม ซึ่งตอนนี้ poe2 ยังไม่รองรับ Function Import<br/>
    ดังนั้นจึงต้องใช้วิธีการรวมไฟล์โดยใช้ Python เข้ามาช่วย
  </p>

  <div class="badges">
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases">
      <img src="https://img.shields.io/github/v/release/darkzerox/Darkxee-Poe2Filter" alt="GitHub Release">
    </a>
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/actions">
      <img src="https://img.shields.io/github/actions/workflow/status/darkzerox/Darkxee-Poe2Filter/python-app.yml" alt="Build Status">
    </a>
  </div>
</div>

<h2 align="center">📥 ดาวน์โหลด</h2>

<div align="center">
  <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest">
    <img src="https://img.shields.io/badge/💻_Download-PC-blue?style=for-the-badge&logo=windows" alt="Download PC">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.pathofexile.com/account/view-profile/Darkxee-3892/item-filters">
    <img src="https://img.shields.io/badge/🎮_Download-PS5-blue?style=for-the-badge&logo=playstation" alt="Download PS5">
  </a>
</div>

<h2>🔧 วิธีติดตั้ง</h2>

<p>แตกไฟล์และคัดลอกไฟล์ทั้งหมดไปไว้ที่:</p>

  <summary>
    <img src="https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows" alt="Windows">
  </summary>
  <pre><code>%userprofile%\Documents\My Games\Path of Exile 2</code></pre>

  <summary>
    <img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux">
  </summary>
  <pre><code>steamapps/compatdata/2694490/pfx/drive_c/users/steamuser/My Documents/My Games/Path of Exile 2</code></pre>

<h2>👨‍💻 สำหรับนักพัฒนา</h2>

<p>สามารถ Clone โปรเจคไปแก้ไขได้เลย</p>

<h3>📂 โครงสร้างโปรเจค</h3>

<table>
  <tr>
    <th>โฟลเดอร์/ไฟล์</th>
    <th>รายละเอียด</th>
  </tr>
  <tr>
    <td>📁 <code>filter_group/</code></td>
    <td>ไฟล์ filter หลักแยกตามหมวดหมู่</td>
  </tr>
  <tr>
    <td>📁 <code>dzx_filter/soundeffect/type-01/</code></td>
    <td>ไฟล์เสียงทั้งหมด</td>
  </tr>
  <tr>
    <td>📄 <code>script/start_build.py</code></td>
    <td>สคริปต์สำหรับรวมไฟล์ filter</td>
  </tr>
</table>

<blockquote>
  <p>💡 Filter นี้จะมีการอัพเดตอย่างสม่ำเสมอ กรุณาติดตามการอัพเดตด้วยนะ</p>
</blockquote>

<h2>🙏 เครดิต</h2>

<div>
  <a href="https://github.com/NeverSinkDev/NeverSink-PoE2litefilter">
    <img src="https://img.shields.io/badge/Original_Filter-NeverSink's_Indepth_Loot_Filter-orange?style=for-the-badge" alt="NeverSink's Filter">
  </a>
</div>

<p>Style ต่างๆจะใช้ของต้นฉบับจาก NeverSink's เพื่อความสะดวกและคุ้นเคย อาจจะมีปรับปรุงเพิ่มเติมเล็กน้อย</p>

# POE2 Filter Installer

Installer อัตโนมัติสำหรับ Path of Exile 2 filters ที่มีการเช็ค version และอัพเดทจาก GitHub

## คุณสมบัติ

- ✅ ติดตั้ง filter files และ dzx_filter folder อัตโนมัติ
- ✅ เช็ค version ใหม่จาก GitHub
- ✅ อัพเดทอัตโนมัติเมื่อมี version ใหม่
- ✅ สร้าง backup ก่อนอัพเดท
- ✅ GUI ที่ใช้งานง่าย
- ✅ รองรับทั้ง Windows และ macOS
- ✅ Rollback ได้หากเกิดปัญหา

## การติดตั้ง

### วิธีที่ 1: ใช้ Executable (แนะนำ)

1. ดาวน์โหลดไฟล์ `POE2FilterInstaller.exe` จาก [Releases](https://github.com/your-username/dzx-filter-poe2/releases)
2. รันไฟล์ `install.bat` หรือ `POE2FilterInstaller.exe --gui`
3. เลือกโฟลเดอร์ Path of Exile 2
4. กดปุ่ม "ติดตั้ง" หรือ "อัพเดท"

### วิธีที่ 2: รันจาก Source Code

1. Clone repository:
```bash
git clone https://github.com/your-username/dzx-filter-poe2.git
cd dzx-filter-poe2
```

2. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

3. รัน installer:
```bash
# GUI mode
python run_installer.py --gui

# CLI mode
python run_installer.py
```

## การใช้งาน

### GUI Mode
- เปิดโปรแกรม installer
- เลือกโฟลเดอร์ Path of Exile 2
- กดปุ่ม "ตรวจสอบอัพเดท" เพื่อเช็ค version ใหม่
- กดปุ่ม "ติดตั้ง" เพื่อติดตั้ง filter ปัจจุบัน
- กดปุ่ม "อัพเดท" เพื่ออัพเดทเป็น version ใหม่

### CLI Mode
```bash
# ติดตั้ง filter ปัจจุบัน
python run_installer.py

# เปิด GUI
python run_installer.py --gui

# เช็คอัพเดท
python run_installer.py --check-updates
```

## โครงสร้างไฟล์

```
dzx-filter-poe2/
├── src/                          # Source code
│   ├── installer.py             # Main installer
│   ├── github_updater.py        # GitHub API updater
│   ├── filter_manager.py        # Filter management
│   └── gui.py                   # GUI interface
├── config/                       # Configuration
│   └── settings.json            # Installer settings
├── dzx_filter/                   # Filter assets
├── *.filter                      # Filter files
├── requirements.txt              # Python dependencies
├── build_installer.py           # Build script
└── run_installer.py             # Main runner
```

## การตั้งค่า

แก้ไขไฟล์ `config/settings.json`:

```json
{
  "github_repo": "your-username/dzx-filter-poe2",
  "current_version": "1.0.0",
  "auto_update": true,
  "backup_enabled": true,
  "backup_retention": 5
}
```

## การ Build

สร้าง executable file:

```bash
python build_installer.py
```

ไฟล์ installer จะอยู่ในโฟลเดอร์ `dist/POE2FilterInstaller/`

## การพัฒนา

### Dependencies
- Python 3.8+
- requests (สำหรับ GitHub API)
- PyInstaller (สำหรับ build executable)
- packaging (สำหรับ version comparison)

### การทดสอบ
```bash
# ทดสอบ installer
python -m pytest tests/

# ทดสอบการติดตั้ง
python test_installer.py
```

## การแก้ไขปัญหา

### ไม่สามารถเชื่อมต่อ GitHub ได้
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ตรวจสอบ firewall settings
- ลองใช้ VPN หากจำเป็น

### ไม่พบโฟลเดอร์ POE2
- ตรวจสอบว่าเกมติดตั้งแล้ว
- เลือกโฟลเดอร์ด้วยตนเอง
- สร้างโฟลเดอร์ใหม่หากจำเป็น

### ข้อผิดพลาดในการติดตั้ง
- ตรวจสอบสิทธิ์การเขียนไฟล์
- รันโปรแกรมเป็น Administrator (Windows)
- ตรวจสอบ log file: `installer.log`

## การสนับสนุน

หากพบปัญหา:
1. ตรวจสอบ log file
2. สร้าง issue บน GitHub
3. ตรวจสอบ [Wiki](https://github.com/your-username/dzx-filter-poe2/wiki)

## License

MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) file

## การมีส่วนร่วม

1. Fork repository
2. สร้าง feature branch
3. Commit changes
4. Push to branch
5. สร้าง Pull Request

## Changelog







### v1.0.16
- 🎯 Version update: 1.0.16
- 📅 Release date: 2025-08-22
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

### v1.0.15
- 🎯 Version update: 1.0.15
- 📅 Release date: 2025-08-22
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

### v1.0.14
- 🎯 Version update: 1.0.14
- 📅 Release date: 2025-08-22
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

### v1.0.14
- 🎯 Version update: 1.0.14
- 📅 Release date: 2025-08-22
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

### v1.0.13
- 🎯 Version update: 1.0.13
- 📅 Release date: 2025-08-22
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

### v1.1.1
- 🎯 Version update: 1.1.1
- 📅 Release date: 2025-08-22
- 🔧 Bug fixes and improvements
- 🚀 Performance optimizations

### v1.1.0
- ปรับปรุง installer ให้ติดตั้งเฉพาะไฟล์ที่จำเป็น
- ติดตั้งเฉพาะ dzx-poe2.filter และ dzx-poe2-*.filter
- ติดตั้งเฉพาะ /dzx_filter/soundeffect/**/**
- ปรับปรุง GUI ให้แสดง default paths และ browse ได้
- เพิ่มการ validate โฟลเดอร์ที่เลือก
- ลดขนาด package และเพิ่มความเร็วในการติดตั้ง

### v1.0.0
- Initial release
- Basic installer functionality
- GitHub update checker
- GUI interface
- Backup and rollback support
