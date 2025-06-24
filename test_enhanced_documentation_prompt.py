#!/usr/bin/env python3
"""
Test the enhanced documentation prompt to ensure it captures Boomi-specific details.
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, 'app')

def test_enhanced_prompt_content():
    """Test that the enhanced prompt includes Boomi-specific requirements."""
    
    try:
        from documentation_enhancer import DocumentationEnhancer
        
        # Create enhancer instance
        enhancer = DocumentationEnhancer()
        
        # Create a test prompt
        test_base_doc = """
        # Test Boomi Process
        
        This is a test Dell Boomi process with:
        - Start Event with Web Services Server
        - Document Properties with HTTP connector calls
        - Map component with field mappings
        - Salesforce connector action
        - Stop event
        """
        
        # Get the prompt (we'll extract it from the enhance_documentation method)
        # Since the prompt is created inside the method, we'll check the method source
        import inspect
        
        enhance_method_source = inspect.getsource(enhancer.enhance_documentation)
        
        print("🧪 Testing Enhanced Documentation Prompt")
        print("=" * 60)
        
        # Check for Boomi-specific keywords
        boomi_keywords = [
            "Dell Boomi",
            "shapetype",
            "connectoraction",
            "documentproperties",
            "dragpoints",
            "toShape",
            "HTTP connector calls",
            "Document Properties",
            "fromKey/toKey",
            "Boomi XML",
            "BOOMI-SPECIFIC",
            "connectorType",
            "actionType"
        ]
        
        found_keywords = []
        missing_keywords = []
        
        for keyword in boomi_keywords:
            if keyword in enhance_method_source:
                found_keywords.append(keyword)
                print(f"✅ Found Boomi keyword: {keyword}")
            else:
                missing_keywords.append(keyword)
                print(f"❌ Missing keyword: {keyword}")
        
        print(f"\n📊 Keyword Analysis:")
        print(f"   Found: {len(found_keywords)}/{len(boomi_keywords)} Boomi-specific keywords")
        
        # Check for removal of MuleSoft references
        mulesoft_keywords = [
            "MuleSoft",
            "DataWeave",
            "Flow Reference"
        ]
        
        mulesoft_found = []
        for keyword in mulesoft_keywords:
            if keyword in enhance_method_source:
                mulesoft_found.append(keyword)
                print(f"⚠️ Still contains MuleSoft reference: {keyword}")
        
        # Check for Mermaid diagram enhancements
        mermaid_keywords = [
            "Boomi diagram structure",
            "FOLLOW THE EXACT SEQUENCE",
            "Boomi XML dragpoints",
            "Document Properties with HTTP calls",
            "Boomi component types"
        ]
        
        mermaid_found = []
        for keyword in mermaid_keywords:
            if keyword in enhance_method_source:
                mermaid_found.append(keyword)
                print(f"✅ Found Mermaid enhancement: {keyword}")
        
        print(f"\n📊 Enhancement Analysis:")
        print(f"   Boomi keywords: {len(found_keywords)}/{len(boomi_keywords)}")
        print(f"   MuleSoft references: {len(mulesoft_found)} (should be 0)")
        print(f"   Mermaid enhancements: {len(mermaid_found)}/{len(mermaid_keywords)}")
        
        # Overall assessment
        success_rate = len(found_keywords) / len(boomi_keywords)
        mermaid_rate = len(mermaid_found) / len(mermaid_keywords)
        
        if success_rate >= 0.8 and len(mulesoft_found) == 0 and mermaid_rate >= 0.6:
            print(f"\n🎉 Enhanced prompt is well-configured for Boomi!")
            print(f"   ✅ {success_rate:.1%} Boomi keyword coverage")
            print(f"   ✅ No MuleSoft references")
            print(f"   ✅ {mermaid_rate:.1%} Mermaid enhancement coverage")
            return True
        else:
            print(f"\n⚠️ Enhanced prompt needs improvement:")
            if success_rate < 0.8:
                print(f"   ❌ Low Boomi keyword coverage: {success_rate:.1%}")
            if len(mulesoft_found) > 0:
                print(f"   ❌ Still contains MuleSoft references: {mulesoft_found}")
            if mermaid_rate < 0.6:
                print(f"   ❌ Low Mermaid enhancement coverage: {mermaid_rate:.1%}")
            return False
            
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_structure():
    """Test that the prompt has the correct structure for Boomi analysis."""
    
    try:
        from documentation_enhancer import DocumentationEnhancer
        import inspect
        
        enhancer = DocumentationEnhancer()
        enhance_method_source = inspect.getsource(enhancer.enhance_documentation)
        
        print("\n🔍 Testing Prompt Structure")
        print("=" * 40)
        
        # Check for critical sections
        required_sections = [
            "CRITICAL BOOMI-SPECIFIC ANALYSIS REQUIREMENTS",
            "SEQUENCE OF EVENTS MUST BE ACCURATE",
            "CAPTURE COMPLEX BOOMI PATTERNS",
            "Current Dell Boomi Flow Logic",
            "Boomi Transformations Explained",
            "Core Boomi Components",
            "Boomi Connector Types to SAP Adapters"
        ]
        
        found_sections = []
        for section in required_sections:
            if section in enhance_method_source:
                found_sections.append(section)
                print(f"✅ Found section: {section}")
            else:
                print(f"❌ Missing section: {section}")
        
        structure_score = len(found_sections) / len(required_sections)
        print(f"\n📊 Structure Analysis: {structure_score:.1%} coverage")
        
        if structure_score >= 0.8:
            print("✅ Prompt structure is well-organized for Boomi analysis")
            return True
        else:
            print("❌ Prompt structure needs improvement")
            return False
            
    except Exception as e:
        print(f"💥 Structure test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing Enhanced Documentation Prompt for Boomi")
    print("=" * 70)
    
    success1 = test_enhanced_prompt_content()
    success2 = test_prompt_structure()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 Enhanced documentation prompt is ready for Boomi!")
        print("✅ Key improvements:")
        print("   - Boomi-specific terminology and analysis")
        print("   - Accurate sequence analysis from XML dragpoints")
        print("   - Complex Document Properties handling")
        print("   - HTTP connector call documentation")
        print("   - Field mapping preservation")
        print("   - Mermaid diagram enhancements")
        print("   - Removed MuleSoft references")
        return 0
    else:
        print("⚠️ Enhanced documentation prompt needs further refinement")
        return 1

if __name__ == "__main__":
    exit(main())
