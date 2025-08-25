# AGENTS.md - DZX Filter POE2

## Project Overview
DZX Filter POE2 เป็นโปรเจคที่พัฒนาฟิลเตอร์สำหรับเกม Path of Exile 2 โดยมีจุดมุ่งหมายเพื่อปรับปรุงประสบการณ์การเล่นเกมของผู้เล่น ผ่านระบบฟิลเตอร์ที่ช่วยแยกแยะไอเทมต่างๆ พร้อมระบบเสียงและเอฟเฟกต์ที่ช่วยในการระบุไอเทม

## Build and Test Commands

### การติดตั้ง Dependencies
```bash
# ติดตั้ง Python dependencies
pip install -r requirements.txt

# หรือใช้ pnpm สำหรับ Node.js dependencies (ถ้ามี)
pnpm install
```

### การ Build ระบบ
```bash
# รันสคริปต์การสร้างหลัก
python script/start_build.py

# หรือรันแต่ละส่วนแยกกัน
python script/build_css.py
python script/build_html.py
python script/merge_file.py
```

### การทดสอบ
```bash
# ทดสอบการสร้างฟิลเตอร์
python -m pytest tests/

# ทดสอบการทำงานของสคริปต์
python script/test_build.py
```

## Code Style Guidelines

### Python
- ใช้ PEP 8 style guide
- ใช้ type hints เมื่อเป็นไปได้
- เขียน docstring สำหรับฟังก์ชันและคลาส
- ใช้ meaningful variable names

### HTML/CSS
- ใช้ semantic HTML
- ใช้ CSS Grid และ Flexbox สำหรับ layout
- รองรับ responsive design
- ใช้ CSS custom properties สำหรับสีและขนาด

### Filter Files
- ใช้ consistent naming convention
- จัดกลุ่มกฎตามประเภทไอเทม
- ใช้ comment เพื่ออธิบายกฎที่ซับซ้อน

## Testing Instructions

### Unit Tests
- ทดสอบแต่ละโมดูลแยกกัน
- ทดสอบการประมวลผลกฎ
- ทดสอบการสร้างไฟล์

### Integration Tests
- ทดสอบการทำงานร่วมกันของโมดูล
- ทดสอบการสร้างฟิลเตอร์สมบูรณ์
- ทดสอบการทำงานบนแพลตฟอร์มต่างๆ

### User Acceptance Tests
- ทดสอบการใช้งานจริง
- ทดสอบประสิทธิภาพ
- ทดสอบความเข้ากันได้

## Security Considerations

### Input Validation
- ตรวจสอบความถูกต้องของข้อมูล
- ป้องกันการโจมตีแบบ injection
- จำกัดขนาดไฟล์

### Output Sanitization
- ทำความสะอาดข้อมูลก่อนส่งออก
- ป้องกันการแสดงผลที่ไม่ปลอดภัย
- ตรวจสอบความถูกต้องของไฟล์

## Project Structure
```
dzx-filter-poe2/
├── .planning/           # ไฟล์การวางแผนและออกแบบ
├── dzx_filter/          # ทรัพยากรหลักของฟิลเตอร์
│   ├── css/            # ไฟล์ CSS
│   ├── filter_group/   # กลุ่มฟิลเตอร์ต่างๆ
│   ├── fonts/          # ฟอนต์
│   ├── images/         # ภาพ
│   └── soundeffect/    # ไฟล์เสียง
├── script/             # สคริปต์ Python สำหรับการสร้าง
├── *.filter            # ไฟล์ฟิลเตอร์สำหรับเกม
└── index.html          # หน้าเว็บหลัก
```

## Development Workflow

### Sprint Cycles
- ใช้ 6-week sprint cycles
- Week 1-2: วางแผนและออกแบบ
- Week 3-4: พัฒนาฟีเจอร์หลัก
- Week 5-6: ทดสอบและปรับปรุง

### Version Control
- ใช้ Git สำหรับ version control
- ใช้ feature branches สำหรับฟีเจอร์ใหม่
- ใช้ semantic versioning

### Code Review
- ทุก code change ต้องผ่าน code review
- ใช้ pull request workflow
- ทดสอบก่อน merge

## Deployment

### Release Process
1. สร้าง release branch
2. ทดสอบระบบ
3. สร้าง release notes
4. Tag version
5. Deploy ไปยัง production

### Rollback Plan
- มี rollback plan สำหรับทุก release
- เก็บ backup ของเวอร์ชันก่อนหน้า
- มี monitoring system เพื่อตรวจจับปัญหา

## Support and Maintenance

### Bug Reports
- ใช้ GitHub Issues สำหรับรายงานปัญหา
- ระบุ steps to reproduce
- แนบ error logs และ screenshots

### Feature Requests
- ใช้ GitHub Issues สำหรับ feature requests
- อธิบาย use case และประโยชน์
- ระบุ priority level

### Documentation
- อัปเดตเอกสารเมื่อมีการเปลี่ยนแปลง
- สร้าง tutorial สำหรับผู้ใช้ใหม่
- รักษา API documentation ให้เป็นปัจจุบัน

## Contact Information

### Development Team
- Project Lead: [ชื่อ]
- Lead Developer: [ชื่อ]
- UI/UX Designer: [ชื่อ]

### Support Channels
- GitHub Issues: สำหรับ technical support
- Email: [อีเมล]
- Discord: [ลิงก์ Discord]

## License
โปรเจคนี้ใช้ MIT License - ดูรายละเอียดในไฟล์ LICENSE
