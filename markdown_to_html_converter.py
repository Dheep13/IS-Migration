#!/usr/bin/env python3
"""
Enhanced Markdown to HTML Converter with Mermaid Diagram Support
Based on the logic from your existing md_to_html_with_mermaid.py
"""

import os
import sys
import argparse
import re
import markdown
from pathlib import Path
from datetime import datetime

def convert_markdown_to_html(markdown_file, output_file=None, custom_title=None):
    """
    Convert Markdown file to HTML with Mermaid support and enhanced styling.
    
    Args:
        markdown_file: Path to the markdown file
        output_file: Optional path for the output file. If not provided, 
                    will use the same filename with .html extension.
        custom_title: Optional custom title for the HTML document
    
    Returns:
        Path to the generated HTML file
    """
    # Validate input file
    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"Input file '{markdown_file}' not found")
    
    # Default output file
    if output_file is None:
        output_file = os.path.splitext(markdown_file)[0] + '_with_mermaid.html'
    
    # Read the markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    print(f"📖 Reading markdown file: {markdown_file}")
    print(f"📄 Content length: {len(markdown_content)} characters")
    
    # Find Mermaid code blocks and save them before markdown conversion
    mermaid_blocks = []
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    
    # Function to replace code blocks with placeholders
    def replace_mermaid(match):
        mermaid_blocks.append(match.group(1))
        return f'MERMAID_PLACEHOLDER_{len(mermaid_blocks) - 1}'
    
    # Replace Mermaid blocks with placeholders
    processed_markdown = re.sub(mermaid_pattern, replace_mermaid, markdown_content, flags=re.DOTALL)
    
    print(f"🎨 Found {len(mermaid_blocks)} Mermaid diagrams")
    
    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        processed_markdown,
        extensions=[
            'markdown.extensions.tables',      # Table support
            'markdown.extensions.fenced_code', # Code block support
            'markdown.extensions.codehilite',  # Syntax highlighting
            'markdown.extensions.toc',         # Table of contents
            'markdown.extensions.attr_list',   # Attribute lists
            'markdown.extensions.def_list',    # Definition lists
            'markdown.extensions.footnotes',   # Footnotes
            'markdown.extensions.md_in_html'   # Markdown in HTML
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight'
            },
            'markdown.extensions.toc': {
                'permalink': True
            }
        }
    )
    
    # Replace placeholders with Mermaid pre tags
    for i, block in enumerate(mermaid_blocks):
        placeholder = f'<p>MERMAID_PLACEHOLDER_{i}</p>'
        mermaid_html = f'<pre class="mermaid">\n{block}\n</pre>'
        html_content = html_content.replace(placeholder, mermaid_html)
        print(f"  ✅ Processed Mermaid diagram {i + 1}")
    
    # Determine document title
    if custom_title:
        doc_title = custom_title
    else:
        # Try to extract title from first H1 in content
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content)
        if title_match:
            doc_title = re.sub(r'<[^>]+>', '', title_match.group(1))  # Remove HTML tags
        else:
            doc_title = os.path.splitext(os.path.basename(markdown_file))[0]
    
    # Create the complete HTML document with enhanced styling
    final_html = create_html_template(html_content, doc_title)
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ HTML file generated successfully: {output_file}")
    print(f"🌐 You can open {output_file} in your browser to view the documentation")
    return output_file

def create_html_template(content, title):
    """Create the complete HTML template with styling and Mermaid support"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* Base Styles */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fafafa;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: #1565c0;
            margin-top: 2em;
            margin-bottom: 1em;
        }}
        
        h1 {{
            border-bottom: 3px solid #1565c0;
            padding-bottom: 10px;
        }}
        
        h2 {{
            border-bottom: 2px solid #42a5f5;
            padding-bottom: 5px;
        }}
        
        /* Code Blocks */
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            border-left: 4px solid #1565c0;
            margin: 20px 0;
        }}
        
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        }}
        
        /* Mermaid Diagrams */
        pre.mermaid {{
            text-align: center;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }}
        
        th {{
            background-color: #1565c0;
            color: white;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e3f2fd;
        }}
        
        /* Special Content Boxes */
        .note {{
            background: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #1565c0;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .insights {{
            background: #f3e5f5;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #9c27b0;
        }}
        
        .best-practices {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #4caf50;
        }}
        
        .security {{
            background: #ffebee;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #f44336;
        }}
        
        .warning {{
            background: #fff3e0;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #ff9800;
        }}
        
        /* Links */
        a {{
            color: #1565c0;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
            color: #0d47a1;
        }}
        
        /* Lists */
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid #1565c0;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            font-style: italic;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            table {{
                font-size: 14px;
            }}
            
            pre {{
                padding: 10px;
                font-size: 14px;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            body {{
                background: white;
                color: black;
            }}
            
            pre.mermaid {{
                border: 1px solid #ccc;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
    
    <!-- Mermaid.js for diagram rendering -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: false,
                htmlLabels: true,
                curve: 'basis'
            }},
            sequence: {{
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35
            }},
            gantt: {{
                titleTopMargin: 25,
                barHeight: 20,
                fontFamily: '"Open-Sans", "sans-serif"',
                fontSize: 11,
                gridLineStartPadding: 35,
                bottomPadding: 25,
                leftPadding: 75,
                rightPadding: 35
            }}
        }});
    </script>
    
    <!-- Footer -->
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 14px;">
        <p>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')} | Powered by Python Markdown + Mermaid.js</p>
    </footer>
</body>
</html>"""

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description='Convert Markdown to HTML with Mermaid diagram support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python markdown_to_html_converter.py -i document.md
  python markdown_to_html_converter.py -i document.md -o output.html
  python markdown_to_html_converter.py -i document.md -o output.html -t "My Custom Title"
        """
    )
    
    parser.add_argument('--input', '-i', required=True, 
                       help='Input markdown file path')
    parser.add_argument('--output', '-o', 
                       help='Output HTML file path (optional)')
    parser.add_argument('--title', '-t', 
                       help='Custom title for the HTML document (optional)')
    
    args = parser.parse_args()
    
    print("🚀 Markdown to HTML Converter with Mermaid Support")
    print("=" * 60)
    
    try:
        # Convert markdown to HTML
        html_file = convert_markdown_to_html(args.input, args.output, args.title)
        
        print("=" * 60)
        print("🎉 Conversion completed successfully!")
        print(f"📁 Input:  {args.input}")
        print(f"📁 Output: {html_file}")
        print(f"🌐 Open the HTML file in your browser to view the rendered documentation")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
