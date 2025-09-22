# AGENTS.md - DZX Filter Editor Web UI

## Project Overview
DZX Filter Editor เป็น Web-based Filter Editor สำหรับเกม Path of Exile 2 ที่พัฒนาด้วย Next.js 15 และ TypeScript โดยมีจุดมุ่งหมายเพื่อให้ผู้เล่นสามารถสร้าง แก้ไข และจัดการ item filters ผ่าน web interface ที่ทันสมัยและใช้งานง่าย

## Modern UI Design System

### Design Philosophy
- **Glass Morphism**: ใช้ backdrop blur และ transparency effects
- **Gradient Design**: ไล่สีที่สวยงามและทันสมัย
- **Micro-animations**: อนิเมชันเล็กๆ ที่เพิ่มประสบการณ์ผู้ใช้
- **Dark Theme**: ธีมมืดที่เหมาะสำหรับการใช้งานนานๆ
- **Responsive**: รองรับทุกขนาดหน้าจอ

### Color Palette
```css
Primary: #667eea → #764ba2 (Blue to Purple)
Secondary: #f093fb → #f5576c (Pink to Red)
Accent: #4facfe → #00f2fe (Cyan to Blue)
Success: #11998e → #38ef7d (Teal to Green)
Warning: #f2994a → #f2c94c (Orange to Yellow)
Danger: #ff416c → #ff4b2b (Red)
```

### Modern Components
- **Buttons**: `.btn-primary`, `.btn-secondary`, `.btn-outline`, `.btn-ghost`
- **Cards**: `.card-modern`, `.card-glass`
- **Inputs**: `.input-modern`, `.focus-modern`
- **Tabs**: `.tab-modern` with gradient underlines
- **Effects**: `.glass`, `.glass-dark`, `.hover-lift`, `.hover-glow`

## Build and Test Commands

### การติดตั้ง Dependencies
```bash
# ติดตั้ง Node.js dependencies
cd web_ui_editor
npm install

# หรือใช้ pnpm
pnpm install
```

### การ Development
```bash
# รัน development server
npm run dev
# หรือ
pnpm dev

# Build สำหรับ production
npm run build
# หรือ
pnpm build

# รัน production server
npm run start
# หรือ
pnpm start
```

### การทดสอบ
```bash
# ทดสอบการ build
npm run build

# ทดสอบ linting
npm run lint

# ทดสอบ TypeScript
npm run type-check
```

## Project Structure
```
web_ui_editor/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # Home page
│   │   ├── editor/            # Filter editor page
│   │   ├── demo/              # Demo page
│   │   ├── test/              # Test page
│   │   ├── simple-test/       # Modern UI showcase
│   │   ├── globals.css        # Global styles & design system
│   │   ├── layout.tsx         # Root layout
│   │   └── api/               # API routes
│   ├── components/            # React components
│   │   ├── FilterEditor.tsx   # Main editor component
│   │   ├── RealtimePreview.tsx # Preview component
│   │   ├── PropertiesPanel.tsx # Properties editor
│   │   └── CategorySidebar.tsx # Category navigation
│   └── lib/                   # Utility libraries
│       ├── FilterParser.ts    # Filter parsing logic
│       └── ImportExportManager.ts # File I/O
├── public/
│   └── sounds/               # Sound effect files
├── package.json              # Dependencies & scripts
├── next.config.js           # Next.js configuration
├── tailwind.config.ts       # Tailwind CSS config
└── vercel.json              # Vercel deployment config
```

## Code Style Guidelines

### TypeScript
- ใช้ strict mode และ proper type annotations
- หลีกเลี่ยง `any` types เมื่อเป็นไปได้
- ใช้ interface สำหรับ object types
- เขียน JSDoc comments สำหรับ complex functions

### React/Next.js
- ใช้ `'use client'` directive สำหรับ client components
- ใช้ App Router patterns
- ใช้ proper state management with useState/useEffect
- ใช้ proper error boundaries

### CSS/Tailwind
- ใช้ utility classes เป็นหลัก
- ใช้ custom CSS classes สำหรับ complex styles
- ใช้ CSS variables สำหรับ theming
- ใช้ responsive design patterns

### Component Architecture
- Single Responsibility Principle
- Proper prop typing
- Use composition over inheritance
- Implement proper loading states

## Modern UI Guidelines

### Animation Principles
- **Smooth Transitions**: ใช้ `transition-all duration-200`
- **Hover Effects**: เพิ่ม scale และ shadow effects
- **Loading States**: ใช้ shimmer และ pulse animations
- **Staggered Animations**: อนิเมชันแบบขั้นบันได

