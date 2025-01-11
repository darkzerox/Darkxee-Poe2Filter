import os

# Get directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent directory of script)
project_path = os.path.dirname(script_dir)

def filter_to_html_table(filter_path):
    try:
        with open(filter_path, 'r') as f:
            filter_content = f.read()
    except Exception as e:
        print(f"Error reading filter file {filter_path}: {str(e)}")
        return None

    html_output = []
    current_block = []
    
    def process_block(rules):
        if not rules:
            return None
            
        block_data = {
            'classes': [],
            'base_types': [],
            'rarity': None,
            'minimap_icon': None,
            'minimap_color': None,
            'conditions': {
                'AreaLevel': None,
                'DropLevel': None,
                'Sockets': None,
                'Quality': None
            },
            'styles': {
                'color': 'rgb(255 255 255)',  # Default white text color
                'border-color': None,
                'background-color': None,
                'font-size': None
            }
        }
        
        # Map for minimap icons to ASCII
        icon_map = {
            'Circle': '○',
            'Diamond': '◇',
            'Hexagon': '⬡',
            'Square': '□',
            'Star': '★',
            'Triangle': '△',
            'Cross': '✗',
            'Moon': '☾',
            'Raindrop': '❧',
            'Pentagon': '⬠',
        }
        
        for rule in rules:
            rule = rule.strip()
            if not rule or rule.startswith('#'):
                continue
                
            parts = rule.split()
            if not parts:
                continue
                
            if parts[0] == 'Class':
                classes = ' '.join(parts[1:]).replace('"', '')
                cleaned_classes = [item.strip().replace('==', '').replace('>=', '')
                                 .replace('<=', '').replace('=', '').strip() 
                                 for item in classes.split(',')]
                block_data['classes'].extend(cleaned_classes)
                
            elif parts[0] == 'BaseType':
                types = ' '.join(parts[1:]).replace('"', '')
                cleaned_types = [item.strip().replace('==', '').replace('>=', '')
                               .replace('<=', '').replace('=', '').strip() 
                               for item in types.split(',')]
                block_data['base_types'].extend(cleaned_types)
                
            elif parts[0] == 'Rarity':
                rarity_value = ' '.join(parts[1:]).replace('"', '')
                cleaned_rarity = rarity_value.replace('==', '').replace('>=', '').replace('<=', '').replace('=', '').strip()
                block_data['rarity'] = cleaned_rarity

            elif parts[0] == 'SetTextColor':
                block_data['styles']['color'] = f'rgb({parts[1]} {parts[2]} {parts[3]})'
            elif parts[0] == 'SetBorderColor':
                block_data['styles']['border-color'] = f'rgb({parts[1]} {parts[2]} {parts[3]})'
            elif parts[0] == 'SetBackgroundColor':
                block_data['styles']['background-color'] = f'rgb({parts[1]} {parts[2]} {parts[3]})'
            elif parts[0] == 'SetFontSize':
                # Multiply font size by 1.5
                original_size = int(parts[1])
                adjusted_size = int(original_size * 0.5)
                block_data['styles']['font-size'] = f'{adjusted_size}px'

            elif parts[0] == 'MinimapIcon':
                # MinimapIcon Size Color Shape
                if len(parts) >= 4:
                    icon_shape = parts[3]
                    block_data['minimap_icon'] = icon_map.get(icon_shape, '●')
                    if len(parts) >= 3:  # Get color if specified
                        block_data['minimap_color'] = f'rgb({parts[2]})'
        
            elif parts[0] == 'AreaLevel':
                block_data['conditions']['AreaLevel'] = ' '.join(parts[1:])
            elif parts[0] == 'DropLevel':
                block_data['conditions']['DropLevel'] = ' '.join(parts[1:])
            elif parts[0] == 'Sockets':
                block_data['conditions']['Sockets'] = ' '.join(parts[1:])
            elif parts[0] == 'Quality':
                block_data['conditions']['Quality'] = ' '.join(parts[1:])

        # If we have any styles or rules, return the block
        if block_data['styles']['border-color'] is not None or \
           block_data['styles']['background-color'] is not None or \
           block_data['styles']['font-size'] is not None:
            # If no classes or base_types, add "ALL"
            if not block_data['classes'] and not block_data['base_types']:
                block_data['classes'].append("ALL")
            return block_data
        # If we have classes or base_types, return the block
        elif block_data['classes'] or block_data['base_types']:
            return block_data
        return None

    # Update table header
    html_output.append(f'<h3>{os.path.basename(filter_path)}</h3>')
    html_output.append('<table class="filter-table">')
    html_output.append('<tr><th>Class</th><th>BaseType</th><th>Rarity</th><th>Conditions</th><th>Icon</th><th>Preview</th></tr>')
    
    # Modified row generation
    def generate_row(block_data, style_str):
        html_output.append(f'<tr>')
        # Class column - show "ALL" if empty
        class_names = ', '.join(block_data['classes']) if block_data['classes'] else 'ALL'
        html_output.append(f'  <td>{class_names}</td>')
        # BaseType column - show "ALL" if empty
        base_types = ', '.join(block_data['base_types']) if block_data['base_types'] else 'ALL'
        html_output.append(f'  <td>{base_types}</td>')
        # Rarity column
        html_output.append(f'  <td>{block_data["rarity"] or "Any"}</td>')
        # Conditions column
        conditions = []
        if block_data['conditions']['AreaLevel']:
            conditions.append(f"Area: {block_data['conditions']['AreaLevel']}")
        if block_data['conditions']['DropLevel']:
            conditions.append(f"iLvl: {block_data['conditions']['DropLevel']}")
        if block_data['conditions']['Sockets']:
            conditions.append(f"Sock: {block_data['conditions']['Sockets']}")
        if block_data['conditions']['Quality']:
            conditions.append(f"Qual: {block_data['conditions']['Quality']}")
        
        condition_text = ', '.join(conditions) if conditions else 'Any'
        html_output.append(f'  <td>{condition_text}</td>')
        # Icon column with color
        icon_style = f'color: {block_data["minimap_color"]}' if block_data["minimap_color"] else ''
        html_output.append(f'  <td><span style="{icon_style}">{block_data["minimap_icon"] or "-"}</span></td>')
        # Preview column - use first non-empty value or "ALL"
        preview_text = block_data['classes'][0] if block_data['classes'] else \
                      block_data['base_types'][0] if block_data['base_types'] else "ALL"
        truncated_name = preview_text[:10] + '...' if len(preview_text) > 10 else preview_text
        html_output.append(f'  <td><div class="style-box" style="{style_str}">{truncated_name}</div></td>')
        html_output.append(f'</tr>')

    # Process blocks
    for line in filter_content.split('\n'):
        line = line.strip()
        
        # Start new block on Show/Hide or empty/comment lines
        if line.startswith('Show') or line.startswith('Hide') or not line or line.startswith('#'):
            if current_block:
                block_data = process_block(current_block)
                if block_data:
                    style_str = '; '.join([f'{k}: {v}' for k, v in block_data['styles'].items() if v])
                    if is_hidden:
                        style_str += '; text-decoration: line-through'
                    generate_row(block_data, style_str)
            # Reset for new block
            current_block = []
            if line.startswith('Show') or line.startswith('Hide'):
                is_hidden = line.startswith('Hide')
            continue
            
        # Add line to current block
        current_block.append(line)
    
    # Process final block
    if current_block:
        block_data = process_block(current_block)
        if block_data:
            style_str = '; '.join([f'{k}: {v}' for k, v in block_data['styles'].items() if v])
            if is_hidden:
                style_str += '; text-decoration: line-through'
            generate_row(block_data, style_str)
    
    html_output.append('</table>')
    return '\n'.join(html_output)

