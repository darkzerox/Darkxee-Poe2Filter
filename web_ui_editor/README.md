# DZX Filter Editor - Next.js

A modern web interface for creating and customizing Path of Exile 2 item filters.

## Features

- 🎨 **Visual Editor**: Edit colors, fonts, sounds, and icons with an intuitive interface
- 📁 **Import/Export**: Support for .filter, .json, and .yaml formats
- 👁️ **Realtime Preview**: See changes instantly with live preview
- 🗂️ **Category Management**: Organize rules by item categories
- 🔊 **Sound Testing**: Test alert sounds directly in the browser
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Frontend**: Next.js 15, React 18, TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI, Lucide React
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd web_ui_editor
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
web_ui_editor/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── api/            # API routes
│   │   ├── editor/         # Filter editor page
│   │   ├── demo/           # Demo page
│   │   └── page.tsx        # Home page
│   ├── components/          # React components
│   │   ├── FilterEditor.tsx
│   │   ├── RealtimePreview.tsx
│   │   ├── PropertiesPanel.tsx
│   │   └── CategorySidebar.tsx
│   └── lib/                # Utility libraries
│       ├── FilterParser.ts
│       └── ImportExportManager.ts
├── public/                 # Static assets
│   └── sounds/            # Sound files
├── package.json
├── vercel.json            # Vercel deployment config
└── README.md
```

## API Endpoints

- `POST /api/parse` - Parse filter content
- `POST /api/generate` - Generate filter content

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy automatically

### Manual Deployment

```bash
npm run build
npm start
```

## Usage

### Importing Filters

1. Click "Import" in the editor
2. Select a .filter, .json, or .yaml file
3. The filter will be parsed and loaded

### Editing Rules

1. Select a rule from the list
2. Use the Properties Panel to modify:
   - Colors (text, border, background)
   - Font size
   - Alert sounds
   - Minimap icons
3. Changes are applied instantly

### Preview

- Switch to the Preview tab to see how items will look
- Test sounds by clicking on preview items
- View statistics about visible/hidden items

### Export

1. Click "Export" to download your filter
2. Choose format: .filter (for POE2), .json, or .yaml
3. Install the .filter file in your POE2 directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)
- Discord: [Join our community](https://discord.gg/your-server)

## Acknowledgments

- Path of Exile 2 community
- Next.js team
- Vercel platform
- All contributors