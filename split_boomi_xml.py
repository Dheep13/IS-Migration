#!/usr/bin/env python3
"""
Split multi-document Boomi XML files into separate XML files.
"""

import os
import re
from pathlib import Path

def split_boomi_xml_file(input_file: str, output_dir: str = None) -> list:
    """
    Split a multi-document Boomi XML file into separate XML files.
    
    Args:
        input_file (str): Path to the input XML file
        output_dir (str): Directory to save split files (optional)
        
    Returns:
        list: List of created file paths
    """
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Find XML declarations to split documents
    xml_pattern = r'<\?xml[^>]*\?>'
    matches = list(re.finditer(xml_pattern, content))
    
    if len(matches) <= 1:
        print(f"📄 Single XML document found in {input_file}")
        return [input_file]
    
    print(f"📄 Found {len(matches)} XML documents in {input_file}")
    
    created_files = []
    base_name = Path(input_file).stem
    
    for i, match in enumerate(matches):
        start = match.start()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
            xml_content = content[start:end].strip()
        else:
            xml_content = content[start:].strip()
        
        # Extract component name from XML for better file naming
        component_name = extract_component_name(xml_content)
        
        if component_name:
            output_file = os.path.join(output_dir, f"{base_name}_{i+1:02d}_{component_name}.xml")
        else:
            output_file = os.path.join(output_dir, f"{base_name}_{i+1:02d}.xml")
        
        # Write the individual XML document
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        created_files.append(output_file)
        print(f"✅ Created: {os.path.basename(output_file)}")
    
    return created_files

def extract_component_name(xml_content: str) -> str:
    """Extract component name from XML content for better file naming."""
    
    # Try to extract name attribute
    name_match = re.search(r'name="([^"]+)"', xml_content)
    if name_match:
        name = name_match.group(1)
        # Clean the name for filename
        name = re.sub(r'[^\w\-_]', '_', name)
        return name[:50]  # Limit length
    
    # Try to extract component type
    type_match = re.search(r'type="([^"]+)"', xml_content)
    if type_match:
        comp_type = type_match.group(1)
        return comp_type.replace('.', '_')
    
    # Try to extract subType
    subtype_match = re.search(r'subType="([^"]+)"', xml_content)
    if subtype_match:
        return subtype_match.group(1)
    
    return "component"

def main():
    """Main function to split the Stripe to SF XML file."""
    
    input_file = "StripeToSFOpp/Create-SFOpp-from-Stripe.xml"
    output_dir = "StripeToSFOpp/split"
    
    print("🔧 Splitting Boomi XML File")
    print("=" * 50)
    print(f"📄 Input: {input_file}")
    print(f"📁 Output: {output_dir}")
    
    try:
        created_files = split_boomi_xml_file(input_file, output_dir)
        
        print(f"\n✅ Successfully split into {len(created_files)} files:")
        for file_path in created_files:
            file_size = os.path.getsize(file_path)
            print(f"   📄 {os.path.basename(file_path)} ({file_size:,} bytes)")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Process each XML file individually")
        print(f"   2. Use the split files for better analysis")
        print(f"   3. Generate documentation for each component")
        
        return created_files
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    main()
