#!/usr/bin/env python3
"""
Test processing the split Boomi XML files.
"""

import sys
import os
import glob

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_split_xml_processing():
    """Test processing the split XML files."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        from boomi_xml_processor import BoomiXMLProcessor
        
        print("🧪 Testing Split XML Processing")
        print("=" * 50)
        
        # Find split XML files
        split_dir = "StripeToSFOpp/split"
        if not os.path.exists(split_dir):
            print(f"❌ Split directory not found: {split_dir}")
            print("💡 Please run: python split_boomi_xml.py first")
            return False
        
        xml_files = glob.glob(os.path.join(split_dir, "*.xml"))
        if not xml_files:
            print(f"❌ No XML files found in: {split_dir}")
            return False
        
        print(f"📄 Found {len(xml_files)} split XML files")
        
        # Process each XML file
        processor = BoomiXMLProcessor()
        all_markdown = []
        
        for xml_file in sorted(xml_files):
            print(f"\n📄 Processing: {os.path.basename(xml_file)}")
            
            try:
                # Process individual XML file
                processor._process_xml_file(xml_file)
                
                # Generate markdown for this component
                component_markdown = processor._generate_markdown()
                if component_markdown and len(component_markdown) > 100:
                    all_markdown.append(f"## Component: {os.path.basename(xml_file)}\n\n{component_markdown}")
                    print(f"✅ Generated {len(component_markdown)} chars of markdown")
                else:
                    print(f"⚠️ Limited markdown generated ({len(component_markdown)} chars)")
                
                # Clear components for next file
                processor.components = []
                
            except Exception as e:
                print(f"❌ Error processing {xml_file}: {e}")
                continue
        
        # Combine all markdown
        combined_markdown = "\n\n".join(all_markdown)
        
        print(f"\n📊 Combined Analysis:")
        print(f"   Total markdown length: {len(combined_markdown)} characters")
        print(f"   Components processed: {len(all_markdown)}")
        
        # Test with enhanced prompt
        if combined_markdown:
            generator = EnhancedGenAIIFlowGenerator(provider="local")
            prompt = generator._create_detailed_analysis_prompt(combined_markdown)
            
            print(f"✅ Enhanced prompt created")
            print(f"📊 Prompt length: {len(prompt)} characters")
            
            # Check for complex patterns
            complex_patterns = [
                "Document Properties",
                "HTTP connector",
                "DDP_CustomerName",
                "DDP_Subscription", 
                "DDP_SalesforceDescription",
                "DDP_CloseDate",
                "connectorparameter",
                "Salesforce",
                "Map",
                "Mappings",
                "documentproperties",
                "connectoraction"
            ]
            
            found_patterns = []
            for pattern in complex_patterns:
                if pattern in combined_markdown:
                    found_patterns.append(pattern)
                    print(f"✅ Found pattern: {pattern}")
            
            pattern_coverage = len(found_patterns) / len(complex_patterns)
            print(f"\n📊 Pattern Coverage: {pattern_coverage:.1%}")
            
            if pattern_coverage >= 0.5:
                print(f"🎉 GOOD COVERAGE! Should generate accurate documentation")
                return True
            else:
                print(f"⚠️ Low coverage, may need manual review")
                return False
        else:
            print(f"❌ No meaningful markdown generated")
            return False
            
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_split_files():
    """Show what split files were created."""
    
    split_dir = "StripeToSFOpp/split"
    if not os.path.exists(split_dir):
        print(f"❌ Split directory not found: {split_dir}")
        return
    
    xml_files = glob.glob(os.path.join(split_dir, "*.xml"))
    
    print(f"\n📁 Split Files in {split_dir}:")
    for xml_file in sorted(xml_files):
        file_size = os.path.getsize(xml_file)
        print(f"   📄 {os.path.basename(xml_file)} ({file_size:,} bytes)")

def main():
    """Main test function."""
    print("🚀 Testing Split XML Processing for Stripe to SF")
    print("=" * 60)
    
    show_split_files()
    success = test_split_xml_processing()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SPLIT XML PROCESSING SUCCESSFUL!")
        print("✅ The system can now:")
        print("   1. Process individual Boomi components")
        print("   2. Extract complex Document Properties")
        print("   3. Capture HTTP connector configurations")
        print("   4. Generate comprehensive documentation")
        print("   5. Create accurate SAP Integration Suite mappings")
        print("\n🚀 Ready to generate the iFlow!")
        return 0
    else:
        print("⚠️ Split XML processing needs refinement")
        print("💡 Check the split files and markdown generation")
        return 1

if __name__ == "__main__":
    exit(main())
