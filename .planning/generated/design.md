# DZX Filter POE2 - System Design (Updated)

## สถาปัตยกรรมระบบ

### ภาพรวมสถาปัตยกรรม
ระบบ DZX Filter POE2 ใช้สถาปัตยกรรมแบบโมดูลาร์ที่แบ่งออกเป็นส่วนต่างๆ ที่ทำงานร่วมกัน พร้อม Web Interface สำหรับการปรับปรุง

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │  Filter Engine  │    │  Output Files  │
│                │───▶│                │───▶│                │
│ - Import/Export│    │ - Rules Engine │    │ - .filter      │
│ - Visual Editor│    │ - Color Logic  │    │ - HTML         │
│ - Realtime Prev│    │ - Sound Logic  │    │ - CSS          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Settings │    │  Filter Parser  │    │  File Manager   │
│                │    │                │    │                │
│ - Preferences   │    │ - Syntax Check │    │ - Version Ctrl  │
│ - Presets      │    │ - Validation   │    │ - Backup        │
│ - History      │    │ - Merge Logic  │    │ - Export        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### โครงสร้างโมดูล

#### 1. Web Interface Module (NEW)
- **Frontend Controller**: จัดการการโต้ตอบกับผู้ใช้
- **Visual Editor**: แก้ไข filter rules แบบ visual
- **Realtime Preview**: แสดงตัวอย่างผลลัพธ์ทันที
- **Import/Export Manager**: จัดการการนำเข้าและส่งออกไฟล์
- **Settings Manager**: จัดการการตั้งค่าผู้ใช้

#### 2. Filter Parser Module (NEW)
- **Syntax Parser**: แปลง filter syntax เป็นโครงสร้างข้อมูล
- **Validation Engine**: ตรวจสอบความถูกต้องของ filter
- **Merge Engine**: รวมหลาย filter files เป็นไฟล์เดียว
- **Export Engine**: สร้าง filter files จากโครงสร้างข้อมูล

#### 3. Input Module
- **Configuration Parser**: อ่านการตั้งค่าจากไฟล์ config
- **User Preferences**: จัดการความต้องการของผู้ใช้
- **Custom Rules**: จัดการกฎที่ผู้ใช้กำหนดเอง
- **File Import**: นำเข้า filter files จากภายนอก (NEW)

#### 4. Filter Engine
- **Rules Engine**: ประมวลผลกฎการฟิลเตอร์
- **Color Logic**: จัดการสีและการแสดงผล
- **Sound Logic**: จัดการเสียงและเอฟเฟกต์
- **Platform Logic**: จัดการความแตกต่างระหว่างแพลตฟอร์ม

#### 5. Output Module
- **Filter Generator**: สร้างไฟล์ .filter
- **HTML Generator**: สร้างไฟล์ HTML สำหรับการแสดงผล
- **CSS Generator**: สร้างไฟล์ CSS สำหรับการจัดรูปแบบ
- **Export Manager**: จัดการการส่งออกไฟล์ (NEW)

### การออกแบบฐานข้อมูล

#### 1. Item Categories (Enhanced)
```yaml
categories:
  currency:
    name: "Currency"
    color: "#FFD700"
    sound: "currency.mp3"
    priority: 1
    icon: "coin"
    sections:
      - high_value
      - medium_value
      - low_value
  
  jewels:
    name: "Jewels"
    color: "#FF69B4"
    sound: "jewel.mp3"
    priority: 2
    icon: "gem"
    sections:
      - unique_jewels
      - rare_jewels
      - magic_jewels
  
  maps:
    name: "Maps"
    color: "#32CD32"
    sound: "map.mp3"
    priority: 3
    icon: "map"
    sections:
      - high_tier
      - medium_tier
      - low_tier
```

#### 2. Filter Rules (Enhanced)
```yaml
rules:
  - id: "rule_001"
    category: "currency"
    section: "high_value"
    conditions:
      - type: "BaseType"
        values: ["Chaos Orb", "Exalted Orb"]
        operator: "=="
    actions:
      - set_color: "#FFD700"
      - set_sound: "currency.mp3"
      - set_size: "Large"
      - set_icon: "star"
    priority: 1
    enabled: true
```

#### 3. User Settings (NEW)
```yaml
user_settings:
  preferences:
    theme: "dark"
    language: "th"
    auto_save: true
    preview_mode: "realtime"
  
  presets:
    - name: "Default"
      description: "Default filter settings"
      rules: ["rule_001", "rule_002"]
    
    - name: "High End"
      description: "For high level players"
      rules: ["rule_003", "rule_004"]
  
  history:
    - timestamp: "2024-12-19T10:30:00Z"
      action: "import"
      filename: "custom.filter"
    
    - timestamp: "2024-12-19T10:35:00Z"
      action: "edit_rule"
      rule_id: "rule_001"
```

### การออกแบบส่วนติดต่อผู้ใช้

#### 1. Web Interface Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Header: Logo, Version, User Menu                            │
├─────────────────────────────────────────────────────────────┤
│ Sidebar: Categories, Sections, Tools                       │
├─────────────────────────────────────────────────────────────┤
│ Main Content:                                               │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Filter Editor   │ │ Visual Preview  │ │ Settings Panel  │ │
│ │                 │ │                 │ │                 │ │
│ │ - Rule List     │ │ - Item Preview  │ │ - Colors        │ │
│ │ - Condition Ed. │ │ - Sound Test    │ │ - Sounds        │ │
│ │ - Action Ed.    │ │ - Icon Preview  │ │ - Icons         │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Footer: Status, Save Button, Export Options                 │
└─────────────────────────────────────────────────────────────┘
```

#### 2. Component Design

##### Filter Editor Component
```javascript
class FilterEditor {
  constructor() {
    this.rules = [];
    this.categories = [];
    this.currentRule = null;
  }
  