def generate_html_content(filter_array):
    # Read CSS file
    css_path = os.path.join(project_path, 'dzx_filter', 'css', 'filter_styles.css')
    try:
        with open(css_path, 'r') as f:
            css_content = f.read()
    except Exception as e:
        print(f"Error reading CSS file: {str(e)}")
        return None

    # Generate tables for each filter file
    tables_html = []
    for filter_name in filter_array:
        filter_path = os.path.join(project_path, 'dzx_filter', 'filter_group', filter_name)
        table_html = filter_to_html_table(filter_path)
        if table_html:
            tables_html.append(table_html)

    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DZX Filter Preview</title>
    <style>
        @font-face {{   
            font-family: 'Fontin';
            src: url('./fonts/Fontin-Regular.ttf') format('truetype');
        }}
        body {{
            font-family: Fontin, Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #1a1a1a;
            color: #ffffff;
        }}
        .filter-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background-color: #2d2d2d;
        }}
        .filter-table th, .filter-table td {{
            padding: 8px;
            text-align: left;
            border: 1px solid #666;
        }}
        .filter-table th {{
            background-color: #4a9eff;
            color: white;
        }}
        .style-box {{
            padding: 5px 10px;
            display: inline-block;
            border: 2px solid #666;
            background-color: #333;
        }}
        h1,h2,h3,h4{{
            color: #4a9eff;
        }}
        {css_content}
    </style>
