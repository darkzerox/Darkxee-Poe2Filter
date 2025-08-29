<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png">
    <img alt="Darkxee Poe2 Filter" src="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png" width="800" style="max-width: 100%">
  </picture>

  <h1 align="center">DZX Poe2 Filter</h1>
  
  <p align="center">
    <strong>🎯 Advanced Item Filter for Path of Exile 2</strong><br/>
    เป็น Item Filter ที่พัฒนาขึ้นสำหรับ Path of Exile 2 โดยเฉพาะ<br/>
    รองรับการรวมไฟล์อัตโนมัติด้วย Python เนื่องจาก PoE2 ยังไม่รองรับ Import Function
  </p>

  <div class="badges">
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases">
      <img src="https://img.shields.io/github/v/release/darkzerox/Darkxee-Poe2Filter" alt="GitHub Release">
    </a>
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/actions">
      <img src="https://img.shields.io/github/actions/workflow/status/darkzerox/Darkxee-Poe2Filter/python-app.yml" alt="Build Status">
    </a>
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/darkzerox/Darkxee-Poe2Filter" alt="License">
    </a>
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/stargazers">
      <img src="https://img.shields.io/github/stars/darkzerox/Darkxee-Poe2Filter" alt="GitHub Stars">
    </a>
  </div>
</div>

## ✨ Features | คุณสมบัติ

- 🎮 **รองรับหลายแพลตฟอร์ม**: PC และ PS5
- 🔊 **เสียงแจ้งเตือน**: เสียงพิเศษสำหรับไอเทมสำคัญ
- 🎨 **หลายโหมด**: Normal, No-Hide, Color-Only, Breach และอื่นๆ
- 🛠️ **ปรับแต่งได้**: แยกไฟล์ตามหมวดหมู่ เพื่อการแก้ไขที่ง่าย
- 🔄 **อัพเดตสม่ำเสมอ**: ติดตามการเปลี่ยนแปลงของเกมอย่างต่อเนื่อง
- 🌐 **Web Preview**: สามารถดูตัวอย่าง Filter ในรูปแบบ HTML ได้

## 📋 Table of Contents | สารบัญ

