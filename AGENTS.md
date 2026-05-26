# AGENTS.md - DZX Filter POE2

> **For AI Agents**: อ่านไฟล์นี้ก่อนทำงานทุกครั้ง  
> ไฟล์นี้รวบรวมข้อมูลทั้งหมดที่ agent จำเป็นต้องรู้เพื่อทำงานกับโปรเจกต์นี้ได้อย่างถูกต้อง

---

## 🗺️ Project Overview

**DZX Filter POE2** คือ Item Filter สำหรับเกม Path of Exile 2 พัฒนาโดย **Darkxee**

- **GitHub**: https://github.com/darkzerox/Darkxee-Poe2Filter
- **Website**: https://darkzerox.github.io/Darkxee-Poe2Filter/
- **Current Version**: ดูใน `config.json` → `project.version`
- **License**: MIT

### สิ่งที่โปรเจกต์นี้ทำ

1. **Filter Files** (`.filter`) — กฎการแสดง/ซ่อน item ในเกม ผ่าน DSL ของ PoE2
2. **Build System** (Python) — แปลง filter group ย่อยๆ ให้กลายเป็น `.filter` ไฟล์สมบูรณ์
3. **Launcher GUI** (Python + Tkinter → `.exe`) — ตัวติดตั้งที่ผู้ใช้ download ไปรัน มี auto-updater ดึง filter ใหม่อัตโนมัติจาก GitHub Releases
4. **Website** (HTML/CSS) — หน้าเว็บโปรเจกต์

---

## 📁 Project Structure (ที่สำคัญ)

```
Darkxee-Poe2Filter/
├── AGENTS.md                  ← ไฟล์นี้ (อ่านก่อนทุกครั้ง)
├── CLAUDE.md                  ← Quick reference commands
├── config.json                ← ⭐ Version, filter groups, build config ทั้งหมด
├── requirements.txt           ← Python dependencies
│
├── script/
│   ├── start_build.py         ← 🏗️ Main build entry point
│   ├── merge_file.py          ← รวม filter group files
│   ├── build_css.py           ← Build CSS สำหรับ website
│   ├── build_html.py          ← Build HTML website
│   ├── create_release.py      ← 🚀 Local release automation (GitHub)
│   └── installer_gui.py       ← 🖥️ Launcher GUI + Auto-updater source
│
├── dzx_filter/
│   ├── filter_group/          ← ⭐ Filter source files (แยกเป็นหมวดหมู่)
│   │   ├── currency.filter
│   │   ├── rarity_unique.filter
│   │   ├── rarity_rare.filter
│   │   ├── rarity_magic.filter
│   │   ├── gacha.filter
│   │   ├── gold.filter
│   │   ├── uncut_gems.filter
│   │   ├── crafting.filter
│   │   ├── amulets.filter
│   │   ├── belts.filter
│   │   ├── rings.filter / ring.filter
│   │   ├── jewel.filter
│   │   ├── key.filter
│   │   ├── relics.filter
│   │   ├── rune.filter
│   │   ├── talisman.filter
│   │   ├── soul_core.filter
│   │   ├── waystones.filter
│   │   ├── flasks.filter
│   │   ├── charms.filter
│   │   ├── salvage.filter
│   │   ├── scroll_of_wisdom.filter
│   │   ├── olroths_legacy.filter
│   │   ├── mirror_tier.filter
│   │   ├── map_breach.filter
│   │   ├── map_temple.filter
│   │   └── sounds/            ← sound effect files
│   ├── css/                   ← Website CSS
│   ├── images/                ← Images (logo, etc.) — bundled into EXE
│   └── soundeffect/           ← Sound type sets
│
├── dist/
│   ├── filter/                ← ⭐ Output compiled .filter files (ห้าม edit ตรงๆ)
│   └── DZX-PoE2-Filter-Launcher.exe ← Compiled launcher
│
├── .planning/
│   └── agent_memory.md        ← 🧠 Technical decisions & session history
│
└── dzx-poe2-filter.zip        ← Release ZIP (auto-generated)
```

---

## ⚙️ config.json — หัวใจของโปรเจกต์

`config.json` ควบคุมทุกอย่าง ต้องอัปเดตก่อน release:

| Field | ความหมาย |
|---|---|
| `project.version` | Version สำหรับ release (e.g. `"0.5.3"`) |
| `filter_variants` | รายการ filter ที่จะสร้าง (name, group, platform) |
| `filter_groups` | กลุ่ม filter files ที่แต่ละ variant ใช้ |
| `special_variants` | Variant พิเศษ เช่น Divine-Mirror |

### Filter Variants ที่มีอยู่

