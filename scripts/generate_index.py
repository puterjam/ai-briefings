#!/usr/bin/env python3
"""
Generate styled index.html for AI Briefings Pages.
Usage: python generate_index.py <output_dir>
"""

import os
import sys
from datetime import datetime
from pathlib import Path

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily Briefing - AI 动态简报</title>
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
            --shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        * {{ box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 40px 20px;
            color: var(--text);
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin: 0 0 10px 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
            margin: 0;
        }}
        
        .stats-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-size: 1.2em;
        }}
        
        .stats-card .emoji {{ font-size: 1.5em; }}
        .stats-card .number {{
            font-weight: bold;
            color: var(--primary);
            font-size: 1.3em;
        }}
        
        .briefing-list {{
            background: var(--card-bg);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow);
        }}
        
        .briefing-list h2 {{
            margin: 0;
            padding: 24px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            font-size: 1.3em;
        }}
        
        .briefing-item {{
            display: flex;
            align-items: center;
            padding: 18px 24px;
            border-bottom: 1px solid var(--border);
            transition: all 0.2s ease;
            text-decoration: none;
            color: var(--text);
        }}
        
        .briefing-item:last-child {{ border-bottom: none; }}
        
        .briefing-item:hover {{
            background: #f6f8fa;
            transform: translateX(4px);
        }}
        
        .briefing-item .date {{
            font-weight: 600;
            color: var(--primary);
            min-width: 110px;
            font-size: 1.1em;
        }}
        
        .briefing-item .arrow {{
            margin-left: auto;
            color: var(--text-secondary);
            font-size: 1.2em;
        }}
        
        .briefing-item:hover .arrow {{
            color: var(--primary);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: rgba(255,255,255,0.7);
            font-size: 0.9em;
        }}
        
        @media (max-width: 600px) {{
            body {{ padding: 20px 16px; }}
            .header h1 {{ font-size: 2em; }}
            .briefing-item {{ padding: 16px 20px; }}
            .briefing-item .date {{ min-width: 90px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Daily Briefing</h1>
            <p>每日 AI 动态简报归档</p>
        </div>
        
        <div class="stats-card">
            <span class="emoji">📊</span>
            <span>共收录</span>
            <span class="number">{count}</span>
            <span>篇简报</span>
        </div>
        
        <div class="briefing-list">
            <h2>📅 简报列表</h2>
            {items}
        </div>
        
        <div class="footer">
            <p>最后更新: {update_time} · 由 ai-daily-briefing skill 自动生成</p>
        </div>
    </div>
</body>
</html>'''

def generate_index(output_dir: str):
    """Generate styled index.html"""
    site_dir = Path(output_dir)
    
    # Find all HTML files except index.html
    html_files = sorted([f for f in site_dir.glob("*.html") if f.name != "index.html"])
    
    # Generate list items
    items_html = ""
    for f in reversed(html_files):  # Newest first
        date = f.stem
        items_html += f'''            <a href="{date}.html" class="briefing-item">
                <span class="date">{date}</span>
                <span class="arrow">→</span>
            </a>\n'''
    
    if not items_html:
        items_html = '<div style="padding: 24px; text-align: center; color: #666;">暂无简报</div>'
    
    # Fill template
    html = HTML_TEMPLATE.format(
        count=len(html_files),
        items=items_html,
        update_time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    # Write file
    output_file = site_dir / "index.html"
    output_file.write_text(html, encoding='utf-8')
    print(f"Generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_index.py <output_dir>")
        sys.exit(1)
    
    generate_index(sys.argv[1])