- [Download | ดาวน์โหลด](#-download--ดาวน์โหลด)
- [Installation | การติดตั้ง](#-installation--การติดตั้ง)
- [Filter Variants | รูปแบบ Filter](#-filter-variants--รูปแบบ-filter)
- [Developer Guide | คู่มือนักพัฒนา](#-developer-guide--คู่มือนักพัฒนา)
- [Contributing | การมีส่วนร่วม](#-contributing--การมีส่วนร่วม)
- [Credits | เครดิต](#-credits--เครดิต)

## 📥 Download | ดาวน์โหลด

<div align="center">
  <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest">
    <img src="https://img.shields.io/badge/💻_Download_for-PC-blue?style=for-the-badge&logo=windows" alt="Download PC">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.pathofexile.com/account/view-profile/Darkxee-3892/item-filters">
    <img src="https://img.shields.io/badge/🎮_Download_for-PS5-blue?style=for-the-badge&logo=playstation" alt="Download PS5">
  </a>
</div>

## 🔧 Installation | การติดตั้ง

### วิธีติดตั้งแบบง่าย (Easy Installation)

1. **ดาวน์โหลดไฟล์**: ไปที่ [Releases Page](https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest) และดาวน์โหลดเวอร์ชันล่าสุด
2. **แตกไฟล์**: แตกไฟล์ zip ที่ดาวน์โหลดมา  
3. **คัดลอกไฟล์**: คัดลอกไฟล์ทั้งหมดไปยังโฟลเดอร์เกมตามแพลตฟอร์มของคุณ

### 📍 Installation Paths | เส้นทางการติดตั้ง

<details>
<summary>
  <img src="https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows" alt="Windows"> <strong>Windows</strong>
</summary>

```
%userprofile%\Documents\My Games\Path of Exile 2
```

**หรือเส้นทางเต็ม:**
```
C:\Users\[ชื่อผู้ใช้]\Documents\My Games\Path of Exile 2
```
</details>

<details>
<summary>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux"> <strong>Linux (Steam Proton)</strong>
</summary>

```
~/.steam/steam/steamapps/compatdata/2694490/pfx/drive_c/users/steamuser/My Documents/My Games/Path of Exile 2
```

**หรือสำหรับ Steam Flatpak:**
```
~/.var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/compatdata/2694490/pfx/drive_c/users/steamuser/My Documents/My Games/Path of Exile 2
```
</details>

<details>
<summary>
  <img src="https://img.shields.io/badge/PlayStation-003791?style=flat&logo=playstation" alt="PlayStation"> <strong>PlayStation 5</strong>
</summary>

สำหรับ PS5 ให้ใช้ลิงก์ดาวน์โหลดด้านบนเพื่อนำเข้าผ่าน Path of Exile Website
</details>

### 🎯 การเลือก Filter

หลังจากติดตั้งแล้ว ในเกมให้ไปที่:
1. **Settings** → **Game** → **Item Filter**
2. เลือก Filter ที่ต้องการจากรายการ (ดูรายละเอียดใน [Filter Variants](#-filter-variants--รูปแบบ-filter))

## 🎨 Filter Variants | รูปแบบ Filter

เรามี Filter หลายรูปแบบให้เลือกใช้ตามความต้องการ:

| Filter Name | Description | แนะนำสำหรับ |
|-------------|-------------|-------------|
| `dzx-poe2.filter` | **🌟 Main Filter** - Filter หลักที่แนะนำ | ผู้เล่นทั่วไป |
| `dzx-poe2-no-hide.filter` | **👁️ No Hide** - ไม่ซ่อนไอเทมใดๆ | ผู้เล่นใหม่, การทดสอบ |
| `dzx-poe2-Color-Only.filter` | **🎨 Color Only** - แสดงสีเฉพาะ | ผู้เล่นที่ไม่ชอบเสียง |
| `dzx-poe2-breach.filter` | **⚔️ Breach Mode** - สำหรับ Breach | การเล่น Breach League |
| `dzx-poe2-Divine-Mirror.filter` | **💎 Divine & Mirror** - เน้นไอเทมหายาก | การฟาร์มไอเทมหายาก |
| `dzx-poe2-PS5.filter` | **🎮 PS5 Version** - เวอร์ชัน PS5 | ผู้เล่น PlayStation 5 |

> 💡 **คำแนะนำ**: หากเป็นครั้งแรกแนะนำให้ใช้ `dzx-poe2-no-hide.filter` เพื่อเรียนรู้ไอเทมต่างๆ แล้วค่อยเปลี่ยนไปใช้ `dzx-poe2.filter`

## 👨‍💻 Developer Guide | คู่มือนักพัฒนา

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/darkzerox/Darkxee-Poe2Filter.git
cd Darkxee-Poe2Filter

# Build filters
cd script
python start_build.py

# Preview in browser (optional)
# เปิดไฟล์ index.html ในเบราว์เซอร์
```

### 📋 Prerequisites

- **Python 3.6+** (สำหรับ build script)
- **Text Editor** สำหรับแก้ไข filter files

### 📂 Project Structure | โครงสร้างโปรเจค

```
dzx-filter-poe2/
├── 📁 dzx_filter/              # ไฟล์ Filter และ Assets
│   ├── soundeffect/type-01/    # ไฟล์เสียงทั้งหมด (.mp3)
│   ├── fonts/                  # Font files (.ttf)
│   └── images/                 # รูปภาพและโลโก้
├── 📁 script/                  # Build Scripts
│   ├── start_build.py         # สคริปต์หลักสำหรับ build
│   ├── merge_file.py          # รวมไฟล์ filter
│   ├── build_css.py           # สร้าง CSS preview
│   └── build_html.py          # สร้าง HTML preview
├── 📄 dzx-poe2*.filter        # Filter files ที่ build แล้ว
└── 📄 index.html              # Web preview
```

### 🛠️ Build Scripts | สคริปต์สำหรับ Build

| Script | Function | Usage |
|--------|----------|--------|
| `start_build.py` | **Main Build** - รวมไฟล์และสร้าง filter ทั้งหมด | `python start_build.py` |
| `merge_file.py` | **File Merger** - รวมไฟล์ filter modules | Import by other scripts |
| `build_css.py` | **CSS Generator** - สร้าง CSS สำหรับ preview | Import by main script |
| `build_html.py` | **HTML Generator** - สร้างหน้า preview | Import by main script |

### 🔄 Development Workflow

1. **แก้ไข Filter**: แก้ไขไฟล์ในโฟลเดอร์ `dzx_filter/`
2. **Build Filter**: รัน `python script/start_build.py`
3. **ทดสอบ**: คัดลอก filter ไฟล์ไปยังโฟลเดอร์เกม
4. **Preview**: เปิด `index.html` เพื่อดู preview

## 🤝 Contributing | การมีส่วนร่วม

เรายินดีรับการมีส่วนร่วมจากทุกคน! 

### วิธีการมีส่วนร่วม:

1. **🍴 Fork** โปรเจคนี้
2. **🌿 Create Branch**: `git checkout -b feature/amazing-feature`
3. **✨ Make Changes**: แก้ไขหรือเพิ่มฟีเจอร์
4. **🔨 Build & Test**: รัน build script และทดสอบ
5. **📝 Commit**: `git commit -m 'Add amazing feature'`
6. **📤 Push**: `git push origin feature/amazing-feature`
7. **🔄 Pull Request**: สร้าง Pull Request

### 📋 Guidelines

- ใช้ชื่อ branch ที่สื่อความหมาย
- Test filter ก่อนส่ง PR
- เขียน commit message ที่ชัดเจน
- อัพเดต README หากมีการเปลี่ยนแปลงใหญ่

## 🐛 Issues & Support | การรายงานปัญหา

หากพบปัญหาหรือมีข้อเสนอแนะ:

- **🐛 Bug Reports**: [Create Issue](https://github.com/darkzerox/Darkxee-Poe2Filter/issues/new?template=bug_report.md)
- **💡 Feature Requests**: [Create Issue](https://github.com/darkzerox/Darkxee-Poe2Filter/issues/new?template=feature_request.md)
- **❓ Questions**: [Discussions](https://github.com/darkzerox/Darkxee-Poe2Filter/discussions)

> 💡 **หมายเหตุ**: Filter นี้จะมีการอัพเดตอย่างสม่ำเสมอ กรุณาติดตามการอัพเดตและ Star โปรเจคเพื่อรับการแจ้งเตือน

## 🙏 Credits | เครดิต

<div align="center">
  <a href="https://github.com/NeverSinkDev/NeverSink-PoE2litefilter">
    <img src="https://img.shields.io/badge/Inspired_by-NeverSink's_PoE2_Filter-orange?style=for-the-badge&logo=github" alt="NeverSink's Filter">
  </a>
</div>

**พิเศษขอบคุณ:**
- **[NeverSink](https://github.com/NeverSinkDev)** - สำหรับ Original Filter Style และแนวคิด
- **Path of Exile 2 Community** - สำหรับ feedback และการทดสอบ
- **Contributors** - ทุกคนที่มีส่วนร่วมในการพัฒนา

> 🎨 Style ต่างๆ จะใช้ของต้นฉบับจาก NeverSink's เพื่อความสะดวกและคุ้นเคย พร้อมปรับปรุงเพิ่มเติมให้เหมาะสมกับ Path of Exile 2

---

<div align="center">
  <p><strong>🌟 หากชอบโปรเจคนี้ อย่าลืม Star ให้กำลังใจด้วยนะ! 🌟</strong></p>
  
  <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/stargazers">
    <img src="https://img.shields.io/github/stars/darkzerox/Darkxee-Poe2Filter?style=social" alt="GitHub Stars">
  </a>
  
  <p><sub>Made with ❤️ by <a href="https://github.com/darkzerox">Darkxee</a> for the Path of Exile 2 Community</sub></p>
</div>