| Variant | กลุ่ม | Platform |
|---|---|---|
| `dzx-poe2` | MAIN_GROUP | PC |
| `dzx-poe2-breach` | BREACH_GROUP | PC, PS5 |
| `dzx-poe2-PS5` | MAIN_GROUP | PS5 |
| `dzx-poe2-temple` | TEMPLE_GROUP | PC, PS5 |
| `dzx-poe2-Divine-Mirror` | Special (currency+unique+gacha+key+waystones) | - |

---

## 🔧 Build Commands

### สร้าง Filter ทั้งหมด
```bash
python -X utf8 script/start_build.py
```
> ผลลัพธ์อยู่ใน `dist/filter/`

### Build แยกส่วน
```bash
python script/build_css.py    # CSS สำหรับ website
python script/build_html.py   # HTML website
python script/merge_file.py   # รวม filter files
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Release Process (สำคัญมาก)

**ทุก release ทำบนเครื่อง local เท่านั้น** ไม่มี CI/CD build บน GitHub

### ขั้นตอน

1. **อัปเดตเวอร์ชัน** ใน `config.json` → `project.version`
2. **ปิด Launcher** ถ้ากำลังรันอยู่ (มิฉะนั้น PyInstaller จะ error)
3. **รัน release script**:
   ```bash
   python -X utf8 script/create_release.py
   ```

### สิ่งที่ `create_release.py` ทำ (ตามลำดับ)

1. อ่านเวอร์ชันจาก `config.json`
2. ถามยืนยันก่อน release
3. ตรวจสอบ `gh` CLI authentication
4. รัน `start_build.py` เพื่อ compile filter
5. สร้าง `dzx-poe2-filter.zip` จาก `dist/filter/`
6. Compile `DZX-PoE2-Filter-Launcher.exe` ด้วย PyInstaller
7. สร้าง git tags (`vX.Y.Z` และ `X.Y.Z`)
8. Push branches (`master`, `develop`) + tags ไป GitHub
9. สร้าง GitHub Release พร้อมแนบ `.zip` และ `.exe`

### PyInstaller Command (ที่ใช้ใน create_release.py)
```bash
python -m PyInstaller \
  --onefile \
  --noconsole \
  --name DZX-PoE2-Filter-Launcher \
  --add-data "dist/filter;filters" \
  --add-data "dzx_filter/images;dzx_filter/images" \
  --add-data "config.json;." \
  script/installer_gui.py
```

> ⚠️ **สำคัญ**: `--add-data "config.json;."` ต้องมีเสมอ เพราะ GUI อ่าน version จาก config.json ที่ bundled ไว้ใน EXE

---

## 🖥️ Launcher GUI (`script/installer_gui.py`)

### Class: `FilterInstallerGUI`

| Feature | รายละเอียด |
|---|---|
| Framework | Python Tkinter |
| Window size | 540×510 px |
| Background color | `#0f0f0f` (dark) |
| DPI Awareness | Set via `ctypes.windll.shcore.SetProcessDpiAwareness(1)` |

### Resource Path Detection
```python
if getattr(sys, 'frozen', False):
    self.base_path = Path(sys._MEIPASS)  # เมื่อรันเป็น EXE
else:
    self.base_path = Path(__file__).parent.parent  # dev mode
```

### Auto-Updater Logic
- **Thread**: ใช้ background daemon thread เพื่อไม่ block GUI
- **GitHub API**: `https://api.github.com/repos/darkzerox/Darkxee-Poe2Filter/releases/latest`
- **Version Comparison**: ตัดคำว่า `v` ออกก่อน compare (e.g. `"v0.5.3"` → `"0.5.3"`)
- **Version Files**:
  - `config.json` (bundled) → version ของ EXE ที่ download มา
  - `.installed_version` (in game folder) → version ของ filter ที่ install ไว้
- **Download**: ดึง `dzx-poe2-filter.zip` ลงใน memory (`io.BytesIO`) แล้ว extract ทันที

### สิ่งที่ installer ทำ
1. ตรวจสอบ filter ที่ติดตั้งอยู่ในโฟลเดอร์เกม
2. ดึงข้อมูล latest release จาก GitHub API
3. เปรียบเทียบ version — ถ้ามี update ให้ดาวน์โหลดใหม่อัตโนมัติ
4. ติดตั้ง filter ไปยัง `Documents\My Games\Path of Exile 2`
5. บันทึก `.installed_version` ไว้ใน game folder

---

## ⚠️ Known Issues & Gotchas