</head>
<body>
    <div style="display: flex;justify-content: center;flex-direction: column;align-items: center;"><img src="./css/logo.png" alt="Darkxee Poe2 Filter">
    <h1>Darkxee Poe2 Filter </h1>
    </div>
   

    <p>เป็นโปรเจคที่ทำขึ้นสำหรับกรอง Item จากเกม ซึ่งตอนนี้ poe2 ยังไม่รองรับ Function Import ดังนั้นจึงต้องใช้วิธีการรวมไฟล์โดยใช้ Python เข้ามาช่วย</p>

    <h2>Badges</h2>
    <ul>
        <li><img src="https://img.shields.io/github/v/release/darkzerox/Darkxee-Poe2Filter" alt="GitHub Release"></li>
        <li><img src="https://img.shields.io/github/actions/workflow/status/darkzerox/Darkxee-Poe2Filter/python-app.yml" alt="GitHub Actions Workflow Status"></li>
    </ul>

    <h2><a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest" style="
    border: solid 1px #ddd;
    padding: 10px 20px;
    background: blueviolet;
    color: #fff;
    border-radius: 10px;
    text-decoration: none;
    margin: 30px;
    display: inline-block;
    ">🔗 Download</a></h2>

    <h2>Installation</h2>
    <p>แตกไฟล์และคัดลอกไฟล์ทั้งหมดไปไว้ที่</p>

    <h4>Windows:</h4>
    <pre><code>%userprofile%\Documents\My Games\Path of Exile 2</code></pre>

    <h4>Linux:</h4>
    <pre><code>steamapps/compatdata/2694490/pfx/drive_c/users/steamuser/My Documents/My Games/Path of Exile 2</code></pre>

    <h2>How to work</h2>

    <h4>filter จะมี 3 ประเภท ให้เลือกใช้ตามช่วงเวลาที่เล่น</h4>
    <ul>
        <li><strong>dzx.filter</strong> จะแสดงไอเท็มทั้งหมด</li>
        <li><strong>dzx-hide-white.filter</strong> จะซ่อนของสีขาว แต่จะยังคงแสดงของที่มีรู และของที่ย่อยได้</li>
        <li><strong>dzx-hide-white-blue.filter</strong> จะซ่อนของสีขาว และสีฟ้า แต่จะยังคงแสดงของที่มีรู และของที่ย่อยได้</li>
    </ul>

    <h3>For Dev</h3>
    <ul>
        <li>สำหรับท่านที่ต้องการแก้ไข Filter นี้ สามารถ Clone ไปแก้ไขได้เลย</li>
        <li>ไฟล์หลักจะอยู่ใน Folder <strong>filter_group</strong> ซึ่งได้แบ่งเป็นหมวดหมู่ต่างๆเอาไว้แล้ว เพื่อง่ายต่อการแก้ไข</li>
        <li>ไฟล์เสียงจะอยู่ใน Folder <strong>dzx_filter/soundeffect</strong></li>
        <li>เมื่อแก้ไขไฟล์เสร็จแล้วให้ run ไฟล์ <strong>run_script.py</strong> เพื่อทำการรวมไฟล์ใหม่อีกครั้ง</li>
        <li>ใช้ภาษา python นะ</li>
    </ul>

    <blockquote>
        <p>filter นี้จะพยายามอัพเดตอยู่ตลอด ดังนั้นแล้วให้เข้ามาดูบ่อยๆนะ</p>
    </blockquote>

    <h2>Github Repo</h2>
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter">https://github.com/darkzerox/Darkxee-Poe2Filter</a>

    <h2>credit</h2>
    <p>Thank you for Original filter from NeverSink's Indepth Loot Filter <a href="https://github.com/NeverSinkDev/NeverSink-PoE2litefilter">https://github.com/NeverSinkDev/NeverSink-PoE2litefilter</a></p>
    <p>Style ต่างๆจะใช้ของต้นฉบับจาก NeverSink's เพื่อความสะดวกและคุ้นเคย</p>
    <hr/>

     <h2>Filter Group Preview</h2>
    {' '.join(tables_html)}
</body>
</html>"""

    return html_content

def write_html_to_file(array_path, output_file_name="index.html"):
    html_content = generate_html_content(array_path)
    if html_content is None:
        return False

    # Create output directory if it doesn't exist
    html_dir = os.path.join(project_path, 'dzx_filter')
    os.makedirs(html_dir, exist_ok=True)

    # Write HTML file
    output_path = os.path.join(html_dir, output_file_name)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML preview generated successfully at {output_path}")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {str(e)}")
        return False

if __name__ == "__main__":
    demo_array = [
        "rarity_rare.filter",
        "salvage.filter",
        "hide_rarity_rare.filter"
    ]
    write_html_to_file(demo_array, "index.html")