### Glass Morphism
```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Gradient Usage
- ใช้ gradients สำหรับ backgrounds และ text
- ใช้ consistent gradient directions (135deg)
- ใช้ opacity variations สำหรับ layering

### Interactive Elements
- Hover states with visual feedback
- Focus states with ring effects
- Active states with scale transforms
- Loading states with animations

## Testing Instructions

### Unit Tests
- ทดสอบ individual components
- ทดสอบ utility functions
- ทดสอบ state management
- ทดสอบ error handling

### Integration Tests
- ทดสอบ component interactions
- ทดสอบ API routes
- ทดสอบ file operations
- ทดสอบ responsive behavior

### Visual Tests
- ทดสอบ modern UI components
- ทดสอบ animations และ transitions
- ทดสอบ glass effects
- ทดสอบ gradient rendering

### User Acceptance Tests
- ทดสอบ filter editing workflow
- ทดสอบ import/export functionality
- ทดสอบ realtime preview
- ทดสอบ responsive design

## Security Considerations

### Input Validation
- Validate filter file formats
- Sanitize user inputs
- Prevent XSS attacks
- Validate file uploads

### File Operations
- Limit file sizes
- Validate file types
- Secure file downloads
- Prevent path traversal

### API Security
- Rate limiting
- Input sanitization
- Error handling
- CORS configuration

## Development Workflow

### Feature Development
1. **Planning**: ออกแบบ UI/UX ใน Figma
2. **Implementation**: พัฒนา components และ logic
3. **Testing**: ทดสอบ functionality และ UI
4. **Review**: Code review และ UI review
5. **Deployment**: Deploy ไปยัง Vercel

### Modern UI Development
1. **Design System**: ใช้ consistent design tokens
2. **Component Library**: สร้าง reusable components
3. **Animation**: เพิ่ม micro-interactions
4. **Responsive**: ทดสอบทุกขนาดหน้าจอ
5. **Performance**: Optimize loading และ rendering

### Version Control
- ใช้ Git สำหรับ version control
- ใช้ feature branches สำหรับ new features
- ใช้ semantic versioning
- ใช้ conventional commits

## Deployment

### Vercel Deployment
```bash
# Deploy to Vercel
vercel --prod

# หรือใช้ GitHub integration
git push origin main
```

### Environment Variables
```env
NEXT_PUBLIC_APP_URL=https://dzx-filter-editor.vercel.app
NEXT_PUBLIC_VERSION=1.0.0
```

### Performance Optimization
- Image optimization
- Code splitting
- Lazy loading
- Caching strategies

## Modern UI Features

### Glass Morphism
- Backdrop blur effects
- Transparency layers
- Subtle borders
- Depth perception

### Gradient Design
- Color transitions
- Background overlays
- Text effects
- Interactive states

### Micro-animations
- Hover effects
- Loading states
- Page transitions
- Component animations

### Responsive Design
- Mobile-first approach
- Flexible layouts
- Adaptive typography
- Touch-friendly interactions

## Support and Maintenance

### Bug Reports
- ใช้ GitHub Issues
- Include screenshots
- Describe steps to reproduce
- Specify browser/device

### Feature Requests
- Describe use case
- Provide mockups
- Consider impact
- Plan implementation

### Performance Monitoring
- Monitor Core Web Vitals
- Track user interactions
- Analyze loading times
- Optimize bottlenecks

## Contact Information

### Development Team
- **UI/UX Designer**: Modern design system
- **Frontend Developer**: React/Next.js implementation
- **Backend Developer**: API development

### Support Channels
- **GitHub Issues**: Technical support
- **Discord**: Community support
- **Email**: Direct support

## License
MIT License - ดูรายละเอียดในไฟล์ LICENSE

---

## Quick Start for New Developers

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd web_ui_editor
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development**
   ```bash
   npm run dev
   ```

4. **Open Browser**
   ```
   http://localhost:3000
   ```

5. **Test Modern UI**
   ```
   http://localhost:3000/simple-test
   ```

## Modern UI Showcase

### Test Pages
- **Home**: `/` - Modern landing page
- **Editor**: `/editor` - Filter editor interface
- **Demo**: `/demo` - Interactive demo
- **Test**: `/test` - Basic functionality test
- **Simple Test**: `/simple-test` - Modern UI showcase

### Key Features to Test
- Glass morphism effects
- Gradient backgrounds
- Micro-animations
- Hover interactions
- Responsive design
- Modern typography
- Interactive components

---

**Built with ❤️ using Next.js 15, TypeScript, Tailwind CSS, and modern design principles**
