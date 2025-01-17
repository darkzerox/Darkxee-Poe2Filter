import os

# Get directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent directory of script)
project_path = os.path.dirname(script_dir)
# Path to filter_group directory
filter_group_path = os.path.join(project_path, "dzx_filter", "filter_group")

def filter_to_css(filter_paths, output_file_name):
    css_output = []
    
    # Color name mapping
    color_map = {
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
        'Purple': '128 0 128'
    }
    
    # Add base styles for minimap icons
    base_styles = """
/* Base styles for minimap icons */
[class^="minimap-icon-"] {
    display: inline-block;
    text-align: center;
    min-width: 20px;
    font-weight: bold;
    text-shadow: 1px 1px 1px rgba(0,0,0,0.7);
}

/* Default colors for specific icon types */
.minimap-icon-● { color: rgb(255 255 255); }  /* White */
.minimap-icon-◆ { color: rgb(255 150 0); }    /* Orange */
.minimap-icon-⬢ { color: rgb(255 0 0); }      /* Red */
.minimap-icon-■ { color: rgb(0 255 0); }      /* Green */
.minimap-icon-★ { color: rgb(0 255 255); }    /* Cyan */
.minimap-icon-▲ { color: rgb(160 110 60); }   /* Brown */
.minimap-icon-✕ { color: rgb(150 150 150); }  /* Grey */
.minimap-icon-☾ { color: rgb(150 200 255); }  /* Light Blue */
.minimap-icon-❧ { color: rgb(50 230 100); }   /* Light Green */
.minimap-icon-⬟ { color: rgb(255 150 0); }    /* Orange */

/* Color-based classes */"""

    # Add color-based classes
    for color_name, rgb_value in color_map.items():
        base_styles += f"""
.minimap-icon-{color_name.lower()} {{
    color: rgb({rgb_value});
}}"""

    css_output.append(base_styles)
    
    # Helper function to process a block of filter rules
    def process_block(rules):
        if not rules:
            return None
            
        selectors = []
        properties = {}
        minimap_styles = []
        
        # Map for minimap icons to ASCII
        icon_map = {
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
        }
        
        for rule in rules:
            rule = rule.strip()
            if not rule or rule.startswith('#'):
                continue
                
            parts = rule.split()
            if not parts:
                continue
                
            # Handle Class and BaseType selectors
            if parts[0] == 'Class':
                # Remove quotes and create class selectors
                classes = ' '.join(parts[1:]).replace('"', '').split()
                selectors.extend([f'.{cls.lower()}' for cls in classes])
                
            elif parts[0] == 'BaseType':
                # Remove quotes and create attribute selectors
                types = ' '.join(parts[1:]).replace('"', '').split()
                selectors.extend([f'[data-basetype="{typ}"]' for typ in types])
                
            # Handle visual properties
            elif parts[0] == 'SetTextColor':
                properties['color'] = f'rgb({parts[1]} {parts[2]} {parts[3]})'
            elif parts[0] == 'SetBorderColor':
                properties['border-color'] = f'rgb({parts[1]} {parts[2]} {parts[3]})'
            elif parts[0] == 'SetBackgroundColor':
                properties['background-color'] = f'rgb({parts[1]} {parts[2]} {parts[3]})'
            elif parts[0] == 'SetFontSize':
                properties['font-size'] = f'{parts[1]}px'
            
            elif parts[0] == 'MinimapIcon':
                if len(parts) >= 4:
                    icon_shape = parts[3]
                    if len(parts) >= 3:  # Get color if specified
                        # Check if color is a name or RGB values
                        color_part = parts[2]
                        if color_part in color_map:
                            icon_color = f'rgb({color_map[color_part]})'
                        else:
                            # Assume it's RGB values
                            icon_color = f'rgb({color_part})'
                        minimap_styles.append(f"""
.minimap-icon-{icon_shape.lower()} {{
    color: {icon_color};
}}""")
        
        # Generate regular CSS rules
        if selectors and properties:
            selector_str = ', '.join(selectors)
            properties_str = ';\n    '.join([f'{k}: {v}' for k, v in properties.items()])
            css_rules = [f'{selector_str} {{\n    {properties_str};\n}}']
        else:
            css_rules = []
        
        # Add minimap icon styles
        css_rules.extend(minimap_styles)
        
        return '\n'.join(css_rules) if css_rules else None

    # Process each filter file
    for filter_path in filter_paths:
        current_block = []
        full_path = os.path.join(filter_group_path, filter_path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Filter file not found - {full_path}")
            continue
            
        try:
            with open(full_path, 'r') as f:
                filter_content = f.read()
                
            # Process the filter content line by line
            for line in filter_content.split('\n'):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    if current_block and line.startswith('#'):
                        # Process previous block
                        css_rule = process_block(current_block)
                        if css_rule:
                            css_output.append(css_rule)
                        current_block = []
                    continue
                    
                if line.startswith('Show') or line.startswith('Hide'):
                    # Process previous block
                    css_rule = process_block(current_block)
                    if css_rule:
                        css_output.append(css_rule)
                    current_block = []
                else:
                    current_block.append(line)
            
            # Process final block
            css_rule = process_block(current_block)
            if css_rule:
                css_output.append(css_rule)
                
        except Exception as e:
            print(f"Error processing filter file {filter_path}: {str(e)}")

    # Create output directory if it doesn't exist
    css_dir = os.path.join(project_path, 'dzx_filter', 'css')
    os.makedirs(css_dir, exist_ok=True)
    
    # Write the combined CSS to file
    css_content = '\n\n'.join(css_output)
    css_file_path = os.path.join(css_dir, output_file_name)
    write_css_to_file(css_content, css_file_path)
    
    return css_content

def write_css_to_file(css_content, file_path):
    try:
        with open(file_path, 'w') as f:
            f.write(css_content)
        print(f"CSS file written successfully to {file_path}")
    except Exception as e:
        print(f"Error writing CSS file: {str(e)}")

if __name__ == "__main__":
    # Example usage with array of filter files
    filter_files = [
        "rarity_magic.filter",
        "rarity_rare.filter",
        "amulets.filter",
        "currency.filter",
        # Add more filter files as needed
    ]
    
    filter_to_css(filter_files, "filter_styles.css")