### 1. `PermissionError: [WinError 5] Access is denied` ตอน Build EXE
- **สาเหตุ**: Launcher กำลังรันอยู่ทำให้ PyInstaller ไม่สามารถ overwrite `.exe` ได้
- **วิธีแก้**:
  ```powershell
  taskkill /F /IM DZX-PoE2-Filter-Launcher.exe
  ```

### 2. Version String Mismatch
- GitHub tags มีทั้ง `v0.5.3` และ `0.5.3`
- ใน code ต้อง strip `v` ออกก่อน compare เสมอ
- ใน `installer_gui.py`: ตรวจสอบที่ `self.latest_tag.lstrip('v')`

### 3. Logo/Image Sizing บน High-DPI
- Logo ใน GUI ถูก subsample เป็น `300×113` px
- Logo frame height: `140`, window height: `510`
- ถ้าโลโก้หาย = `base_path` ผิด หรือ `--add-data` ไม่ได้ map path ถูกต้อง

### 4. Filter Path บน PS5
- PoE2 บน PS5 ไม่มีระบบ filter file เหมือน PC
- Variant `dzx-poe2-PS5` มีอยู่แต่เป็น reference สำหรับ manual use

### 5. ไฟล์ใน `dist/` ห้าม commit ลง git
- `.gitignore` ควร exclude `dist/` และ `build/`
- ผลลัพธ์ build อัปโหลดผ่าน GitHub Releases เท่านั้น

---

## 📦 Dependencies

### Python (`requirements.txt`)
```
pyinstaller    # สำหรับ compile EXE
pillow         # สำหรับ image handling ใน Tkinter GUI
requests       # (optional) ถ้าใช้ requests แทน urllib
```

### Tools ที่ต้องติดตั้งบนเครื่อง
- **Python 3.x** (3.9+ แนะนำ)
- **GitHub CLI** (`gh`) — ต้อง authenticate ก่อน: `gh auth login`
- **Git**

---

## 🔁 Git Workflow

- **`master`** → production branch (release จากนี้)
- **`develop`** → development branch
- **Tags**: `vX.Y.Z` และ `X.Y.Z` (สองแบบทั้งคู่)
- ใช้ `semantic versioning`: `MAJOR.MINOR.PATCH`

### Branch เมื่อทำ feature ใหม่
```bash
git checkout develop
git checkout -b feature/feature-name
# ... ทำงาน ...
git checkout develop
git merge feature/feature-name
```

---

## 🧠 Agent Memory & Session History

ดูข้อมูลเพิ่มเติมและ decision log ที่: `.planning/agent_memory.md`

### Key Decisions (สรุป)

| Decision | เหตุผล |
|---|---|
| Build local เท่านั้น | ไม่มี GitHub Actions CI/CD — ทุกอย่าง build จาก local machine |
| `urllib` แทน `requests` | ลดขนาด EXE และ dependency ที่ต้อง bundle |
| Background thread สำหรับ update check | ป้องกัน GUI freeze / Windows "Not Responding" |
| Bundle `config.json` ใน EXE | GUI ต้องอ่าน version ได้เมื่อรันเป็น standalone EXE |
| `.installed_version` file | Track version ที่ install จริงๆ แยกจาก version ของ EXE |

---

## 🗂️ Filter File Format (PoE2 DSL)

ตัวอย่างโครงสร้าง `.filter` file:

```filter
# Show unique items
Show
    Rarity Unique
    SetBorderColor 255 165 0 255
    SetTextColor 255 165 0 255
    PlayAlertSound 1 300

# Hide normal items
Hide
    Rarity Normal
    ItemLevel <= 60
```

### คำสั่งที่ใช้บ่อย
- `Show` / `Hide` — แสดง/ซ่อน item
- `Rarity Normal | Magic | Rare | Unique`
- `ItemLevel >= N`
- `BaseType "Name"`
- `Class "Name"`
- `SetBorderColor R G B [A]`
- `SetTextColor R G B [A]`
- `SetBackgroundColor R G B [A]`
- `PlayAlertSound N Volume`
- `MinimapIcon Size Color Shape`
- `PlayEffect Color [Temp]`

---

## 📋 Release Checklist

ก่อน release ทุกครั้ง:

- [ ] อัปเดต version ใน `config.json` → `project.version`
- [ ] ทดสอบ filter ในเกมว่าทำงานถูกต้อง
- [ ] ปิด Launcher EXE ถ้ากำลังรันอยู่
- [ ] รัน `python -X utf8 script/create_release.py`
- [ ] ตรวจสอบ GitHub Release ว่าไฟล์ ZIP และ EXE แนบครบ

---

*อัปเดตล่าสุด: 2026-05-26 | Version: 0.5.3*
