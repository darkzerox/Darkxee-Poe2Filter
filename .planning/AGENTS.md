# AGENTS.md - DZX Filter POE2 Planning & Development

## Project Overview
DZX Filter POE2 เป็นโปรเจคที่พัฒนาฟิลเตอร์สำหรับเกม Path of Exile 2 โดยมีจุดมุ่งหมายเพื่อปรับปรุงประสบการณ์การเล่นเกมของผู้เล่น ผ่านระบบฟิลเตอร์ที่ช่วยแยกแยะไอเทมต่างๆ พร้อมระบบเสียงและเอฟเฟกต์ที่ช่วยในการระบุไอเทม

## Project Structure
```
dzx-filter-poe2/
├── .planning/                 # ไฟล์การวางแผนและออกแบบ
│   ├── idea.md               # ไอเดียหลักของโปรเจค
│   ├── requirements.md       # ความต้องการของระบบ
│   ├── design.md             # การออกแบบระบบ
│   ├── tasks.md              # รายการงานที่ต้องทำ
│   ├── scratchboard.md       # การคิดวิเคราะห์และบันทึก
│   ├── prompts.md            # บันทึก prompts จากผู้ใช้
│   └── chart/                # ไดอะแกรมและแผนภาพ
│       ├── mermaid/          # Mermaid diagrams
│       └── svg/              # SVG exports
├── web_ui_editor/             # Modern Web UI Editor
│   ├── src/                  # Next.js source code
│   ├── public/               # Static assets
│   └── AGENTS.md             # Web UI specific guide
├── dzx_filter/               # ทรัพยากรหลักของฟิลเตอร์
│   ├── css/                  # ไฟล์ CSS
│   ├── filter_group/         # กลุ่มฟิลเตอร์ต่างๆ
│   ├── fonts/                # ฟอนต์
│   ├── images/               # ภาพ
│   └── soundeffect/          # ไฟล์เสียง
├── script/                   # สคริปต์ Python สำหรับการสร้าง
└── *.filter                 # ไฟล์ฟิลเตอร์สำหรับเกม
```

## Development Phases

### Phase 1: Planning & Design ✅
- [x] วิเคราะห์ความต้องการ
- [x] ออกแบบระบบ
- [x] สร้าง task list
- [x] วางแผน architecture

### Phase 2: Web UI Development ✅
- [x] สร้าง Next.js project
- [x] พัฒนา modern UI components
- [x] สร้าง filter editor interface
- [x] เพิ่ม glass morphism effects
- [x] เพิ่ม gradient designs
- [x] เพิ่ม micro-animations

### Phase 3: Core Functionality (In Progress)
- [ ] Filter parsing engine
- [ ] Import/Export functionality
- [ ] Realtime preview system
- [ ] Rule management system

### Phase 4: Advanced Features (Planned)
- [ ] Category management
- [ ] Bulk editing
- [ ] Template system
- [ ] User preferences

### Phase 5: Testing & Deployment (Planned)
- [ ] Unit testing
- [ ] Integration testing
- [ ] User acceptance testing
- [ ] Production deployment

## Modern UI Design System

### Design Philosophy
- **Glass Morphism**: ใช้ backdrop blur และ transparency
- **Gradient Design**: ไล่สีที่สวยงามและทันสมัย
- **Micro-animations**: อนิเมชันเล็กๆ ที่เพิ่มประสบการณ์
- **Dark Theme**: ธีมมืดที่เหมาะสำหรับการใช้งานนานๆ
- **Responsive**: รองรับทุกขนาดหน้าจอ

### Key Components
- **Modern Buttons**: Gradient backgrounds, hover effects
- **Glass Cards**: Backdrop blur, transparency
- **Modern Inputs**: Focus states, glass effects
- **Interactive Elements**: Hover animations, micro-interactions

## Build and Test Commands

### Web UI Editor
```bash
# Development
cd web_ui_editor
npm run dev

# Build
npm run build

# Test
npm run test
```

### Python Scripts
```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# รันสคริปต์การสร้าง
python script/start_build.py
```

## Code Style Guidelines

