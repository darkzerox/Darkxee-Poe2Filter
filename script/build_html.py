#!/usr/bin/env python3
"""
DZX Filter HTML Generator
=========================

This module generates HTML preview pages from Path of Exile 2 filter files.
It creates a comprehensive web-based preview showing filter rules, styles, and item examples.

Author: Darkxee
License: MIT
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass, field

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path configuration
script_dir = Path(__file__).parent
project_path = script_dir.parent

@dataclass 
class FilterBlockData:
    """Represents parsed filter block data for HTML generation"""
    classes: List[str] = field(default_factory=list)
    base_types: List[str] = field(default_factory=list)
    rarity: Optional[str] = None
    minimap_icon: Optional[str] = None
    minimap_color: Optional[str] = None
    conditions: Dict[str, str] = field(default_factory=dict)
    styles: Dict[str, str] = field(default_factory=lambda: {
        'color': 'rgb(255 255 255)',  # Default white text
        'border-color': None,
        'background-color': None, 
        'font-size': None
    })
    is_hidden: bool = False

class HTMLGenerator:
    """Generate HTML preview from filter files"""
    
    # Minimap icon mapping
    ICON_MAP = {
        'Circle': '●',
        'Diamond': '◆',
        'Hexagon': '⬢', 
        'Square': '■',
        'Star': '★',
        'Triangle': '▲',
        'Cross': '✕',
        'Moon': '☾',
        'Raindrop': '❧',
        'Pentagon': '⬟',
        'Kite': '⬜',
        'UpsideDownHouse': '⬢'
    }
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.filter_group_path = project_path / "dzx_filter" / "filter_group"
        self.preview_tags: Set[Tuple[str, str]] = set()
    
    def get_git_version(self) -> str:
        """Get current git version/tag"""
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'], 
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            logger.debug(f"Could not get git version: {e}")
        
        return "v1.0.0"  # Default fallback

    def _parse_filter_conditions(self, parts: List[str], block_data: FilterBlockData):
        """Parse filter condition rules"""
        keyword = parts[0]
        value = ' '.join(parts[1:]) if len(parts) > 1 else ""
        
        condition_mappings = {
            'AreaLevel': 'AreaLevel',
            'DropLevel': 'DropLevel', 
            'Sockets': 'Sockets',
            'Quality': 'Quality',
            'ItemLevel': 'ItemLevel'
        }
        
        if keyword in condition_mappings:
            block_data.conditions[condition_mappings[keyword]] = value
    
    def _parse_quoted_list(self, value: str) -> List[str]:
        """Parse quoted strings and clean up operators"""
        value = value.replace('"', '').strip()
        items = [item.strip() for item in value.split(',')]
        cleaned = []
        
        for item in items:
            # Remove comparison operators
            clean_item = item.replace('==', '').replace('>=', '').replace('<=', '').replace('=', '').strip()
            if clean_item:
                cleaned.append(clean_item)
                
        return cleaned
    
    def process_filter_block(self, lines: List[str]) -> Optional[FilterBlockData]:
        """Parse filter block lines into structured data"""
        if not lines:
            return None
            
        block_data = FilterBlockData()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split()
            if not parts:
                continue
                
            keyword = parts[0]
            
            if keyword in ('Show', 'Hide'):
                block_data.is_hidden = (keyword == 'Hide')
                continue
                
            # Parse selectors
            if keyword == 'Class':
                value = ' '.join(parts[1:])
                classes = self._parse_quoted_list(value)
                block_data.classes.extend(classes)
                
            elif keyword == 'BaseType':
                value = ' '.join(parts[1:])
                base_types = self._parse_quoted_list(value)
                block_data.base_types.extend(base_types)
                
            elif keyword == 'Rarity':
                value = ' '.join(parts[1:])
                rarities = self._parse_quoted_list(value)
                if rarities:
                    block_data.rarity = rarities[0]  # Take first rarity
                    
            # Parse visual styles
            elif keyword == 'SetTextColor' and len(parts) >= 4:
                r, g, b = parts[1:4]
                block_data.styles['color'] = f'rgb({r} {g} {b})'
                
            elif keyword == 'SetBorderColor' and len(parts) >= 4:
                r, g, b = parts[1:4]
                block_data.styles['border-color'] = f'rgb({r} {g} {b})'
                
            elif keyword == 'SetBackgroundColor' and len(parts) >= 4:
                r, g, b = parts[1:4]
                block_data.styles['background-color'] = f'rgb({r} {g} {b})'
                
            elif keyword == 'SetFontSize' and len(parts) >= 2:
                try:
                    # Scale down font size for web display
                    original_size = int(parts[1])
                    web_size = int(original_size * 0.5)
                    block_data.styles['font-size'] = f'{web_size}px'
                except ValueError:
                    pass
                    
            elif keyword == 'MinimapIcon' and len(parts) >= 4:
                shape = parts[3]
                block_data.minimap_icon = self.ICON_MAP.get(shape, '●')
                
                if len(parts) >= 3:
                    color = parts[2]
                    # Handle named colors vs RGB
                    if color.title() in ['Red', 'Green', 'Blue', 'Brown', 'White', 
                                       'Yellow', 'Cyan', 'Grey', 'Orange', 'Pink', 'Purple']:
                        block_data.minimap_color = color.lower()
                    else:
                        block_data.minimap_color = f'rgb({color})'
                        
            # Parse conditions
            else:
                self._parse_filter_conditions(parts, block_data)
        
        # Return block if it has meaningful content
        return block_data if (block_data.classes or block_data.base_types or 
                             any(v for v in block_data.styles.values() if v)) else None
    
    def filter_to_html_table(self, filter_path: Path) -> Optional[str]:
        """Convert filter file to HTML table representation"""
        try:
            with open(filter_path, 'r', encoding='utf-8') as f:
                filter_content = f.read()
        except Exception as e:
            logger.error(f"Error reading filter file {filter_path}: {e}")
            return None

        html_output = [f'<h3>{filter_path.name}</h3>']
        html_output.append('<table class="filter-table">')
        html_output.append('<thead><tr>')
        html_output.append('<th>Class</th><th>BaseType</th><th>Rarity</th>')
        html_output.append('<th>Conditions</th><th>Icon</th><th>Preview</th>')
        html_output.append('</tr></thead><tbody>')
        
        current_block = []
        blocks_processed = 0
        
        def generate_table_row(block_data: FilterBlockData) -> str:
            """Generate HTML table row from block data"""
            row_parts = ['<tr>']
            
            # Class column
            class_names = ', '.join(block_data.classes) if block_data.classes else 'ALL'
            row_parts.append(f'<td>{class_names}</td>')
            
            # BaseType column  
            base_types = ', '.join(block_data.base_types) if block_data.base_types else 'ALL'
            row_parts.append(f'<td>{base_types}</td>')
            
            # Rarity column
            row_parts.append(f'<td>{block_data.rarity or "Any"}</td>')
            
            # Conditions column
            conditions = []
            for key, value in block_data.conditions.items():
                conditions.append(f"{key}: {value}")
            condition_text = ', '.join(conditions) if conditions else 'Any'
            row_parts.append(f'<td>{condition_text}</td>')
            
            # Icon column
            if block_data.minimap_icon:
                icon_class = f'minimap-icon-{block_data.minimap_icon}'
                if block_data.minimap_color:
                    if block_data.minimap_color.startswith('rgb'):
                        icon_style = f'style="color: {block_data.minimap_color}"'
                        row_parts.append(f'<td><span class="{icon_class}" {icon_style}>{block_data.minimap_icon}</span></td>')
                    else:
                        row_parts.append(f'<td><span class="{icon_class} minimap-icon-{block_data.minimap_color}">{block_data.minimap_icon}</span></td>')
                else:
                    row_parts.append(f'<td><span class="{icon_class}">{block_data.minimap_icon}</span></td>')
            else:
                row_parts.append('<td>-</td>')
            
            # Preview column
            preview_text = (block_data.base_types[0] if block_data.base_types else 
                           block_data.classes[0] if block_data.classes else "ALL")
            truncated_name = preview_text[:10] + '...' if len(preview_text) > 10 else preview_text
            
            # Build style string  
            style_parts = []
            for key, value in block_data.styles.items():
                if value:
                    style_parts.append(f'{key}: {value}')
            if block_data.is_hidden:
                style_parts.append('text-decoration: line-through')
                style_parts.append('opacity: 0.7')
            
            style_str = '; '.join(style_parts)
            row_parts.append(f'<td><div class="style-box" style="{style_str}">{truncated_name}</div></td>')
            row_parts.append('</tr>')
            
            # Add to preview tags
            self.preview_tags.add((preview_text, style_str))
            
            return ''.join(row_parts)
        
        # Process filter content line by line
        for line in filter_content.split('\n'):
            line = line.strip()
            
            if line.startswith(('Show', 'Hide')) or not line or line.startswith('#'):
                # Process previous block
                if current_block:
                    block_data = self.process_filter_block(current_block)
                    if block_data:
                        html_output.append(generate_table_row(block_data))
                        blocks_processed += 1
                        
                current_block = [line] if line.startswith(('Show', 'Hide')) else []
            else:
                current_block.append(line)
        
        # Process final block
        if current_block:
            block_data = self.process_filter_block(current_block)
            if block_data:
                html_output.append(generate_table_row(block_data))
                blocks_processed += 1
        
        html_output.append('</tbody></table>')
        
        logger.debug(f"Processed {blocks_processed} filter blocks from {filter_path.name}")
        return '\n'.join(html_output)
    
    def generate_tag_cloud(self) -> str:
        """Generate animated tag cloud HTML from preview tags"""
        if not self.preview_tags:
            return "<p>No preview items found</p>"
        
        tag_cloud_parts = ['''
        <style>
        @keyframes fadeInScale {
            0% { opacity: 0; transform: scale(0.5) translateY(20px); }
            100% { opacity: 1; transform: scale(1) translateY(0); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .tag-cloud .tag {
            display: inline-block;
            padding: 8px 16px;
            margin: 6px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            animation: fadeInScale 0.6s ease backwards, float 3s ease-in-out infinite;
            border: 2px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(5px);
        }
        
        .tag-cloud .tag:hover {
            transform: scale(1.15) translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            animation-play-state: paused;
            z-index: 10;
        }
        </style>
        
        <h2>✨ Item Preview Gallery</h2>
        <div class="tag-cloud">''']
        
        for index, (tag_text, style) in enumerate(sorted(self.preview_tags)):
            clean_tag = tag_text[:20] + '...' if len(tag_text) > 20 else tag_text
            delay = index * 0.05
            float_duration = 3 + (index % 4)
            float_offset = (index * 25) % 100
            
            tag_cloud_parts.append(f'''
            <span class="tag" style="
                {style};
                animation: 
                    fadeInScale 0.6s ease backwards {delay}s,
                    float {float_duration}s ease-in-out infinite {float_offset}%;
                ">{clean_tag}</span>''')
        
        tag_cloud_parts.append('</div>')
        return ''.join(tag_cloud_parts)
    
    def generate_html_content(self, filter_array: List[str]) -> str:
        """Generate complete HTML content"""
        version = self.get_git_version()
        
        # Read CSS content
        css_path = self.project_path / 'dzx_filter' / 'css' / 'filter_styles.css'
        css_content = ""
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
        except Exception as e:
            logger.warning(f"Could not read CSS file: {e}")
        
        # Generate filter tables
        tables_html = []
        for filter_name in filter_array:
            filter_path = self.filter_group_path / filter_name
            if filter_path.exists():
                table_html = self.filter_to_html_table(filter_path)
                if table_html:
                    tables_html.append(table_html)
            else:
                logger.warning(f"Filter file not found: {filter_path}")
        
        # Generate tag cloud
        tag_cloud_html = self.generate_tag_cloud()
        
        return self._build_html_template(version, css_content, tag_cloud_html, tables_html)
    
    def _build_html_template(self, version: str, css_content: str, tag_cloud_html: str, tables_html: List[str]) -> str:
        """Build the complete HTML template"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DZX Filter for POE2 - {version} | Path of Exile 2 Item Filter</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="DZX Poe2 Filter - Professional item filter for Path of Exile 2. Enhance your gameplay with comprehensive item filtering. Download for PC and PS5.">
    <meta name="keywords" content="Path of Exile 2, POE2, Item Filter, DZX Filter, Loot Filter, Gaming">
    <meta name="author" content="Darkxee">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="DZX Filter for POE2 - {version}">
    <meta property="og:description" content="Professional Path of Exile 2 item filter system">
    <meta property="og:image" content="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png">
    <meta property="og:url" content="https://darkzerox.github.io/Darkxee-Poe2Filter/">
    
    <style>
        @font-face {{   
            font-family: 'Fontin';
            src: url('https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/fonts/Fontin-Regular.ttf') format('truetype');
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Fontin', Arial, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff;
            line-height: 1.6;
        }}
        
        .container {{
            background: rgba(45, 45, 45, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        h1, h2, h3 {{
            color: #4a9eff;
            text-shadow: 0 2px 4px rgba(74, 158, 255, 0.3);
        }}
        
        h1 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 30px;
        }}
        
        .filter-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(20, 20, 20, 0.8);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        .filter-table th {{
            background: linear-gradient(135deg, #4a9eff 0%, #357abd 100%);
            color: white;
            padding: 15px 10px;
            text-align: center;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .filter-table td {{
            padding: 12px 10px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: background-color 0.3s ease;
        }}
        
        .filter-table tr:hover {{
            background-color: rgba(74, 158, 255, 0.1);
        }}
        
        .filter-table tr td:nth-child(2) {{
            text-align: left;
            font-family: monospace;
        }}
        
        .style-box {{
            display: inline-block;
            padding: 8px 15px;
            border: 2px solid #666;
            border-radius: 8px;
            background: rgba(20, 20, 20, 0.9);
            font-family: 'Fontin', monospace;
            font-size: 14px;
            min-width: 80px;
            font-weight: 500;
            transition: transform 0.2s ease;
        }}
        
        .style-box:hover {{
            transform: scale(1.05);
        }}
        
        .tag-cloud {{
            text-align: center;
            margin: 30px 0;
            padding: 30px;
            background: rgba(20, 20, 20, 0.6);
            border-radius: 15px;
            min-height: 200px;
            border: 1px solid rgba(74, 158, 255, 0.2);
        }}
        
        .badges {{
            text-align: center;
            margin: 20px 0;
        }}
        
        .badges img {{
            margin: 5px;
        }}
        
        .download-section {{
            text-align: center;
            margin: 40px 0;
        }}
        
        .download-button {{
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            background: linear-gradient(135deg, #f17d40 0%, #ff4a4a 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(241, 125, 64, 0.4);
        }}
        
        .download-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(241, 125, 64, 0.6);
            text-decoration: none;
        }}
        
        .version-tag {{
            background: linear-gradient(135deg, #4a9eff 0%, #357abd 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        {css_content}
    </style>
</head>

<body>
    <div class="container">
        <div align="center">
            <picture>
                <img alt="DZX Poe2 Filter" 
                     src="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png" 
                     width="600" style="max-width: 100%; border-radius: 10px;">
            </picture>

            <h1>DZX Poe2 Filter <span class="version-tag" id="repo-version">{version}</span></h1>

            <script>
                async function fetchLatestTag() {{
                    try {{
                        const response = await fetch('https://api.github.com/repos/darkzerox/Darkxee-Poe2Filter/tags');
                        if (!response.ok) throw new Error('Network response was not ok');
                        const tags = await response.json();
                        const latestTag = tags[0]?.name || '{version}';
                        document.getElementById('repo-version').innerText = latestTag;
                        document.title = `DZX Filter for POE2 - ${{latestTag}} | Path of Exile 2 Item Filter`;
                    }} catch (error) {{
                        console.error('Error fetching latest tag:', error);
                    }}
                }}
                document.addEventListener('DOMContentLoaded', fetchLatestTag);
            </script>

            <p style="font-size: 1.2rem; color: #cccccc; margin: 20px 0;">
                🎯 <strong>Advanced Item Filter for Path of Exile 2</strong><br>
                เป็น Item Filter ที่พัฒนาขึ้นสำหรับ Path of Exile 2 โดยเฉพาะ<br>
                รองรับการรวมไฟล์อัตโนมัติด้วย Python
            </p>

            <div class="badges">
                <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases">
                    <img src="https://img.shields.io/github/v/release/darkzerox/Darkxee-Poe2Filter" alt="GitHub Release">
                </a>
                <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/actions">
                    <img src="https://img.shields.io/github/actions/workflow/status/darkzerox/Darkxee-Poe2Filter/python-app.yml" alt="Build Status">
                </a>
                <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/stargazers">
                    <img src="https://img.shields.io/github/stars/darkzerox/Darkxee-Poe2Filter" alt="Stars">
                </a>
            </div>
        </div>
    </div>

    <div class="container download-section">
        <h2>📥 Download</h2>
        <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest" class="download-button">
            💻 Download for PC
        </a>
        <a href="https://www.pathofexile.com/account/view-profile/Darkxee-3892/item-filters" class="download-button">  
            🎮 Download for PS5
        </a>
    </div>

    <div class="container">
        {tag_cloud_html}
    </div>

    <div class="container">
        <h2>📋 Filter Rules Preview</h2>
        {''.join(tables_html)}
    </div>

    <div class="container">
        <h2>🛠️ Developer Information</h2>
        <p>สามารถ <a href="https://github.com/darkzerox/Darkxee-Poe2Filter" style="color: #4a9eff;">Clone โปรเจค</a> ไปแก้ไขได้เลย</p>
        
        <h3>Build Instructions</h3>
        <pre style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 8px; overflow-x: auto;"><code># Clone the repository
git clone https://github.com/darkzerox/Darkxee-Poe2Filter.git
cd Darkxee-Poe2Filter

# Build all filters
cd script
python start_build.py

# Run tests
python merge_file.py --test
python build_css.py --test</code></pre>
        
        <blockquote style="border-left: 4px solid #4a9eff; padding: 15px; margin: 20px 0; background: rgba(74, 158, 255, 0.1);">
            💡 Filter นี้จะมีการอัพเดตอย่างสม่ำเสมอ กรุณาติดตามการอัพเดตและ Star โปรเจคเพื่อรับการแจ้งเตือน
        </blockquote>
    </div>

    <div style="text-align: center; margin: 40px 0; color: #888;">
        <p><sub>Made with ❤️ by <a href="https://github.com/darkzerox" style="color: #4a9eff;">Darkxee</a> for the Path of Exile 2 Community</sub></p>
    </div>
</body>
</html>'''
    
    def write_html_file(self, filter_array: List[str], output_file_name: str = "index.html") -> bool:
        """Generate and write HTML file"""
        logger.info(f"Generating HTML preview from {len(filter_array)} filter files")
        
        try:
            html_content = self.generate_html_content(filter_array)
            output_path = self.project_path / output_file_name
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML preview generated: {output_path}")
            logger.info(f"Preview tags collected: {len(self.preview_tags)}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating HTML: {e}")
            return False

# Global HTML generator instance  
_html_generator = HTMLGenerator(project_path)

def write_html_to_file(array_path: List[str], output_file_name: str = "index.html") -> bool:
    """Legacy function for backward compatibility"""
    return _html_generator.write_html_file(array_path, output_file_name)

def run_tests():
    """Run basic tests of HTML generation"""
    print("🧪 Running build_html tests...")
    
    test_files = [
        "rarity_magic.filter",
        "rarity_rare.filter",
        "currency.filter"
    ]
    
    # Test HTML generation
    print("\n   Test 1: HTML generation")
    success = write_html_to_file(test_files, "test_preview.html")
    if success:
        print("   ✅ HTML generation test passed")
    else:
        print("   ❌ HTML generation test failed")
        return False
    
    # Check if file was created
    test_path = project_path / "test_preview.html"
    if test_path.exists():
        print("   ✅ HTML file creation test passed")
        # Clean up
        try:
            test_path.unlink()
            print("   Cleaned up test HTML file")
        except Exception as e:
            print(f"   Warning: Could not clean up test file: {e}")
    else:
        print("   ❌ HTML file creation test failed")
        return False
    
    print("\n🎉 All HTML tests passed!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DZX Filter HTML Generator")
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--generate', nargs='+', help='Generate HTML from specific filter files')
    parser.add_argument('--output', default='preview.html', help='Output HTML file name')
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    elif args.generate:
        print(f"Generating HTML preview from files: {args.generate}")
        success = write_html_to_file(args.generate, args.output)
        if success:
            print(f"✅ HTML generation completed: {args.output}")
        else:
            print("❌ HTML generation failed")
            sys.exit(1)
    else:
        print("Use --test to run tests or --generate to generate HTML")
        parser.print_help()
