#!/usr/bin/env python3
"""
DZX Filter CSS Generator
========================

This module generates CSS styles from Path of Exile 2 filter files for web preview.
It parses filter rules and converts them to CSS for HTML visualization.

Author: Darkxee
License: MIT
"""

import os
import sys
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path configuration
script_dir = Path(__file__).parent
project_path = script_dir.parent
filter_group_path = project_path / "dzx_filter" / "filter_group"

@dataclass
class FilterRule:
    """Represents a parsed filter rule with its properties"""
    selectors: List[str] = field(default_factory=list)
    text_color: Optional[str] = None
    border_color: Optional[str] = None
    background_color: Optional[str] = None
    font_size: Optional[str] = None
    minimap_icon: Optional[str] = None
    minimap_color: Optional[str] = None
    is_hidden: bool = False

class CSSGenerator:
    """Generate CSS from Path of Exile 2 filter files"""
    
    # Color mapping for named colors
    COLOR_MAP = {
        'Red': '255 0 0',
        'Green': '0 255 0', 
        'Blue': '0 0 255',
        'Brown': '160 110 60',
        'White': '255 255 255',
        'Yellow': '255 255 0',
        'Cyan': '0 255 255',
        'Grey': '150 150 150',
        'Orange': '255 150 0',
        'Pink': '255 192 203',
        'Purple': '128 0 128',
        'Black': '0 0 0'
    }
    
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
    
    def __init__(self, project_path: Path, filter_group_path: Path):
        self.project_path = project_path
        self.filter_group_path = filter_group_path
        self.processed_selectors: Set[str] = set()
        self.minimap_styles: Dict[str, str] = {}
        
    def _parse_rgb_color(self, color_str: str) -> Optional[str]:
        """Parse color string to RGB format"""
        if not color_str:
            return None
            
        # Handle named colors
        if color_str in self.COLOR_MAP:
            return f"rgb({self.COLOR_MAP[color_str]})"
        
        # Handle RGB values
        rgb_match = re.match(r'^(\d+)\s+(\d+)\s+(\d+)(?:\s+\d+)?$', color_str.strip())
        if rgb_match:
            r, g, b = rgb_match.groups()[:3]
            return f"rgb({r} {g} {b})"
            
        # Handle alpha RGB values  
        rgba_match = re.match(r'^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)$', color_str.strip())
        if rgba_match:
            r, g, b, a = rgba_match.groups()
            alpha = int(a) / 255.0
            return f"rgba({r}, {g}, {b}, {alpha:.2f})"
        
        logger.warning(f"Could not parse color: {color_str}")
        return None
    
    def _parse_filter_block(self, lines: List[str]) -> Optional[FilterRule]:
        """Parse a filter block and return a FilterRule"""
        rule = FilterRule()
        current_action = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split(None, 1)  # Split on first whitespace only
            if not parts:
                continue
                
            keyword = parts[0]
            value = parts[1] if len(parts) > 1 else ""
            
            if keyword in ('Show', 'Hide'):
                current_action = keyword
                rule.is_hidden = (keyword == 'Hide')
                continue
                
            # Handle selectors
            if keyword == 'Class':
                classes = self._parse_quoted_list(value)
                rule.selectors.extend([f'.filter-{cls.lower().replace(" ", "-")}' for cls in classes])
                
            elif keyword == 'BaseType':
                types = self._parse_quoted_list(value)
                rule.selectors.extend([f'[data-basetype="{typ}"]' for typ in types])
                
            elif keyword == 'Rarity':
                rarities = self._parse_quoted_list(value)
                rule.selectors.extend([f'.rarity-{rar.lower()}' for rar in rarities])
                
            # Handle visual properties
            elif keyword == 'SetTextColor':
                rule.text_color = self._parse_rgb_color(value)
                
            elif keyword == 'SetBorderColor':
                rule.border_color = self._parse_rgb_color(value)
                
            elif keyword == 'SetBackgroundColor':
                rule.background_color = self._parse_rgb_color(value)
                
            elif keyword == 'SetFontSize':
                try:
                    size = int(value)
                    rule.font_size = f"{size}px"
                except ValueError:
                    logger.warning(f"Invalid font size: {value}")
                    
            elif keyword == 'MinimapIcon':
                self._parse_minimap_icon(value, rule)
        
        return rule if (rule.selectors or rule.text_color or rule.border_color or 
                       rule.background_color or rule.font_size) else None
    
    def _parse_quoted_list(self, value: str) -> List[str]:
        """Parse quoted strings from filter value"""
        # Remove outer quotes and split on spaces outside quotes
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        
        # Split on commas or spaces, clean up
        items = re.split(r'[,\s]+', value)
        return [item.strip().strip('"') for item in items if item.strip()]
    
    def _parse_minimap_icon(self, value: str, rule: FilterRule):
        """Parse minimap icon configuration"""
        parts = value.split()
        if len(parts) >= 3:
            # MinimapIcon Size Color Shape
            size = parts[0]
            color = parts[1] 
            shape = parts[2]
            
            icon_symbol = self.ICON_MAP.get(shape, '●')
            rule.minimap_icon = icon_symbol
            
            # Parse color
            parsed_color = self._parse_rgb_color(color)
            if parsed_color:
                rule.minimap_color = parsed_color
                # Store for minimap-specific styles
                self.minimap_styles[f"minimap-icon-{shape.lower()}"] = parsed_color
    
    def _generate_css_rule(self, rule: FilterRule) -> Optional[str]:
        """Generate CSS rule from FilterRule"""
        if not rule.selectors:
            return None
            
        properties = []
        
        if rule.text_color:
            properties.append(f"color: {rule.text_color}")
            
        if rule.border_color:
            properties.append(f"border-color: {rule.border_color}")
            
        if rule.background_color:
            properties.append(f"background-color: {rule.background_color}")
            
        if rule.font_size:
            properties.append(f"font-size: {rule.font_size}")
            
        if rule.is_hidden:
            properties.append("opacity: 0.5")
            properties.append("text-decoration: line-through")
        
        if not properties:
            return None
            
        selectors = ", ".join(rule.selectors)
        props = ";\n    ".join(properties)
        
        return f"{selectors} {{\n    {props};\n}}"
    
    def _generate_base_css(self) -> str:
        """Generate base CSS styles"""
        return """
/* DZX Filter CSS - Base Styles */
/* Generated by DZX Filter Build System */

/* Reset and base styles */
* {
    box-sizing: border-box;
}

.filter-preview {
    font-family: 'Fontin', Arial, sans-serif;
    background: #1a1a1a;
    color: #ffffff;
    padding: 20px;
}

/* Minimap icon base styles */
[class*="minimap-icon-"] {
    display: inline-block;
    text-align: center;
    min-width: 20px;
    font-weight: bold;
    text-shadow: 1px 1px 1px rgba(0,0,0,0.7);
    font-size: 16px;
}

/* Default minimap icon colors */
.minimap-icon-circle { color: rgb(255 255 255); }
.minimap-icon-diamond { color: rgb(255 150 0); }
.minimap-icon-hexagon { color: rgb(255 0 0); }
.minimap-icon-square { color: rgb(0 255 0); }
.minimap-icon-star { color: rgb(0 255 255); }
.minimap-icon-triangle { color: rgb(160 110 60); }
.minimap-icon-cross { color: rgb(150 150 150); }
.minimap-icon-moon { color: rgb(150 200 255); }
.minimap-icon-raindrop { color: rgb(50 230 100); }
.minimap-icon-pentagon { color: rgb(255 150 0); }

/* Rarity-based styles */
.rarity-normal {
    color: rgb(200 200 200);
}

.rarity-magic {
    color: rgb(136 136 255);
}

.rarity-rare {
    color: rgb(255 255 119);
}

.rarity-unique {
    color: rgb(175 96 37);
}

/* Common filter classes */
.filter-currency {
    font-weight: bold;
    text-shadow: 0 0 5px currentColor;
}

.filter-gem {
    font-style: italic;
}

.filter-flask {
    border-radius: 4px;
    padding: 2px 6px;
}

/* Item preview box */
.style-box {
    display: inline-block;
    padding: 8px 12px;
    margin: 2px;
    border: 2px solid #666;
    border-radius: 4px;
    background-color: #2a2a2a;
    font-family: 'Fontin', monospace;
    font-size: 14px;
    min-width: 60px;
    text-align: center;
}
"""
    
    def generate_css(self, filter_paths: List[str], output_file_name: str = "filter_styles.css") -> bool:
        """Generate CSS from filter files"""
        logger.info(f"Generating CSS from {len(filter_paths)} filter files")
        
        css_parts = [self._generate_base_css()]
        rules_generated = 0
        
        for filter_path in filter_paths:
            full_path = self.filter_group_path / filter_path
            
            if not full_path.exists():
                logger.warning(f"Filter file not found: {full_path}")
                continue
                
            try:
                css_rules = self._process_filter_file(full_path)
                if css_rules:
                    css_parts.append(f"\n/* Rules from {filter_path} */")
                    css_parts.extend(css_rules)
                    rules_generated += len(css_rules)
                    logger.debug(f"Generated {len(css_rules)} rules from {filter_path}")
                    
            except Exception as e:
                logger.error(f"Error processing {filter_path}: {e}")
                continue
        
        # Add minimap-specific styles
        if self.minimap_styles:
            css_parts.append("\n/* Custom minimap icon colors */")
            for selector, color in self.minimap_styles.items():
                css_parts.append(f".{selector} {{ color: {color}; }}")
        
        # Write CSS file
        css_content = "\n".join(css_parts)
        return self._write_css_file(css_content, output_file_name, rules_generated)
    
    def _process_filter_file(self, file_path: Path) -> List[str]:
        """Process a single filter file and return CSS rules"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Could not read {file_path}: {e}")
            return []
        
        css_rules = []
        current_block = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Start new block on Show/Hide
            if line.startswith(('Show', 'Hide')):
                # Process previous block
                if current_block:
                    rule = self._parse_filter_block(current_block)
                    if rule:
                        css_rule = self._generate_css_rule(rule)
                        if css_rule:
                            css_rules.append(css_rule)
                
                current_block = [line]
            elif line and not line.startswith('#'):
                current_block.append(line)
        
        # Process final block
        if current_block:
            rule = self._parse_filter_block(current_block)
            if rule:
                css_rule = self._generate_css_rule(rule)
                if css_rule:
                    css_rules.append(css_rule)
        
        return css_rules
    
    def _write_css_file(self, css_content: str, output_file_name: str, rules_count: int) -> bool:
        """Write CSS content to file"""
        css_dir = self.project_path / 'dzx_filter' / 'css'
        css_dir.mkdir(exist_ok=True)
        
        output_path = css_dir / output_file_name
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
                
            logger.info(f"CSS generated successfully: {output_path}")
            logger.info(f"Generated {rules_count} CSS rules")
            return True
            
        except Exception as e:
            logger.error(f"Error writing CSS file: {e}")
            return False

# Global CSS generator instance
_css_generator = CSSGenerator(project_path, filter_group_path)

def filter_to_css(filter_paths: List[str], output_file_name: str = "filter_styles.css") -> str:
    """
    Legacy function for backward compatibility
    
    Args:
        filter_paths: List of filter file names
        output_file_name: Output CSS file name
        
    Returns:
        str: Generated CSS content (empty string on error)
    """
    success = _css_generator.generate_css(filter_paths, output_file_name)
    if success:
        # Read and return the generated CSS
        css_path = project_path / 'dzx_filter' / 'css' / output_file_name
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading generated CSS: {e}")
    
    return ""

def write_css_to_file(css_content: str, file_path: str):
    """Legacy function for backward compatibility"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        logger.info(f"CSS file written to {file_path}")
    except Exception as e:
        logger.error(f"Error writing CSS file: {e}")

