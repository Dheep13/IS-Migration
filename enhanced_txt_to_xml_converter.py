#!/usr/bin/env python3
"""
Enhanced script to convert all .txt files in boomi-api folder to .xml files
Handles different content types intelligently
"""

import os
import re
import json
from datetime import datetime
from xml.sax.saxutils import escape

def is_already_xml(content):
    """Check if content is already in XML format"""
    stripped = content.strip()
    return stripped.startswith('<?xml') or stripped.startswith('<')

def is_json_content(content):
    """Check if content looks like JSON"""
    stripped = content.strip()
    return (stripped.startswith('{') and stripped.endswith('}')) or \
           (stripped.startswith('[') and stripped.endswith(']'))

def detect_content_type(content, filename):
    """Detect the type of content in the file"""
    if is_already_xml(content):
        return "xml"
    elif is_json_content(content):
        return "json"
    elif "Connection" in filename and any(keyword in content for keyword in ["bootstrap_servers", "oauth", "security_protocol"]):
        return "connection_config"
    elif "Mapping" in filename and "fromKey" in content:
        return "mapping_config"
    elif any(keyword in content.lower() for keyword in ["process", "step", "connector", "action"]):
        return "process_guide"
    else:
        return "text"

def convert_connection_config_to_xml(content, filename):
    """Convert connection configuration to structured XML"""
    base_name = os.path.splitext(filename)[0]
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<boomi-connection-config>
    <metadata>
        <name>{escape(base_name)}</name>
        <type>Connection Configuration</type>
        <converted_date>{datetime.now().isoformat()}</converted_date>
        <source_file>{escape(filename)}</source_file>
    </metadata>
    
    <configuration>
        <raw_content><![CDATA[{content}]]></raw_content>
    </configuration>
</boomi-connection-config>'''
    
    return xml_content

def convert_mapping_config_to_xml(content, filename):
    """Convert mapping configuration to structured XML"""
    base_name = os.path.splitext(filename)[0]
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<boomi-mapping-config>
    <metadata>
        <name>{escape(base_name)}</name>
        <type>Mapping Configuration</type>
        <converted_date>{datetime.now().isoformat()}</converted_date>
        <source_file>{escape(filename)}</source_file>
    </metadata>
    
    <mapping_details>
        <raw_content><![CDATA[{content}]]></raw_content>
    </mapping_details>
</boomi-mapping-config>'''
    
    return xml_content

def convert_process_guide_to_xml(content, filename):
    """Convert process guide to structured XML"""
    base_name = os.path.splitext(filename)[0]
    
    # Try to extract sections
    lines = content.split('\n')
    sections = []
    current_section = {"title": "Introduction", "content": []}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this looks like a section header
        if (line.isupper() and len(line) > 5) or \
           (line.endswith(':') and len(line.split()) <= 5) or \
           line.startswith('#'):
            if current_section["content"]:
                sections.append(current_section)
            current_section = {"title": line.rstrip(':'), "content": []}
        else:
            current_section["content"].append(line)
    
    if current_section["content"]:
        sections.append(current_section)
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<boomi-process-guide>
    <metadata>
        <name>{escape(base_name)}</name>
        <type>Process Guide</type>
        <converted_date>{datetime.now().isoformat()}</converted_date>
        <source_file>{escape(filename)}</source_file>
    </metadata>
    
    <sections>'''
    
    for section in sections:
        xml_content += f'''
        <section>
            <title>{escape(section["title"])}</title>
            <content>'''
        
        for content_line in section["content"]:
            xml_content += f'''
                <paragraph>{escape(content_line)}</paragraph>'''
        
        xml_content += '''
            </content>
        </section>'''
    
    xml_content += '''
    </sections>
</boomi-process-guide>'''
    
    return xml_content

def convert_text_to_xml(content, filename):
    """Convert plain text content to XML format"""
    base_name = os.path.splitext(filename)[0]
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<boomi-text-document>
    <metadata>
        <name>{escape(base_name)}</name>
        <type>Text Document</type>
        <converted_date>{datetime.now().isoformat()}</converted_date>
        <source_file>{escape(filename)}</source_file>
    </metadata>
    
    <content>
        <raw_text><![CDATA[{content}]]></raw_text>
    </content>
</boomi-text-document>'''
    
    return xml_content

def format_xml_content(xml_content):
    """Format XML content with proper indentation"""
    try:
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_content)
        return dom.toprettyxml(indent="    ", encoding=None).split('\n', 1)[1]  # Remove first line (XML declaration gets duplicated)
    except:
        return xml_content

def convert_file_to_xml(content, filename):
    """Convert file content to appropriate XML format based on content type"""
    content_type = detect_content_type(content, filename)
    
    print(f"  📄 Detected content type: {content_type}")
    
    if content_type == "xml":
        return content  # Already XML
    elif content_type == "connection_config":
        return convert_connection_config_to_xml(content, filename)
    elif content_type == "mapping_config":
        return convert_mapping_config_to_xml(content, filename)
    elif content_type == "process_guide":
        return convert_process_guide_to_xml(content, filename)
    else:
        return convert_text_to_xml(content, filename)

def convert_files_in_directory(directory_path):
    """Convert all .txt files in the specified directory to .xml files"""
    
    if not os.path.exists(directory_path):
        print(f"❌ Directory {directory_path} does not exist!")
        return
    
    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"ℹ️  No .txt files found in {directory_path}")
        return
    
    print(f"📋 Found {len(txt_files)} .txt files to convert:")
    print()
    
    converted_count = 0
    error_count = 0
    
    for txt_file in txt_files:
        txt_path = os.path.join(directory_path, txt_file)
        xml_file = txt_file.replace('.txt', '.xml')
        xml_path = os.path.join(directory_path, xml_file)
        
        print(f"🔄 Converting: {txt_file}")
        
        try:
            # Read the text file
            with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Convert to XML
            xml_content = convert_file_to_xml(content, txt_file)
            
            # Format the XML
            if not is_already_xml(content):
                xml_content = format_xml_content(xml_content)
            
            # Write the XML file
            with open(xml_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            print(f"  ✅ Successfully created: {xml_file}")
            converted_count += 1
            
        except Exception as e:
            print(f"  ❌ Error converting {txt_file}: {str(e)}")
            error_count += 1
        
        print()
    
    print(f"📊 Conversion Summary:")
    print(f"  ✅ Successfully converted: {converted_count} files")
    print(f"  ❌ Errors: {error_count} files")
    print(f"  📁 Total processed: {len(txt_files)} files")

def main():
    """Main function"""
    # Directory containing the text files
    boomi_api_dir = "boomi-api"
    
    print("🚀 Enhanced TXT to XML Converter")
    print("=" * 50)
    print(f"📁 Target directory: {boomi_api_dir}")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    
    convert_files_in_directory(boomi_api_dir)
    
    print("=" * 50)
    print("🎉 Conversion completed!")

if __name__ == "__main__":
    main()
