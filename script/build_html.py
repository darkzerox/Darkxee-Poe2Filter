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
    play_effect_color: Optional[str] = None
    custom_sound: Optional[str] = None
    alert_sound_id: Optional[int] = None
    alert_sound_volume: Optional[int] = None
    conditions: Dict[str, str] = field(default_factory=dict)
    styles: Dict[str, str] = field(default_factory=lambda: {
        'color': 'rgb(255 255 255)',  # Default white text
        'border-color': 'rgb(120 120 120)',
        'background-color': 'rgba(10, 10, 10, 0.9)', 
        'font-size': '16px'
    })
    is_hidden: bool = False
    source_file: str = ""

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
    
    def __init__(self, project_path: Path, output_dir: Optional[Path] = None):
        self.project_path = project_path
        self.filter_group_path = project_path / "dzx_filter" / "filter_group"
        self.output_dir = output_dir if output_dir else project_path / "dist" / "web"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.preview_tags: Set[Tuple[str, str, str, str, str, str, str]] = set() # (text, style, category, sound, effect, icon_color, icon_shape)
    
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
        
        return "v0.5.4"  # Default fallback

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
    
    def process_filter_block(self, lines: List[str], source_file: str = "") -> Optional[FilterBlockData]:
        """Parse filter block lines into structured data"""
        if not lines:
            return None
            
        block_data = FilterBlockData(source_file=source_file)
        
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
                alpha = parts[4] if len(parts) >= 5 else "230" # standard alpha
                # Scale alpha to 0-1
                try:
                    a_val = float(alpha) / 255.0
                except ValueError:
                    a_val = 0.9
                block_data.styles['background-color'] = f'rgba({r} {g} {b} / {a_val:.2f})'
                
            elif keyword == 'SetFontSize' and len(parts) >= 2:
                try:
                    # Keep size proportional
                    original_size = int(parts[1])
                    block_data.styles['font-size'] = f'{original_size}px'
                except ValueError:
                    pass
                    
            elif keyword == 'MinimapIcon' and len(parts) >= 4:
                shape = parts[3]
                block_data.minimap_icon = shape
                
                if len(parts) >= 3:
                    color = parts[2]
                    if color.title() in ['Red', 'Green', 'Blue', 'Brown', 'White', 
                                       'Yellow', 'Cyan', 'Grey', 'Orange', 'Pink', 'Purple']:
                        block_data.minimap_color = color.lower()
                    else:
                        block_data.minimap_color = f'rgb({color})'
                        
            elif keyword == 'PlayEffect' and len(parts) >= 2:
                block_data.play_effect_color = parts[1].lower()
                
            elif keyword == 'CustomAlertSound' and len(parts) >= 2:
                sound_path = ' '.join(parts[1:]).replace('"', '').strip()
                block_data.custom_sound = sound_path
                
            elif keyword == 'PlayAlertSound' and len(parts) >= 2:
                try:
                    block_data.alert_sound_id = int(parts[1])
                    if len(parts) >= 3:
                        block_data.alert_sound_volume = int(parts[2])
                except ValueError:
                    pass
                        
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

        # Clean file name for category
        cat_name = filter_path.stem.replace('_', ' ').title()
        
        html_output = [f'<h3 class="category-header" data-file="{filter_path.name}">{cat_name} ({filter_path.name})</h3>']
        html_output.append('<div class="table-wrapper">')
        html_output.append('<table class="filter-table">')
        html_output.append('<thead><tr>')
        html_output.append('<th>Class</th><th>BaseType</th><th>Rarity</th>')
        html_output.append('<th>Conditions</th><th>Minimap & Effects</th><th>Preview</th>')
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
            row_parts.append(f'<td class="basetype-cell">{base_types}</td>')
            
            # Rarity column
            row_parts.append(f'<td>{block_data.rarity or "Any"}</td>')
            
            # Conditions column
            conditions = []
            for key, value in block_data.conditions.items():
                conditions.append(f"{key}: {value}")
            condition_text = ', '.join(conditions) if conditions else 'Any'
            row_parts.append(f'<td>{condition_text}</td>')
            
            # Icon and Effects column
            effect_parts = []
            if block_data.minimap_icon:
                icon_char = self.ICON_MAP.get(block_data.minimap_icon, '●')
                icon_class = f'minimap-indicator minimap-color-{block_data.minimap_color or "white"}'
                effect_parts.append(f'<span class="{icon_class}" title="Radar Icon: {block_data.minimap_color} {block_data.minimap_icon}">{icon_char}</span>')
            if block_data.play_effect_color:
                beam_class = f'beam-indicator beam-color-{block_data.play_effect_color}'
                effect_parts.append(f'<span class="{beam_class}" title="Beam: {block_data.play_effect_color}">❘</span>')
            if block_data.custom_sound:
                effect_parts.append(f'<span class="sound-indicator" title="Sound file: {block_data.custom_sound}">🔊</span>')
            elif block_data.alert_sound_id:
                effect_parts.append(f'<span class="sound-indicator" title="Alert Sound ID: {block_data.alert_sound_id}">🔔</span>')
                
            effect_text = ' '.join(effect_parts) if effect_parts else '-'
            row_parts.append(f'<td><div class="effects-cell">{effect_text}</div></td>')
            
            # Preview column
            preview_text = (block_data.base_types[0] if block_data.base_types else 
                           block_data.classes[0] if block_data.classes else "Item")
            
            # Clean up quotes for HTML attribute
            preview_clean_name = preview_text.replace('"', '').strip()
            
            # Build style string  
            style_parts = []
            for key, value in block_data.styles.items():
                if value:
                    style_parts.append(f'{key}: {value}')
            if block_data.is_hidden:
                style_parts.append('text-decoration: line-through')
                style_parts.append('opacity: 0.4')
            
            style_str = '; '.join(style_parts)
            
            # Sound dataset
            sound_attr = ""
            if block_data.custom_sound:
                sound_attr = f'data-sound="{block_data.custom_sound}"'
            elif block_data.alert_sound_id:
                sound_attr = f'data-alert-id="{block_data.alert_sound_id}"'
                
            # Effect dataset
            effect_attr = f'data-effect="{block_data.play_effect_color or ""}"'
            
            # Minimap dataset
            icon_shape = block_data.minimap_icon or ""
            icon_color = block_data.minimap_color or ""
            minimap_attr = f'data-icon-shape="{icon_shape}" data-icon-color="{icon_color}"'
            
            row_parts.append(f'<td><div class="poe-item" style="{style_str}" onclick="playItemDropSound(this)" {sound_attr} {effect_attr} {minimap_attr}>{preview_clean_name}</div></td>')
            row_parts.append('</tr>')
            
            # Add to preview tags (only show items that are not hidden)
            if not block_data.is_hidden and preview_clean_name != "Item" and preview_clean_name != "Augment":
                self.preview_tags.add((
                    preview_clean_name, 
                    style_str, 
                    cat_name.lower(),
                    block_data.custom_sound or (str(block_data.alert_sound_id) if block_data.alert_sound_id else ""),
                    block_data.play_effect_color or "",
                    icon_color,
                    icon_shape
                ))
            
            return ''.join(row_parts)
        
        # Process filter content line by line
        for line in filter_content.split('\n'):
            line = line.strip()
            
            if line.startswith(('Show', 'Hide')) or not line or line.startswith('#'):
                # Process previous block
                if current_block:
                    block_data = self.process_filter_block(current_block, filter_path.name)
                    if block_data:
                        html_output.append(generate_table_row(block_data))
                        blocks_processed += 1
                        
                current_block = [line] if line.startswith(('Show', 'Hide')) else []
            else:
                current_block.append(line)
        
        # Process final block
        if current_block:
            block_data = self.process_filter_block(current_block, filter_path.name)
            if block_data:
                html_output.append(generate_table_row(block_data))
                blocks_processed += 1
        
        html_output.append('</tbody></table></div>')
        
        logger.debug(f"Processed {blocks_processed} filter blocks from {filter_path.name}")
        return '\n'.join(html_output)
    
    def generate_tag_cloud(self) -> str:
        """Generate animated item preview area"""
        if not self.preview_tags:
            return "<p>No preview items found</p>"
        
        # Unique categories
        cats = sorted(list(set(tag[2] for tag in self.preview_tags)))
        
        # Render category tabs
        tabs_html = ['<div class="tabs-container">']
        tabs_html.append('<button class="tab-btn active" onclick="filterGallery(\'all\')">All</button>')
        for cat in cats:
            tab_label = cat.title()
            tabs_html.append(f'<button class="tab-btn" onclick="filterGallery(\'{cat}\')">{tab_label}</button>')
        tabs_html.append('</div>')
        
        # Render Loot Grid ("The Ground")
        loot_grid_html = ['<div class="loot-ground" id="loot-ground">']
        
        # Add visual effect wrapper for beams
        loot_grid_html.append('<div class="beam-layer" id="beam-layer"></div>')
        
        for index, (tag_text, style, category, sound, effect, icon_color, icon_shape) in enumerate(sorted(self.preview_tags)):
            clean_tag = tag_text.replace('"', '').strip()
            
            # Sound attributes
            sound_attr = ""
            if sound:
                if sound.isdigit():
                    sound_attr = f'data-alert-id="{sound}"'
                else:
                    sound_attr = f'data-sound="{sound}"'
                    
            effect_attr = f'data-effect="{effect}"'
            minimap_attr = f'data-icon-shape="{icon_shape}" data-icon-color="{icon_color}"'
            
            loot_grid_html.append(f'''
            <div class="poe-item animate-drop" style="{style}" 
                 data-category="{category}" 
                 onclick="playItemDropSound(this)"
                 {sound_attr} {effect_attr} {minimap_attr}
                 style="animation-delay: {index * 0.02:.2f}s;">{clean_tag}</div>''')
            
        loot_grid_html.append('</div>')
        
        return f'''
        <h2>🎮 Interactive Ground Preview (ทดสอบคลิกไอเทมเพื่อฟังเสียง/ดูแสง)</h2>
        <p style="color: #aaa; font-size: 0.95rem; margin-top: -10px; margin-bottom: 20px;">
           นี่คือจำลองการตกของไอเทมบนพื้นในเกม สามารถพิมพ์ค้นหา หรือเลือกหมวดหมู่ที่ต้องการด้านล่างนี้ได้
        </p>
        
        <div class="ground-control-panel">
            <div class="search-wrapper">
                <input type="text" id="item-search" placeholder="🔍 Search item names... (เช่น Chaos, Divine, Rune)" oninput="searchItems(this.value)">
            </div>
            { ''.join(tabs_html) }
        </div>
        
        <div class="game-ground-container">
            <!-- Minimap Mockup -->
            <div class="radar-map-wrapper">
                <div class="radar-title">🛰️ Minimap Radar</div>
                <div class="radar-disc">
                    <div class="radar-crosshair"></div>
                    <div class="radar-ping" id="radar-ping"></div>
                </div>
            </div>
            
            <!-- Items Grid -->
            { ''.join(loot_grid_html) }
        </div>
        '''
    
    def generate_html_content(self, filter_array: List[str]) -> str:
        """Generate complete HTML content"""
        version = self.get_git_version()
        
        # Ensure CSS files exist and are up to date
        self._ensure_css_files_exist()
        
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
        
        return self._build_html_template(version, tag_cloud_html, tables_html)
    
    def _ensure_css_files_exist(self):
        """Ensure main.css and filter_styles.css exist"""
        css_dir = self.output_dir / 'dzx_filter' / 'css'
        js_dir = self.output_dir / 'dzx_filter' / 'js'
        
        # Create directories if they don't exist
        css_dir.mkdir(parents=True, exist_ok=True)
        js_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if main.css exists, if not create it
        main_css_path = css_dir / 'main.css'
        self._create_main_css(main_css_path)
        
        # Check if main.js exists, if not create it
        main_js_path = js_dir / 'main.js'
        self._create_main_js(main_js_path)
    
    def _create_main_css(self, css_path: Path):
        """Create main.css with base styles"""
        main_css_content = '''/* DZX Filter PoE2 Premium Theme */
/* Generated by DZX Filter Build System */

@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Outfit:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: 'Outfit', sans-serif;
    background-color: #060608;
    background-image:
        radial-gradient(circle at 50% 0%, rgba(139, 92, 26, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 10% 50%, rgba(10, 80, 150, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(120, 20, 180, 0.08) 0%, transparent 40%);
    background-attachment: fixed;
    color: #e2e8f0;
    line-height: 1.6;
    padding: 20px 12px;
}

@media (max-width: 480px) {
    body { padding: 10px 8px; }
}

.container {
    max-width: 1400px;
    margin: 0 auto 20px auto;
    background: rgba(14, 16, 22, 0.75);
    border-radius: 12px;
    padding: clamp(14px, 3vw, 30px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
    border: 1px solid rgba(212, 175, 55, 0.15);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    color: #f7fafc;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
}

h1 {
    font-family: 'Cinzel Decorative', serif;
    font-size: clamp(1.3rem, 4.5vw, 2.5rem);
    color: #e5c158;
    text-align: center;
    letter-spacing: clamp(0.5px, 0.4vw, 2px);
    margin-bottom: 5px;
    text-shadow: 0px 4px 15px rgba(229, 193, 88, 0.4);
    line-height: 1.3;
}

h2 { font-size: clamp(1rem, 2.5vw, 1.4rem); margin-bottom: 8px; }
h3 { font-size: clamp(0.9rem, 2vw, 1.15rem); }

.header-logo {
    max-width: min(560px, 88vw);
    width: 100%;
    border-radius: 6px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    display: block;
    margin: 0 auto;
}

.sub-title {
    text-align: center;
    color: #a0aec0;
    font-size: clamp(0.82rem, 2vw, 1.05rem);
    margin-bottom: 18px;
    padding: 0 8px;
}

.badges { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.badges img { height: 20px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)); }

.download-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    text-align: center;
}

@media (max-width: 600px) {
    .download-section { grid-template-columns: 1fr; gap: 12px; }
}

.download-card {
    background: rgba(22, 26, 36, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: clamp(12px, 2.5vw, 20px);
    transition: border-color 0.3s, background 0.3s, transform 0.3s;
}

.download-card:hover {
    border-color: #e5c158;
    background: rgba(30, 36, 50, 0.7);
    transform: translateY(-2px);
}

.download-card p { color: #a0aec0; font-size: clamp(0.78rem, 1.5vw, 0.9rem); margin-top: 5px; }

.download-button {
    display: inline-block;
    padding: clamp(9px, 1.5vw, 14px) clamp(14px, 2.5vw, 28px);
    background: linear-gradient(135deg, #c5a043 0%, #917122 100%);
    color: #060608;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: clamp(0.72rem, 1.4vw, 0.9rem);
    letter-spacing: 0.8px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(197, 160, 67, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-top: 12px;
}

.download-button:hover {
    background: linear-gradient(135deg, #e5c158 0%, #c5a043 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(197, 160, 67, 0.5);
    color: #000;
}

.ground-control-panel { display: flex; flex-direction: column; gap: 10px; margin-bottom: 14px; }
.search-wrapper { width: 100%; }

#item-search {
    width: 100%;
    padding: 10px 14px;
    background: rgba(10, 12, 16, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: #fff;
    font-family: inherit;
    font-size: clamp(0.85rem, 1.5vw, 0.95rem);
    transition: border-color 0.3s, box-shadow 0.3s;
}

#item-search:focus { border-color: #e5c158; outline: none; box-shadow: 0 0 8px rgba(229, 193, 88, 0.2); }
#item-search::placeholder { color: #718096; }

/* Tabs: horizontal scroll on mobile, wrap on desktop */
.tabs-container {
    display: flex;
    gap: 5px;
    overflow-x: auto;
    flex-wrap: nowrap;
    padding-bottom: 5px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: rgba(212, 175, 55, 0.3) transparent;
}

@media (min-width: 1024px) {
    .tabs-container { flex-wrap: wrap; overflow-x: visible; padding-bottom: 0; }
}

.tab-btn {
    flex-shrink: 0;
    padding: clamp(5px, 0.9vw, 8px) clamp(9px, 1.4vw, 13px);
    background: rgba(22, 26, 36, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    color: #a0aec0;
    border-radius: 4px;
    font-size: clamp(0.72rem, 1.2vw, 0.83rem);
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
    transition: color 0.2s, border-color 0.2s, background 0.2s;
}

.tab-btn:hover { color: #fff; border-color: rgba(255,255,255,0.2); }
.tab-btn.active { background: rgba(229, 193, 88, 0.15); border-color: #e5c158; color: #e5c158; }

.game-ground-container {
    display: flex;
    gap: 14px;
    background-color: #090b0e;
    background-image:
        radial-gradient(rgba(255,255,255,0.03) 1px, transparent 0),
        linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8));
    background-size: 24px 24px, 100%;
    border-radius: 8px;
    padding: clamp(12px, 2.5vw, 22px);
    min-height: 300px;
    border: 1px solid rgba(0, 0, 0, 0.5);
    box-shadow: inset 0 0 40px rgba(0,0,0,0.9);
    position: relative;
}

@media (max-width: 768px) {
    .game-ground-container { flex-direction: column; gap: 10px; min-height: unset; }
}

.radar-map-wrapper {
    flex: 0 0 auto;
    width: 185px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(10, 12, 17, 0.85);
    border-radius: 6px;
    padding: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    align-self: flex-start;
}

@media (max-width: 768px) {
    .radar-map-wrapper { width: 100%; flex-direction: row; justify-content: center; gap: 14px; align-items: center; }
}

.radar-title { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; color: #e5c158; margin-bottom: 10px; font-weight: 600; }
@media (max-width: 768px) { .radar-title { margin-bottom: 0; } }

.radar-disc {
    width: 145px;
    height: 145px;
    border-radius: 50%;
    background-color: rgba(5, 10, 15, 0.8);
    border: 2px solid rgba(74, 158, 255, 0.3);
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 15px rgba(74, 158, 255, 0.1);
    flex-shrink: 0;
}

@media (max-width: 480px) { .radar-disc { width: 100px; height: 100px; } }

.radar-crosshair {
    position: absolute;
    width: 100%; height: 100%;
    top: 0; left: 0;
    background:
        linear-gradient(to right, transparent 49.5%, rgba(74,158,255,0.15) 50%, transparent 50.5%),
        linear-gradient(to bottom, transparent 49.5%, rgba(74,158,255,0.15) 50%, transparent 50.5%);
}

.radar-ping {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 14px; height: 14px;
    border-radius: 50%;
    display: none;
    font-size: 14px;
    line-height: 14px;
    text-align: center;
    font-weight: bold;
}

.radar-ping.active { display: block; animation: radarPulse 1.2s infinite; }

@keyframes radarPulse {
    0%   { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    50%  { box-shadow: 0 0 15px currentColor; }
    100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

.loot-ground {
    flex: 1;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    gap: 7px;
    position: relative;
    max-height: 480px;
    overflow-y: auto;
    padding-right: 4px;
}

@media (max-width: 768px) { .loot-ground { max-height: 320px; } }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
::-webkit-scrollbar-thumb { background: rgba(212, 175, 55, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(212, 175, 55, 0.6); }

.poe-item {
    display: inline-block;
    padding: 3px 9px;
    border: 1px solid #7f7f7f;
    background-color: rgba(0, 0, 0, 0.9);
    color: #fff;
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 600;
    border-radius: 2px;
    cursor: pointer;
    user-select: none;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    text-shadow: 1px 1px 1px #000, -1px -1px 1px #000, 1px -1px 1px #000, -1px 1px 1px #000;
    white-space: nowrap;
    line-height: 1.4;
    max-width: 300px;
    overflow: hidden;
}

.poe-item:hover { transform: scale(1.06); box-shadow: 0 0 12px currentColor; z-index: 5; }

.beam-layer {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 1;
}

.beam-ray {
    position: absolute;
    bottom: 0;
    width: 6px;
    height: 100%;
    transform: translateX(-50%);
    background: linear-gradient(to top, transparent, currentColor 70%, #fff 100%);
    opacity: 0.95;
    filter: blur(2px) drop-shadow(0 0 8px currentColor);
    animation: beamFade 0.8s ease-out forwards;
}

@keyframes beamFade {
    0%   { height: 0%;   opacity: 1; }
    50%  { height: 100%; opacity: 0.8; }
    100% { height: 100%; opacity: 0; }
}

.table-wrapper {
    overflow-x: auto;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    -webkit-overflow-scrolling: touch;
}

.category-header {
    margin-top: 28px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid rgba(212, 175, 55, 0.25);
    font-size: clamp(0.95rem, 2vw, 1.2rem);
    color: #e5c158;
}

.filter-table {
    width: 100%;
    border-collapse: collapse;
    background-color: rgba(10, 12, 16, 0.6);
    font-size: clamp(0.76rem, 1.4vw, 0.88rem);
    min-width: 580px;
}

.filter-table th {
    background-color: rgba(18, 22, 28, 0.9);
    color: #a0aec0;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.68rem;
    letter-spacing: 0.8px;
    padding: 9px 11px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
    white-space: nowrap;
}

.filter-table td { padding: 7px 11px; border-bottom: 1px solid rgba(255, 255, 255, 0.03); text-align: center; color: #cbd5e0; }
.filter-table tr:hover { background-color: rgba(255, 255, 255, 0.02); }
.filter-table td.basetype-cell { text-align: left; font-family: monospace; font-size: 0.8rem; color: #e2e8f0; }
.effects-cell { display: flex; justify-content: center; gap: 6px; font-size: 0.95rem; }

.minimap-indicator { font-size: 0.95rem; text-shadow: 0 0 5px currentColor; }
.beam-indicator    { font-size: 1.1rem; font-weight: bold; text-shadow: 0 0 5px currentColor; }
.sound-indicator   { font-size: 0.85rem; opacity: 0.8; }

.minimap-color-red,    .beam-color-red    { color: #f56565; }
.minimap-color-green,  .beam-color-green  { color: #48bb78; }
.minimap-color-blue,   .beam-color-blue   { color: #4299e1; }
.minimap-color-brown,  .beam-color-brown  { color: #b7791f; }
.minimap-color-white,  .beam-color-white  { color: #ffffff; }
.minimap-color-yellow, .beam-color-yellow { color: #ecc94b; }
.minimap-color-cyan,   .beam-color-cyan   { color: #38b2ac; }
.minimap-color-grey,   .beam-color-grey   { color: #a0aec0; }
.minimap-color-orange, .beam-color-orange { color: #ed8936; }
.minimap-color-pink,   .beam-color-pink   { color: #ed64a6; }
.minimap-color-purple, .beam-color-purple { color: #9f7aea; }

@keyframes tagDrop {
    0%   { opacity: 0; transform: scale(0.6) translateY(-12px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-drop { animation: tagDrop 0.22s ease-out both; }

.version-tag {
    display: inline-block;
    padding: 2px 7px;
    background: rgba(229, 193, 88, 0.15);
    border: 1px solid #e5c158;
    color: #e5c158;
    border-radius: 3px;
    font-size: 0.72rem;
    vertical-align: middle;
    margin-left: 8px;
    font-family: monospace;
}

pre {
    background-color: rgba(5, 7, 10, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: clamp(10px, 2vw, 15px);
    border-radius: 4px;
    overflow-x: auto;
    font-family: monospace;
    color: #48bb78;
    font-size: clamp(0.72rem, 1.3vw, 0.84rem);
    margin-top: 14px;
    -webkit-overflow-scrolling: touch;
}

.dev-tip {
    border-left: 4px solid #e5c158;
    padding: clamp(10px, 2vw, 15px);
    margin: 18px 0;
    background: rgba(229, 193, 88, 0.05);
    border-radius: 0 4px 4px 0;
    font-size: clamp(0.82rem, 1.4vw, 0.92rem);
    line-height: 1.6;
}

.site-footer { text-align: center; margin: 36px 0 14px; color: #718096; font-size: clamp(0.78rem, 1.4vw, 0.88rem); }
.site-footer a { color: #e5c158; text-decoration: none; }
.site-footer a:hover { text-decoration: underline; }
.site-footer .copyright { font-size: clamp(0.68rem, 1.2vw, 0.78rem); margin-top: 4px; opacity: 0.6; }
'''
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(main_css_content)
    
    def _create_main_js(self, js_path: Path):
        """Create main.js with base functionality"""
        main_js_content = '''// DZX Filter Main JavaScript
// Generated by DZX Filter Build System

// AudioContext for synthesized alert sounds
let audioCtx = null;

function getAudioContext() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtx;
}

/**
 * Play a synthesized sound based on Alert ID
 */
function playSynthBeep(id) {
    try {
        const ctx = getAudioContext();
        if (ctx.state === 'suspended') {
            ctx.resume();
        }
        
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        const now = ctx.currentTime;
        
        // Define sound qualities based on ID
        if (id === 1 || id === 11) { // High Value Beep
            osc.type = 'sine';
            osc.frequency.setValueAtTime(880, now);
            osc.frequency.exponentialRampToValueAtTime(1200, now + 0.15);
            gain.gain.setValueAtTime(0.3, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
            osc.start(now);
            osc.stop(now + 0.3);
        } else if (id === 2 || id === 12) { // Normal Currency Beep
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(523.25, now); // C5
            osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
            osc.start(now);
            osc.stop(now + 0.25);
        } else if (id === 3 || id === 13) { // Unique Sound
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(330, now);
            osc.frequency.linearRampToValueAtTime(165, now + 0.4);
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
            osc.start(now);
            osc.stop(now + 0.4);
        } else if (id === 4 || id === 14) { // Map / Key Sound
            osc.type = 'sine';
            osc.frequency.setValueAtTime(587.33, now); // D5
            osc.frequency.exponentialRampToValueAtTime(880, now + 0.1);
            gain.gain.setValueAtTime(0.25, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
            osc.start(now);
            osc.stop(now + 0.3);
        } else if (id === 6 || id === 16) { // Special Beep
            osc.type = 'sine';
            osc.frequency.setValueAtTime(1000, now);
            osc.frequency.setValueAtTime(1500, now + 0.05);
            osc.frequency.setValueAtTime(2000, now + 0.1);
            gain.gain.setValueAtTime(0.3, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
            osc.start(now);
            osc.stop(now + 0.25);
        } else { // Standard Beep
            osc.type = 'sine';
            osc.frequency.setValueAtTime(440, now);
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
            osc.start(now);
            osc.stop(now + 0.2);
        }
    } catch (e) {
        console.error('Error playing synthesized sound:', e);
    }
}

/**
 * Handle Item Drop Click: Play sound, show light beam, update minimap radar
 */
function playItemDropSound(element) {
    const soundPath = element.getAttribute('data-sound');
    const alertId = element.getAttribute('data-alert-id');
    const effectColor = element.getAttribute('data-effect');
    const iconShape = element.getAttribute('data-icon-shape');
    const iconColor = element.getAttribute('data-icon-color');
    
    // 1. Play Sound
    if (soundPath) {
        // Build correct relative path
        const audio = new Audio(soundPath);
        audio.volume = 0.5;
        audio.play().catch(err => {
            console.warn('Audio play failed, falling back to synthesizer:', err);
            // Fallback to synth if audio file isn't copied/loaded
            playSynthBeep(2);
        });
    } else if (alertId) {
        playSynthBeep(parseInt(alertId));
    }
    
    // 2. Play Beam Effect
    if (effectColor) {
        triggerGroundBeam(element, effectColor);
    }
    
    // 3. Update Radar
    if (iconShape && iconColor) {
        triggerRadarPing(iconShape, iconColor);
    }
}

/**
 * Render a vertical light beam matching PoE drop effect
 */
function triggerGroundBeam(element, colorName) {
    const ground = document.getElementById('loot-ground');
    const beamLayer = document.getElementById('beam-layer');
    if (!ground || !beamLayer) return;
    
    // Get absolute positioning relative to the ground container
    const groundRect = ground.getBoundingClientRect();
    const elemRect = element.getBoundingClientRect();
    
    const posX = elemRect.left - groundRect.left + (elemRect.width / 2) + ground.scrollLeft;
    
    // Create beam element
    const beam = document.createElement('div');
    beam.className = `beam-ray beam-color-${colorName}`;
    beam.style.left = `${posX}px`;
    
    beamLayer.appendChild(beam);
    
    // Auto remove after animation completes
    setTimeout(() => {
        beam.remove();
    }, 850);
}

/**
 * Show a radar ping on the mockup map
 */
function triggerRadarPing(shape, color) {
    const ping = document.getElementById('radar-ping');
    if (!ping) return;
    
    // Mapping of shapes to text character
    const iconMap = {
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
        'Kite': '⬜'
    };
    
    const iconChar = iconMap[shape] || '●';
    
    ping.className = 'radar-ping active';
    // Remove colors
    ping.style.color = '';
    
    if (color.startsWith('rgb')) {
        ping.style.color = color;
    } else {
        ping.classList.add(`minimap-color-${color}`);
    }
    
    ping.innerText = iconChar;
    
    // Restart animation
    const newPing = ping.cloneNode(true);
    ping.parentNode.replaceChild(newPing, ping);
}

/**
 * Filter item gallery by category
 */
function filterGallery(category) {
    // Update active tab button
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        if (btn.getAttribute('onclick').includes(category)) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    const items = document.querySelectorAll('#loot-ground .poe-item');
    items.forEach(item => {
        const itemCat = item.getAttribute('data-category');
        if (category === 'all' || itemCat === category) {
            item.style.display = 'inline-block';
        } else {
            item.style.display = 'none';
        }
    });
}

/**
 * Search items in ground preview
 */
function searchItems(query) {
    const cleanedQuery = query.toLowerCase().trim();
    const items = document.querySelectorAll('#loot-ground .poe-item');
    
    // Clear active tab filter if searching
    if (cleanedQuery.length > 0) {
        const buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(btn => btn.classList.remove('active'));
        document.querySelector('.tab-btn[onclick*="all"]').classList.add('active');
    }
    
    items.forEach(item => {
        const text = item.innerText.toLowerCase();
        if (text.includes(cleanedQuery)) {
            item.style.display = 'inline-block';
        } else {
            item.style.display = 'none';
        }
    });
}

/**
 * Fetch the latest tag from GitHub and update the version display
 */
async function fetchLatestTag() {
    try {
        const response = await fetch('https://api.github.com/repos/darkzerox/Darkxee-Poe2Filter/tags');
        if (!response.ok) throw new Error('Network response was not ok');
        const tags = await response.json();
        const latestTag = tags[0]?.name || 'v0.5.4';
        
        // Update version display
        const versionElement = document.getElementById('repo-version');
        if (versionElement) {
            versionElement.innerText = latestTag;
        }
    } catch (error) {
        console.error('Error fetching latest tag:', error);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DZX Filter Premium Previewer initialized');
    fetchLatestTag();
});
'''
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(main_js_content)
    
    def _build_html_template(self, version: str, tag_cloud_html: str, tables_html: List[str]) -> str:
        """Build the complete HTML template with external CSS and JS"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DZX Filter for POE2 - {version} | Path of Exile 2 Item Filter</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="DZX Poe2 Filter - Professional item filter for Path of Exile 2. Preview item drop beams, minimap radar icons, and play alert sounds directly in your web browser. Available for PC & PS5.">
    <meta name="keywords" content="Path of Exile 2, POE2, Item Filter, DZX Filter, Loot Filter, Gaming, loot filter preview">
    <meta name="author" content="Darkxee">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="DZX Filter for POE2 - Premium Item Filter">
    <meta property="og:description" content="Interactive item filter preview with sounds, beams, and minimap radar simulation. Available for PC & PS5.">
    <meta property="og:image" content="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png">
    <meta property="og:url" content="https://darkzerox.github.io/Darkxee-Poe2Filter/">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="dzx_filter/css/main.css">
</head>

<body>
    <div class="container">
        <div align="center">
            <img alt="DZX Poe2 Filter Logo"
                 src="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png"
                 class="header-logo">

            <h1 style="margin-top: 12px;">DZX Poe2 Filter <span class="version-tag" id="repo-version">{version}</span></h1>
            <div class="sub-title">🎯 Advanced Item Filter for Path of Exile 2 (รองรับ PC และ PS5)</div>

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

    <!-- Download Section -->
    <div class="container download-section">
        <div class="download-card">
            <h3>💻 PC (Steam / Client)</h3>
            <p>ฟิลเตอร์แบบรวมไฟล์เสียงและเอฟเฟกต์ สำหรับเครื่องคอมพิวเตอร์</p>
            <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest" class="download-button">
                Download Latest Release (.zip)
            </a>
        </div>
        <div class="download-card">
            <h3>🎮 Console (PS5 / Xbox)</h3>
            <p>ซิงค์โดยตรงกับบัญชี Path of Exile ผ่านเว็บบอร์ดหลักเพื่อใช้งานบนคอนโซล</p>
            <a href="https://www.pathofexile.com/account/view-profile/Darkxee-3892/item-filters" class="download-button" target="_blank">
                Follow on Path of Exile website
            </a>
        </div>
    </div>

    <!-- Interactive Ground Preview -->
    <div class="container">
        {tag_cloud_html}
    </div>

    <!-- Raw Rules Section -->
    <div class="container">
        <h2>📋 Detailed Filter Rules (โครงสร้างและสไตล์ไฟล์ดิบ)</h2>
        <p style="color: #a0aec0; font-size: clamp(0.82rem, 1.5vw, 0.95rem); margin-bottom: 16px;">
           ตารางแสดงผลสไตล์และกฎทั้งหมดของฟิลเตอร์ โดยแยกตามหัวข้อไฟล์ .filter ต่างๆ ในการใช้งาน
        </p>
        {''.join(tables_html)}
    </div>

    <!-- Developer Section -->
    <div class="container">
        <h2>🛠️ Developer Guide & Compilation</h2>
        <p style="color: #a0aec0; font-size: clamp(0.85rem, 1.5vw, 0.95rem);">สามารถดาวน์โหลด/โคลนคลังโค้ดเพื่อแก้ไข ปรับแต่งเสียง หรือแต่งสไตล์ของฟิลเตอร์เองได้ตามต้องการ</p>
        
        <pre><code># 1. โคลนคลังโค้ดลงเครื่อง
git clone https://github.com/darkzerox/Darkxee-Poe2Filter.git
cd Darkxee-Poe2Filter

# 2. รันสคริปต์คอมไพล์ฟิลเตอร์ (ต้องรันในโฟลเดอร์ root)
python script/start_build.py

# 3. ไฟล์เอาต์พุตที่คอมไพล์แล้วจะอยู่ในโฟลเดอร์ dist/
# สคริปต์จะคัดลอกไฟล์ตรงไปยังโฟลเดอร์ของเกม Path of Exile 2 ให้อัตโนมัติ (หากตั้งค่าไว้ใน config.json)</code></pre>
        
        <div class="dev-tip">
            💡 <strong>Tip สำหรับนักพัฒนา:</strong> ปรับแต่งคีย์ไอเทมหรือแยก Tier ได้ง่ายๆ ผ่านโฟลเดอร์ <code>dzx_filter/filter_group</code> (แยก subdirectory: content/, gear/, unique/) แล้วสั่งรันสคริปต์บิลด์ซ้ำอีกครั้ง
        </div>
    </div>

    <!-- Footer -->
    <div class="site-footer">
        <p>Made with ⚔️ by <a href="https://github.com/darkzerox">Darkxee</a> for the Path of Exile 2 Community</p>
        <p class="copyright">This is a fan-made project. Path of Exile is a trademark of Grinding Gear Games.</p>
    </div>

    <!-- Scripts -->
    <script src="dzx_filter/js/main.js"></script>
</body>
</html>'''
    
    def write_html_file(self, filter_array: List[str], output_file_name: str = "index.html") -> bool:
        """Generate and write HTML file"""
        logger.info(f"Generating HTML preview from {len(filter_array)} filter files")
        
        try:
            html_content = self.generate_html_content(filter_array)
            output_path = self.output_dir / output_file_name
            
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
    test_path = _html_generator.output_dir / "test_preview.html"
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
        
    print("\n🎉 All build_html tests passed!")
    return True

if __name__ == "__main__":
    if '--test' in sys.argv:
        run_tests()
    else:
        print("Use --test to run tests")