  addRule(rule) {
    // Add new rule
  }
  
  editRule(ruleId, changes) {
    // Edit existing rule
  }
  
  deleteRule(ruleId) {
    // Delete rule
  }
  
  validateRule(rule) {
    // Validate rule syntax
  }
}
```

##### Realtime Preview Component
```javascript
class RealtimePreview {
  constructor() {
    this.previewItems = [];
    this.currentFilter = null;
  }
  
  updatePreview() {
    // Update preview based on current filter
  }
  
  playSound(soundFile) {
    // Play sound preview
  }
  
  showItemPreview(item) {
    // Show item with current styling
  }
}
```

##### Import/Export Manager
```javascript
class ImportExportManager {
  constructor() {
    this.supportedFormats = ['.filter', '.json', '.yaml'];
  }
  
  importFile(file) {
    // Import filter file
  }
  
  exportFile(format, data) {
    // Export filter file
  }
  
  validateFile(file) {
    // Validate imported file
  }
}
```

### การออกแบบการประมวลผล

#### 1. Filter Processing Pipeline (Enhanced)
```
Input → Parse → Validate → Process → Preview → Generate → Output
  │       │        │         │         │         │         │
  ▼       ▼        ▼         ▼         ▼         ▼         ▼
File   AST     Syntax    Rules    Realtime  Filter   Files
Import Check   Check    Engine    Preview  Generator Export
```

#### 2. Rule Evaluation (Enhanced)
- **Condition Matching**: ตรวจสอบเงื่อนไข
- **Action Execution**: ดำเนินการตามกฎ
- **Priority Handling**: จัดลำดับความสำคัญ
- **Realtime Update**: อัปเดตผลลัพธ์ทันที (NEW)

#### 3. Web Interface Processing (NEW)
```
User Input → Validation → Processing → Update UI → Save State
     │           │           │           │           │
     ▼           ▼           ▼           ▼           ▼
  Click/Edit  Check Data  Apply Rules  Refresh   Persist
              Format      Changes      Preview   Changes
```

### การออกแบบการทดสอบ

#### 1. Unit Tests
- ทดสอบแต่ละโมดูลแยกกัน
- ทดสอบการประมวลผลกฎ
- ทดสอบการสร้างไฟล์
- ทดสอบ Web Interface components (NEW)

#### 2. Integration Tests
- ทดสอบการทำงานร่วมกันของโมดูล
- ทดสอบการสร้างฟิลเตอร์สมบูรณ์
- ทดสอบการทำงานบนแพลตฟอร์มต่างๆ
- ทดสอบ Import/Export functionality (NEW)

#### 3. User Acceptance Tests
- ทดสอบการใช้งานจริง
- ทดสอบประสิทธิภาพ
- ทดสอบความเข้ากันได้
- ทดสอบ Web Interface usability (NEW)

#### 4. Web Interface Tests (NEW)
- Cross-browser testing
- Responsive design testing
- Performance testing
- Accessibility testing

### การออกแบบการปรับขยาย

#### 1. Plugin System
- รองรับการเพิ่มประเภทไอเทมใหม่
- รองรับการเพิ่มกฎใหม่
- รองรับการเพิ่มเสียงใหม่
- รองรับการเพิ่ม Web Interface components (NEW)

#### 2. Template System
- เทมเพลตสำหรับสี
- เทมเพลตสำหรับเสียง
- เทมเพลตสำหรับการแสดงผล
- เทมเพลตสำหรับ Web Interface themes (NEW)

#### 3. API System (NEW)
- REST API สำหรับการจัดการ filter
- WebSocket สำหรับ realtime updates
- GraphQL สำหรับ complex queries
- Webhook สำหรับ external integrations

### การออกแบบความปลอดภัย

#### 1. Input Validation
- ตรวจสอบความถูกต้องของข้อมูล
- ป้องกันการโจมตีแบบ injection
- จำกัดขนาดไฟล์
- Validate file uploads (NEW)

#### 2. Output Sanitization
- ทำความสะอาดข้อมูลก่อนส่งออก
- ป้องกันการแสดงผลที่ไม่ปลอดภัย
- ตรวจสอบความถูกต้องของไฟล์
- Sanitize user-generated content (NEW)

#### 3. Web Security (NEW)
- CSRF protection
- XSS prevention
- File upload security
- Session management

### การออกแบบประสิทธิภาพ

#### 1. Caching
- แคชการประมวลผลกฎ
- แคชไฟล์ที่สร้างแล้ว
- แคชการตั้งค่าผู้ใช้
- แคช Web Interface assets (NEW)

#### 2. Optimization
- ลดการประมวลผลที่ไม่จำเป็น
- ใช้โครงสร้างข้อมูลที่มีประสิทธิภาพ
- ลดขนาดไฟล์ที่สร้าง
- Optimize Web Interface performance (NEW)

#### 3. Lazy Loading (NEW)
- Load components on demand
- Progressive enhancement
- Code splitting
- Asset optimization

### การออกแบบการใช้งาน

#### 1. User Journey
```
1. User opens web interface
2. User imports existing filter or starts new
3. User browses categories and sections
4. User edits rules visually
5. User sees realtime preview
6. User saves/exports filter
7. User downloads for game use
```

#### 2. Error Handling
- Graceful error messages
- Validation feedback
- Recovery mechanisms
- User guidance

#### 3. Accessibility
- Keyboard navigation
- Screen reader support
- High contrast mode
- Font size adjustment