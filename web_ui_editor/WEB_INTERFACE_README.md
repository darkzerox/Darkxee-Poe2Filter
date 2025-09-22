# DZX Filter Editor - Web Interface

## ภาพรวม
DZX Filter Editor เป็น Web Interface ที่ช่วยให้ผู้ใช้สามารถปรับปรุง filter สำหรับ Path of Exile 2 ได้อย่างง่ายดายผ่าน browser โดยไม่ต้องแก้ไขไฟล์โดยตรง

## คุณสมบัติหลัก

### 🎯 Import/Export Filter
- **Import**: นำเข้าไฟล์ .filter, .json, .yaml
- **Export**: ส่งออกเป็นไฟล์ .filter สำหรับใช้ในเกม
- **Validation**: ตรวจสอบความถูกต้องของไฟล์ที่นำเข้า
- **Backup**: สร้างและกู้คืน backup

### 🎨 Visual Editor
- **Color Picker**: เลือกสีสำหรับ text, border, background
- **Font Size**: ปรับขนาดฟอนต์
- **Sound Preview**: ทดสอบเสียงก่อนใช้งาน
- **Icon Customization**: ปรับแต่ง minimap icon

### 📋 Rule Management
- **Add/Edit/Delete**: จัดการ filter rules
- **Duplicate**: คัดลอก rules
- **Search & Filter**: ค้นหาและกรอง rules
- **Drag & Drop**: จัดเรียง rules (coming soon)

### 👁️ Realtime Preview
- **Live Preview**: แสดงตัวอย่างทันทีเมื่อมีการเปลี่ยนแปลง
- **Sound Testing**: ทดสอบเสียงโดยคลิกที่ไอเทม
- **Visual Effects**: แสดงผล effects ตามที่กำหนด
- **Sample Items**: ไอเทมตัวอย่างสำหรับทดสอบ

### 🗂️ Category Management
- **Currency**: สกุลเงินต่างๆ
- **Equipment**: อุปกรณ์และอาวุธ
- **Jewels**: Jewel ทุกประเภท
- **Maps**: Maps และพื้นที่ต่างๆ
- **Special Items**: ไอเทมพิเศษ

## การติดตั้งและใช้งาน

### 1. เปิด Web Interface
```
เปิดไฟล์ filter-editor.html ใน browser
```

### 2. Import Filter ที่มีอยู่
1. คลิกปุ่ม "Import Filter"
2. เลือกไฟล์ .filter ที่ต้องการแก้ไข
3. ระบบจะ parse และแสดง rules ทั้งหมด

### 3. แก้ไข Rules
1. เลือก category และ section ที่ต้องการ
2. คลิกที่ rule ที่ต้องการแก้ไข
3. ปรับแต่งสี, เสียง, icon ใน Properties Panel
4. ดูผลลัพธ์ใน Realtime Preview

### 4. Export Filter
1. คลิกปุ่ม "Export Filter"
2. ไฟล์ .filter จะถูกดาวน์โหลดอัตโนมัติ
3. นำไฟล์ไปใช้ในเกม

## โครงสร้างไฟล์

```
dzx-filter-poe2/
├── filter-editor.html          # หน้าเว็บหลัก
├── css/
│   └── filter-editor.css       # CSS สำหรับ editor
├── js/
│   ├── filter-editor.js        # JavaScript หลัก
│   ├── filter-parser.js        # Parser สำหรับ filter files
│   ├── realtime-preview.js     # ระบบ preview แบบ realtime
│   └── import-export.js        # จัดการ import/export
└── script/
    └── filter_parser.py        # Python parser (backend)
```

## API Reference

### FilterEditor Class
```javascript
const editor = new FilterEditor();

// Methods
editor.importFilter()           // นำเข้า filter
editor.exportFilter()          // ส่งออก filter
editor.addRule()               // เพิ่ม rule ใหม่
editor.deleteRule()            // ลบ rule
editor.refreshPreview()        // รีเฟรช preview
```

### ImportExportManager Class
```javascript
const manager = new ImportExportManager(editor);

// Methods
await manager.importFile(file)     // นำเข้าไฟล์
await manager.exportFile(format, data)  // ส่งออกไฟล์
manager.createBackup()            // สร้าง backup
await manager.restoreFromBackup(file)  // กู้คืน backup
```

### RealtimePreview Class
```javascript
const preview = new RealtimePreview(editor);

// Methods
preview.updatePreview()           // อัปเดต preview
preview.playSound(sound)          // เล่นเสียง
preview.testAllSounds()           // ทดสอบเสียงทั้งหมด
preview.getPreviewStats()         // ดูสถิติ preview
```

## ตัวอย่างการใช้งาน

### การสร้าง Rule ใหม่
```javascript
// เพิ่ม rule สำหรับ Divine Orb
const newRule = {
    id: 'rule_divine',
    show_hide: 'Show',
    conditions: [
        { type: 'BaseType', operator: '==', values: ['Divine'] }
    ],
    actions: [
        { type: 'SetTextColor', values: [232, 231, 171] },
        { type: 'SetBorderColor', values: [232, 37, 97] },
        { type: 'SetBackgroundColor', values: [232, 37, 97] },
        { type: 'SetFontSize', values: [45] },
        { type: 'CustomAlertSound', values: ['divine.mp3', 100] }
    ],
    comment: 'Divine Orb - High Value',
    enabled: true
};

editor.rules.push(newRule);
editor.updateRulesList();
```

### การปรับแต่งสี
```javascript
// เปลี่ยนสี text เป็นสีทอง
const textColorAction = rule.actions.find(a => a.type === 'SetTextColor');
if (textColorAction) {
    textColorAction.values = [255, 215, 0]; // RGB for gold
    editor.updateSelectedRule();
}
```

## การแก้ไขปัญหา

### ปัญหาที่พบบ่อย

#### 1. Import ไม่ได้
- ตรวจสอบว่าไฟล์เป็น .filter, .json, หรือ .yaml
- ตรวจสอบขนาดไฟล์ (ไม่เกิน 10MB)
- ตรวจสอบ syntax ของไฟล์

#### 2. Preview ไม่แสดง
- ตรวจสอบว่า rules มี enabled: true
- ตรวจสอบว่า rules มี show_hide: 'Show'
- รีเฟรช preview โดยคลิกปุ่ม Refresh

#### 3. เสียงไม่เล่น
- ตรวจสอบว่าไฟล์เสียงอยู่ในโฟลเดอร์ที่ถูกต้อง
- ตรวจสอบว่า browser รองรับการเล่นเสียง
- ลองใช้เสียงอื่น

### Debug Mode
เปิด Developer Tools (F12) เพื่อดู console logs และ debug ข้อมูล

## การพัฒนาต่อ

### ฟีเจอร์ที่กำลังพัฒนา
- [ ] Drag & Drop สำหรับการจัดเรียง rules
- [ ] Undo/Redo functionality
- [ ] Rule templates และ presets
- [ ] Advanced condition builder
- [ ] Multi-language support
- [ ] Dark/Light theme toggle

### การมีส่วนร่วม
1. Fork repository
2. สร้าง feature branch
3. Commit การเปลี่ยนแปลง
4. Push ไปยัง branch
5. สร้าง Pull Request

## License
MIT License - ดูรายละเอียดในไฟล์ LICENSE

## Support
หากพบปัญหาหรือต้องการความช่วยเหลือ:
- สร้าง Issue ใน GitHub
- ติดต่อผ่าน Discord
- อีเมล: support@dzxfilter.com

---

**DZX Filter Editor** - ทำให้การปรับแต่ง filter ง่ายขึ้น! 🎮✨