def run_tests():
    """Run basic tests of CSS generation"""
    print("🧪 Running build_css tests...")
    
    # Test files that should exist
    test_files = [
        "rarity_magic.filter",
        "rarity_rare.filter",
        "currency.filter"
    ]
    
    # Test 1: Basic CSS generation
    print("\n   Test 1: Basic CSS generation")
    css_content = filter_to_css(test_files, "test_styles.css")
    if css_content and len(css_content) > 100:  # Should have substantial content
        print("   ✅ CSS generation test passed")
    else:
        print("   ❌ CSS generation test failed")
        return False
    
    # Test 2: Check if CSS file was created
    print("\n   Test 2: CSS file creation")
    css_path = project_path / 'dzx_filter' / 'css' / 'test_styles.css'
    if css_path.exists():
        print("   ✅ CSS file creation test passed")
    else:
        print("   ❌ CSS file creation test failed")
        return False
    
    # Clean up test file
    try:
        css_path.unlink()
        print("   Cleaned up test CSS file")
    except Exception as e:
        print(f"   Warning: Could not clean up test CSS file: {e}")
    
    print("\n🎉 All CSS tests passed!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DZX Filter CSS Generator")
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--generate', nargs='+', help='Generate CSS from specific filter files')
    parser.add_argument('--output', default='filter_styles.css', help='Output CSS file name')
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    elif args.generate:
        print(f"Generating CSS from files: {args.generate}")
        css_content = filter_to_css(args.generate, args.output)
        if css_content:
            print(f"✅ CSS generation completed: {args.output}")
        else:
            print("❌ CSS generation failed")
            sys.exit(1)
    else:
        print("Use --test to run tests or --generate to generate CSS")
        parser.print_help()