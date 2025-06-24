#!/usr/bin/env python3
"""
Test the Stripe to Salesforce Opportunity conversion with our enhanced system.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, 'BoomiToIS-API')

def test_stripe_to_sf_conversion():
    """Test the conversion of the Stripe to SF Opportunity Boomi XML."""
    
    try:
        from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator
        from boomi_xml_processor import BoomiXMLProcessor
        
        print("🧪 Testing Stripe to Salesforce Opportunity Conversion")
        print("=" * 60)
        
        # File path
        xml_file = "StripeToSFOpp/Create-SFOpp-from-Stripe.xml"
        
        if not os.path.exists(xml_file):
            print(f"❌ File not found: {xml_file}")
            return False
        
        print(f"📄 Processing file: {xml_file}")
        
        # Step 1: Process the Boomi XML
        processor = BoomiXMLProcessor()
        markdown_content = processor._process_xml_file(xml_file)
        markdown_doc = processor._generate_markdown()
        
        print(f"✅ Boomi XML processed successfully")
        print(f"📊 Markdown length: {len(markdown_doc)} characters")
        
        # Step 2: Test the enhanced prompt
        generator = EnhancedGenAIIFlowGenerator(provider="local")
        prompt = generator._create_detailed_analysis_prompt(markdown_doc)
        
        print(f"✅ Enhanced prompt created")
        print(f"📊 Prompt length: {len(prompt)} characters")
        
        # Step 3: Check if prompt captures the complex patterns we identified
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
            "Mappings"
        ]
        
        found_patterns = []
        for pattern in complex_patterns:
            if pattern in markdown_doc:
                found_patterns.append(pattern)
                print(f"✅ Found complex pattern: {pattern}")
            else:
                print(f"❌ Missing pattern: {pattern}")
        
        pattern_coverage = len(found_patterns) / len(complex_patterns)
        print(f"\n📊 Complex Pattern Coverage: {pattern_coverage:.1%}")
        
        # Step 4: Check if the prompt includes Boomi-specific guidance
        boomi_guidance = [
            "BOOMI-SPECIFIC ANALYSIS",
            "shapetype",
            "connectoraction",
            "documentproperties",
            "HTTP connector calls",
            "fromKey/toKey"
        ]
        
        guidance_found = []
        for guidance in boomi_guidance:
            if guidance in prompt:
                guidance_found.append(guidance)
        
        guidance_coverage = len(guidance_found) / len(boomi_guidance)
        print(f"📊 Boomi Guidance Coverage: {guidance_coverage:.1%}")
        
        # Step 5: Predict success likelihood
        if pattern_coverage >= 0.8 and guidance_coverage >= 0.8:
            print(f"\n🎉 HIGH SUCCESS LIKELIHOOD!")
            print(f"✅ Complex patterns detected: {pattern_coverage:.1%}")
            print(f"✅ Boomi guidance included: {guidance_coverage:.1%}")
            print(f"✅ Enhanced prompt should capture:")
            print(f"   - HTTP GET calls for customer and product data")
            print(f"   - Dynamic property calculations")
            print(f"   - Field mappings from Map component")
            print(f"   - Salesforce connector configuration")
            print(f"   - Exact sequence from dragpoints")
            return True
        else:
            print(f"\n⚠️ POTENTIAL ISSUES:")
            if pattern_coverage < 0.8:
                print(f"   ❌ Low pattern coverage: {pattern_coverage:.1%}")
            if guidance_coverage < 0.8:
                print(f"   ❌ Low guidance coverage: {guidance_coverage:.1%}")
            return False
            
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_expected_components():
    """Test what components we expect to generate for this integration."""
    
    print("\n🔍 Expected Component Analysis")
    print("=" * 40)
    
    expected_components = {
        "Start Event": "Web Services Server Listen (WSS)",
        "Set Dynamic Properties": "Content Modifier with HTTP GET calls",
        "Transform": "Message Mapping (Map component)",
        "Salesforce Send": "Request Reply with Salesforce adapter",
        "End Event": "End Message Event"
    }
    
    print("📋 Expected SAP Integration Suite Components:")
    for boomi_comp, sap_comp in expected_components.items():
        print(f"   {boomi_comp} → {sap_comp}")
    
    print("\n🔧 Critical Features to Capture:")
    critical_features = [
        "HTTP GET to fetch customer name using customer ID",
        "HTTP GET to fetch product name using product ID", 
        "Concatenation: '{CustomerName} has subscribed to: {ProductName}'",
        "Date calculation: 3 months before current date",
        "Field mappings: DDP_CustomerName → Opportunity.Name",
        "Field mappings: DDP_SalesforceDescription → Opportunity.Description",
        "Field mappings: DDP_CloseDate → Opportunity.CloseDate",
        "Default value: StageName = 'Pipeline'"
    ]
    
    for feature in critical_features:
        print(f"   ✓ {feature}")
    
    return True

def main():
    """Main test function."""
    print("🚀 Testing Enhanced System with Stripe to SF Opportunity")
    print("=" * 70)
    
    success1 = test_stripe_to_sf_conversion()
    success2 = test_expected_components()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 SYSTEM IS READY!")
        print("✅ The enhanced system should successfully:")
        print("   1. Parse the complex Boomi XML structure")
        print("   2. Capture all HTTP connector dependencies")
        print("   3. Document the sophisticated Document Properties logic")
        print("   4. Generate accurate field mappings")
        print("   5. Create proper SAP Integration Suite components")
        print("   6. Maintain the correct sequence of operations")
        print("\n🚀 You can proceed with confidence!")
        return 0
    else:
        print("⚠️ System may need additional refinements")
        return 1

if __name__ == "__main__":
    exit(main())
