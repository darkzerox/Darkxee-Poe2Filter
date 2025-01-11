import os

# Get directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent directory of script)
project_path = os.path.dirname(script_dir)
# Path to filter_group directory
filter_group_path = os.path.join(project_path, "dzx_filter", "filter_group")

def filter_to_css(filter_paths, output_file_name):
    css_output = []
    
    # Helper function to process a block of filter rules
    def process_block(rules):
        if not rules:
            return None
            
        selectors = []
        properties = {}
        
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
                
        if selectors and properties:
            # Combine selectors and create CSS rule
            selector_str = ', '.join(selectors)
            properties_str = ';\n    '.join([f'{k}: {v}' for k, v in properties.items()])
            return f'{selector_str} {{\n    {properties_str};\n}}'
        
        return None

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
        "amulets.filter"
        # Add more filter files as needed
    ]
    
    filter_to_css(filter_files, "filter_styles.css")