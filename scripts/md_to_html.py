#!/usr/bin/env python3
"""
Convert markdown briefing to styled HTML.
Usage: ./md_to_html.py input.md output.html
"""

import re
import sys
from pathlib import Path

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{title}</title>
    <style>
        @charset "UTF-8";
        :root {{
            --primary: #0066cc;
            --primary-dark: #0052a3;
            --bg: #f8f9fa;
            --card-bg: #ffffff;
            --text: #333333;
            --text-secondary: #666666;
            --border: #e1e4e8;
            --code-bg: #f6f8fa;
            --warning: #f59e0b;
        }}
        
        * {{ box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 40px 20px;
            color: var(--text);
            line-height: 1.7;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: rgba(255,255,255,0.9);
            text-decoration: none;
            margin-bottom: 24px;
            font-size: 0.95em;
            transition: all 0.2s;
        }}
        
        .back-link:hover {{
            color: white;
            transform: translateX(-4px);
        }}
        
        .content {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 1.8em;
            margin: 0 0 16px 0;
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
            padding-bottom: 12px;
        }}
        
        h2 {{
            font-size: 1.4em;
            margin: 32px 0 16px 0;
            color: var(--primary-dark);
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        h3 {{
            font-size: 1.15em;
            margin: 24px 0 12px 0;
            color: var(--text);
            padding-left: 12px;
            border-left: 4px solid var(--primary);
        }}
        
        blockquote {{
            margin: 16px 0;
            padding: 16px 20px;
            background: linear-gradient(135deg, #f0f7ff 0%, #e8f4ff 100%);
            border-radius: 8px;
            border-left: 4px solid var(--primary);
        }}
        
        blockquote p {{
            margin: 0;
            color: var(--text-secondary);
            font-size: 0.95em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
        }}
        
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        th {{
            background: #f6f8fa;
            font-weight: 600;
            color: var(--text);
        }}
        
        tr:hover {{
            background: #f9fafb;
        }}
        
        ul {{
            padding-left: 24px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        code {{
            background: var(--code-bg);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 0.9em;
        }}
        
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
            margin: 32px 0;
        }}
        
        .tag {{
            display: inline-block;
            padding: 2px 8px;
            background: var(--primary);
            color: white;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        @media (max-width: 600px) {{
            body {{ padding: 20px 16px; }}
            .content {{ padding: 24px; }}
            h1 {{ font-size: 1.5em; }}
            h2 {{ font-size: 1.2em; }}
            table {{ font-size: 0.9em; }}
            th, td {{ padding: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="./index.html" class="back-link">← 返回首页</a>
        <div class="content">
{content}
        </div>
    </div>
</body>
</html>'''

def markdown_to_html(md_text: str) -> str:
    """Simple markdown to HTML converter"""
    html = md_text
    
    # Extract title from first h1
    title_match = re.search(r'^#\s+(.+)$', html, re.MULTILINE)
    title = title_match.group(1) if title_match else "AI Briefing"
    
    # Headers
    html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Blockquote
    html = re.sub(r'^\>\s+(.+)$', r'<blockquote><p>\1</p></blockquote>', html, flags=re.MULTILINE)
    
    # Links
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # Code
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Tables (simple conversion)
    lines = html.split('\n')
    result = []
    in_table = False
    table_lines = []
    
    for line in lines:
        if '|' in line and not in_table:
            in_table = True
            table_lines = [line]
        elif '|' in line and in_table:
            table_lines.append(line)
        elif in_table:
            # Process table
            result.append(convert_table(table_lines))
            in_table = False
            table_lines = []
            if line.strip():
                result.append(line)
        else:
            result.append(line)
    
    if in_table:
        result.append(convert_table(table_lines))
    
    html = '\n'.join(result)
    
    # Horizontal rule
    html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)
    
    # Lists (simple)
    html = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Wrap consecutive li in ul
    html = re.sub(r'(<li>.+</li>\n)+', r'<ul>\g<0></ul>', html)
    
    # Paragraphs
    paragraphs = []
    for block in html.split('\n\n'):
        block = block.strip()
        if block and not block.startswith('<') and not block.startswith('---'):
            block = f'<p>{block}</p>'
        paragraphs.append(block)
    
    html = '\n\n'.join(paragraphs)
    
    return title, html

def convert_table(lines: list) -> str:
    """Convert markdown table to HTML"""
    rows = []
    for line in lines:
        if '---' in line:
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells:
            rows.append(cells)
    
    if not rows:
        return ''
    
    html = '<table>\n'
    # Header
    html += '  <tr>' + ''.join(f'<th>{c}</th>' for c in rows[0]) + '</tr>\n'
    # Body
    for row in rows[1:]:
        html += '  <tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>\n'
    html += '</table>'
    
    return html

def main():
    if len(sys.argv) < 3:
        print("Usage: ./md_to_html.py input.md output.html")
        return 1
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return 1
    
    md_text = input_file.read_text(encoding='utf-8')
    title, html_content = markdown_to_html(md_text)
    
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)
    
    output_file.write_text(full_html, encoding='utf-8')
    print(f"Converted: {input_file} -> {output_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