### Web UI (Next.js/TypeScript)
- ใช้ TypeScript strict mode
- ใช้ modern React patterns
- ใช้ Tailwind CSS utilities
- ใช้ glass morphism effects
- ใช้ gradient designs

### Python Scripts
- ใช้ PEP 8 style guide
- ใช้ type hints
- เขียน docstrings
- ใช้ meaningful variable names

### Filter Files
- ใช้ consistent naming
- จัดกลุ่มตามประเภท
- ใช้ comments อธิบาย

## Testing Instructions

### Web UI Testing
- ทดสอบ modern UI components
- ทดสอบ responsive design
- ทดสอบ animations
- ทดสอบ glass effects
- ทดสอบ gradient rendering

### Filter Testing
- ทดสอบการ parse filter files
- ทดสอบการ generate filters
- ทดสอบการ import/export
- ทดสอบการ preview

### Integration Testing
- ทดสอบการทำงานร่วมกัน
- ทดสอบการสร้างฟิลเตอร์สมบูรณ์
- ทดสอบการทำงานบนแพลตฟอร์มต่างๆ

## Security Considerations

### Web UI Security
- Input validation
- XSS prevention
- File upload security
- API security

### Filter Security
- File format validation
- Size limits
- Path traversal prevention
- Content sanitization

## Development Workflow

### Sprint Cycles (6-week)
- **Week 1-2**: Planning & Design
- **Week 3-4**: Core Development
- **Week 5**: Testing & Refinement
- **Week 6**: Deployment & Documentation

### Version Control
- ใช้ Git สำหรับ version control
- ใช้ feature branches
- ใช้ semantic versioning
- ใช้ conventional commits

### Code Review Process
- ทุก code change ต้องผ่าน review
- ใช้ pull request workflow
- ทดสอบก่อน merge
- Document changes

## Modern UI Features

### Glass Morphism
```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Gradient System
- Primary: Blue to Purple
- Secondary: Pink to Red
- Accent: Cyan to Blue
- Success: Teal to Green
- Warning: Orange to Yellow
- Danger: Red

### Animation System
- Fade in animations
- Slide in effects
- Scale transforms
- Hover interactions
- Loading states

## Deployment Strategy

### Web UI Deployment
- **Platform**: Vercel
- **Domain**: Custom domain
- **CDN**: Global edge network
- **SSL**: Automatic HTTPS

### Filter Distribution
- **GitHub Releases**: Version control
- **Direct Download**: User convenience
- **Community Sharing**: Social features

## Support and Maintenance

### Bug Reports
- ใช้ GitHub Issues
- Include screenshots
- Describe reproduction steps
- Specify environment

### Feature Requests
- Describe use case
- Provide mockups
- Consider impact
- Plan implementation

### Documentation
- Keep README updated
- Document API changes
- Create user guides
- Maintain changelog

## Contact Information

### Development Team
- **Project Lead**: Overall coordination
- **UI/UX Designer**: Modern design system
- **Frontend Developer**: React/Next.js
- **Backend Developer**: Python scripts

### Support Channels
- **GitHub Issues**: Technical support
- **Discord**: Community support
- **Email**: Direct support

## License
MIT License - ดูรายละเอียดในไฟล์ LICENSE

---

## Quick Start Guide

### For New Developers
1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd dzx-filter-poe2
   ```

2. **Start Web UI**
   ```bash
   cd web_ui_editor
   npm install
   npm run dev
   ```

3. **Test Modern UI**
   ```
   http://localhost:3000/simple-test
   ```

4. **Run Python Scripts**
   ```bash
   pip install -r requirements.txt
   python script/start_build.py
   ```

### For Users
1. **Access Web Editor**
   ```
   https://dzx-filter-editor.vercel.app
   ```

2. **Import Filter**
   - Upload existing .filter file
   - Start from template

3. **Customize**
   - Edit colors and sounds
   - Modify rules
   - Preview changes

4. **Export**
   - Download customized filter
   - Use in Path of Exile 2

---

**Built with ❤️ for the Path of Exile 2 Community**

**Modern UI powered by Next.js 15, TypeScript, Tailwind CSS, and Glass Morphism**
