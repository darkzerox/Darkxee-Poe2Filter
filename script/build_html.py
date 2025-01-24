import os

# Get directory of current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root (parent directory of script)
project_path = os.path.dirname(script_dir)

def filter_to_html_table(filter_path, preview_tags):
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
                'Quality': None,
                'ItemLevel': None
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
                        color_part = parts[2]
                        # If it's a named color, use it as a class
                        if color_part.title() in ['Red', 'Green', 'Blue', 'Brown', 'White', 
                                                'Yellow', 'Cyan', 'Grey', 'Orange', 'Pink', 'Purple']:
                            block_data['minimap_color'] = color_part.lower()
                        else:
                            # For RGB values, use inline style
                            block_data['minimap_color'] = f'rgb({color_part})'
        
            elif parts[0] == 'AreaLevel':
                block_data['conditions']['AreaLevel'] = ' '.join(parts[1:])
            elif parts[0] == 'DropLevel':
                block_data['conditions']['DropLevel'] = ' '.join(parts[1:])
            elif parts[0] == 'Sockets':
                block_data['conditions']['Sockets'] = ' '.join(parts[1:])
            elif parts[0] == 'Quality':
                block_data['conditions']['Quality'] = ' '.join(parts[1:])
            elif parts[0] == 'ItemLevel':
                block_data['conditions']['ItemLevel'] = ' '.join(parts[1:])

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
    
    # Modified row generation to collect preview tags
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
        if block_data['conditions']['ItemLevel']:
            conditions.append(f"iLvl: {block_data['conditions']['ItemLevel']}")
        
        condition_text = ', '.join(conditions) if conditions else 'Any'
        html_output.append(f'  <td>{condition_text}</td>')
        # Icon column with color
        if block_data["minimap_icon"]:
            icon_class = f'minimap-icon-{block_data["minimap_icon"]}'
            if block_data["minimap_color"]:
                if block_data["minimap_color"].startswith('rgb'):
                    # RGB value - use inline style
                    html_output.append(f'  <td><span class="{icon_class}" style="color: {block_data["minimap_color"]}">{block_data["minimap_icon"]}</span></td>')
                else:
                    # Named color - use color class
                    html_output.append(f'  <td><span class="{icon_class} minimap-icon-{block_data["minimap_color"]}">{block_data["minimap_icon"]}</span></td>')
            else:
                html_output.append(f'  <td><span class="{icon_class}">{block_data["minimap_icon"]}</span></td>')
        else:
            html_output.append(f'  <td>-</td>')
        # Preview column - use first non-empty value or "ALL"
        preview_text = block_data['base_types'][0] if block_data['base_types'] else \
                      block_data['classes'][0] if block_data['classes'] else "ALL"
        truncated_name = preview_text[:10] + '...' if len(preview_text) > 10 else preview_text
        html_output.append(f'  <td><div class="style-box" style="{style_str}">{truncated_name}</div></td>')
        html_output.append(f'</tr>')
        
        # Add to preview tags set
        preview_tags.add((preview_text, style_str))

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

    # Create set for preview tags
    preview_tags = set()

    # Generate tables for each filter file
    tables_html = []
    for filter_name in filter_array:
        filter_path = os.path.join(project_path, 'dzx_filter', 'filter_group', filter_name)
        table_html = filter_to_html_table(filter_path, preview_tags)
        if table_html:
            tables_html.append(table_html)

    # Generate tag cloud HTML with floating animations
    tag_cloud_html = """
    <style>
        @keyframes fadeInScale {
            0% {
                opacity: 0;
                transform: scale(0.5) translateY(20px);
            }
            100% {
                opacity: 1;
                transform: scale(1) translateY(0);
            }
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        .tag-cloud .tag {
            display: inline-block;
            padding: 5px 15px;
            margin: 5px;
            border-radius: 20px;
            font-size: 14px;
            transition: all 0.3s ease;
            animation: 
                fadeInScale 0.5s ease backwards,
                float 3s ease-in-out infinite;
            cursor: pointer;
            position: relative;
        }
        
        .tag-cloud .tag:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            animation-play-state: paused;
        }
    </style>
    <h2>Preview Items</h2>
    <div class="tag-cloud">
    """
    
    # Add each unique preview tag with staggered animation and different float durations
    for index, (tag_text, style) in enumerate(preview_tags):
        # Clean up the tag text
        clean_tag = tag_text[:20]  # Limit length
        if len(tag_text) > 20:
            clean_tag += '...'
            
        # Calculate staggered delay and randomized float duration
        delay = index * 0.05  # 50ms delay between each tag
        float_duration = 3 + (index % 3)  # Varies between 3-5s
        float_offset = (index * 33) % 100  # Offset float animation start
            
        # Add the tag with animation delay and original style
        tag_cloud_html += f"""
        <span class="tag" style="
            {style};
            animation: 
                fadeInScale 0.5s ease backwards {delay}s,
                float {float_duration}s ease-in-out infinite {float_offset}%;
        ">{clean_tag}</span>
        """
    
    tag_cloud_html += "</div>"

    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DZX Poe2 Filter</title>
    <meta name="description" content="DZX Poe2 Filter สำหรับกรอง Item จากเกม Path of Exile 2">
    <meta property="og:title" content="DZX Poe2 Filter">
    <meta property="og:description" content="DZX Poe2 Filter สำหรับกรอง Item จากเกม Path of Exile 2">
    <meta property="og:image" content="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png">
    <meta property="og:url" content="https://darkzerox.github.io/Darkxee-Poe2Filter/">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="DZX Poe2 Filter">
    <style>
        @font-face {{   
            font-family: 'Fontin';
            src: url('https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/fonts/Fontin-Regular.ttf') format('truetype');
        }}
        body {{
            font-family: Fontin, Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #1a1a1a;
            color: #ffffff;
        }}
        a {{
            color: #f17d40;
            text-decoration: none;
        }}
        a:hover {{
            color: #ff4a4a;
            text-decoration: underline;
        }}
        .download-button {{
            border: solid 1px #f17d40;
            padding: 10px 20px;
            background: #f17d40;
            color: #fff;
            border-radius: 10px;
            text-decoration: none;
            margin: 30px;
            display: inline-block;
        }}
        .download-button:hover {{
            background: #ff4a4a;
            border: solid 1px #ff4a4a;
            text-decoration: none;
            color: #fff;
        }}
        .filter-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background-color: #2d2d2d;
        }}
        .filter-table th, .filter-table td {{
            padding: 8px;
            text-align: center;
            border: 1px solid #666;
        }}
        .filter-table tr td:nth-child(2) {{
            text-align: left;
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
        .tag-cloud .tag {{
            display: inline-block;
            padding: 5px 15px;
            margin: 5px;
            border-radius: 20px;
            font-size: 14px;
            transition: all 0.3s ease;
            animation: 
                fadeInScale 0.5s ease backwards,
                float 3s ease-in-out infinite;
            cursor: pointer;
            position: relative;
            color: rgb(255 209 94); border-color: rgb(255 209 94); background-color: rgb(34 34 34); font-size: 17px;
            animation: 
                fadeInScale 0.5s ease backwards 0.0s,
                float 3s ease-in-out infinite 0%;
        }}
        
        .tag-cloud .tag:hover {{
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            animation-play-state: paused;
        }}
        .tag-cloud{{
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background: #2d2d2d;
            border-radius: 10px;
            min-height: 200px;
        }}
        .dev-table{{
            background: #2e2e2e; padding: 5px; border-spacing: 15px;
        }}
        {css_content}

    </style>

    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-P8JFCCZC');</script>
    <!-- End Google Tag Manager -->

</head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JNBFDR6WBY"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
    
  gtag('config', 'G-JNBFDR6WBY');
</script>


<body>

    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-P8JFCCZC"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->

    <div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png">
    <img alt="Darkxee Poe2 Filter" src="https://raw.githubusercontent.com/darkzerox/Darkxee-Poe2Filter/refs/heads/master/dzx_filter/images/dzx-poe2-filter-logo.png" width="800" style="max-width: 100%">
  </picture>

  <h1 align="center">DZX Poe2 Filter</h1>
  
  <p>
    เป็นโปรเจคที่ทำขึ้นสำหรับกรอง Item จากเกม ซึ่งตอนนี้ poe2 ยังไม่รองรับ Function Import<br/>
    ดังนั้นจึงต้องใช้วิธีการรวมไฟล์โดยใช้ Python เข้ามาช่วย
  </p>

  <div class="badges">
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases">
      <img src="https://img.shields.io/github/v/release/darkzerox/Darkxee-Poe2Filter" alt="GitHub Release">
    </a>
    <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/actions">
      <img src="https://img.shields.io/github/actions/workflow/status/darkzerox/Darkxee-Poe2Filter/python-app.yml" alt="Build Status">
    </a>
  </div>
</div>

<h2 align="center">📥 ดาวน์โหลด</h2>

<div align="center">
  <a href="https://github.com/darkzerox/Darkxee-Poe2Filter/releases/latest">
    <img src="https://img.shields.io/badge/💻_Download-PC-blue?style=for-the-badge&logo=windows" alt="Download PC">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.pathofexile.com/account/view-profile/Darkxee-3892/item-filters">
    <img src="https://img.shields.io/badge/🎮_Download-PS5-blue?style=for-the-badge&logo=playstation" alt="Download PS5">
  </a>
</div>

<h2>🔧 วิธีติดตั้ง</h2>

<p>แตกไฟล์และคัดลอกไฟล์ทั้งหมดไปไว้ที่:</p>

  <summary>
    <img src="https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows" alt="Windows">
  </summary>
  <pre><code>%userprofile%\Documents\My Games\Path of Exile 2</code></pre>

  <summary>
    <img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux">
  </summary>
  <pre><code>steamapps/compatdata/2694490/pfx/drive_c/users/steamuser/My Documents/My Games/Path of Exile 2</code></pre>

  <summary>
    <img src="https://img.shields.io/badge/🎮_-PS5-blue?style=flat&logo=playstation&logoColor=white" alt="Ps5 Xbox">
  </summary>
  <pre><code><a href="https://www.pathofexile.com/account/view-profile/Darkxee-3892/item-filters">PS5 XBox กดเข้าลิ๊งนี้</a> แล้วกด Follow ทั้งสองอันได้เลย</code></pre>

    <h2>👨‍💻 สำหรับนักพัฒนา</h2>

    <p>สามารถ <a href="https://github.com/darkzerox/Darkxee-Poe2Filter">Clone โปรเจค</a> ไปแก้ไขได้เลย</p>

    <h3>📂 โครงสร้างโปรเจค</h3>

    <table class="dev-table">
    <tr>
        <th>โฟลเดอร์/ไฟล์</th>
        <th>รายละเอียด</th>
    </tr>
    <tr>
        <td>📁 filter_group/</td>
        <td>ไฟล์ filter หลักแยกตามหมวดหมู่</td>
    </tr>
    <tr>
        <td>📁  dzx_filter/soundeffect/</td>
        <td>ไฟล์เสียงทั้งหมด</td>
    </tr>
    <tr>
        <td>📄 script/start_build.py</td>
        <td>สคริปต์สำหรับรวมไฟล์ filter</td>
    </tr>
    </table>

    <blockquote>
    <p>💡 Filter นี้จะมีการอัพเดตอย่างสม่ำเสมอ กรุณาติดตามการอัพเดตด้วยนะ</p>
    </blockquote>

    <h2>🙏 เครดิต</h2>

    <div>
    <a href="https://github.com/NeverSinkDev/NeverSink-PoE2litefilter">
        <img src="https://img.shields.io/badge/Original_Filter-NeverSink's_Indepth_Loot_Filter-orange?style=for-the-badge" alt="NeverSink's Filter">
    </a>
    </div>

    <p>Style ต่างๆจะใช้ของต้นฉบับจาก NeverSink's เพื่อความสะดวกและคุ้นเคย อาจจะมีปรับปรุงเพิ่มเติมเล็กน้อย</p>


    <hr/>

    {tag_cloud_html}

    <h2>Filter Group Preview</h2>
    {' '.join(tables_html)}
</body>
</html>"""

    # Fix escape sequence warning by using raw string for HTML content
    return html_content.replace('\\', r'\\')

def write_html_to_file(array_path, output_file_name="index.html"):
    html_content = generate_html_content(array_path)
    if html_content is None:
        return False

    # Create output directory if it doesn't exist
    html_dir = os.path.join(project_path)
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
    ]
    write_html_to_file(demo_array, "index.html")
