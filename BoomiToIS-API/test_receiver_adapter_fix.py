#!/usr/bin/env python3
"""
Test script to verify that the receiver_adapter fix is working correctly.
This script tests the validation and fix functions for request_reply components.
"""

import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_genai_iflow_generator import EnhancedGenAIIFlowGenerator

def test_standalone_odata_fix():
    """Test that standalone odata components are converted to request_reply with receiver_adapter"""
    print("🧪 Testing standalone odata component fix...")
    
    # Create test data with standalone odata component (the problem case)
    test_data = {
        "process_name": "Test Process",
        "endpoints": [
            {
                "method": "POST",
                "path": "/test",
                "components": [
                    {
                        "type": "odata",  # This should be fixed
                        "name": "Create_Salesforce_Opportunity",
                        "id": "odata_1",
                        "config": {
                            "address": "${property.salesforce_url}",
                            "resource_path": "Opportunity",
                            "operation": "Create(POST)"
                        }
                    }
                ]
            }
        ]
    }
    
    # Initialize the generator and apply the fix
    generator = EnhancedGenAIIFlowGenerator()
    fixed_data = generator.validate_and_fix_components(test_data)
    
    # Check the results
    component = fixed_data["endpoints"][0]["components"][0]
    
    assert component["type"] == "request_reply", f"Expected 'request_reply', got '{component['type']}'"
    assert "receiver_adapter" in component, "Missing receiver_adapter"
    assert component["receiver_adapter"]["type"] == "odata_adapter", "Wrong receiver_adapter type"
    assert component["receiver_adapter"]["operation"] == "POST", "Wrong operation"
    
    print("✅ Standalone odata component successfully converted to request_reply with receiver_adapter")
    return True

def test_request_reply_without_adapter_fix():
    """Test that request_reply components without receiver_adapter get one added"""
    print("🧪 Testing request_reply without receiver_adapter fix...")
    
    # Create test data with request_reply component missing receiver_adapter
    test_data = {
        "process_name": "Test Process",
        "endpoints": [
            {
                "method": "POST",
                "path": "/test",
                "components": [
                    {
                        "type": "request_reply",  # Missing receiver_adapter
                        "name": "Create_Salesforce_Opportunity",
                        "id": "request_reply_1",
                        "config": {
                            "endpoint_path": "/services/data/v53.0/sobjects/Opportunity",
                            "method": "POST"
                        }
                    }
                ]
            }
        ]
    }
    
    # Initialize the generator and apply the fix
    generator = EnhancedGenAIIFlowGenerator()
    fixed_data = generator.validate_and_fix_components(test_data)
    
    # Check the results
    component = fixed_data["endpoints"][0]["components"][0]
    
    assert component["type"] == "request_reply", f"Expected 'request_reply', got '{component['type']}'"
    assert "receiver_adapter" in component, "Missing receiver_adapter"
    assert component["receiver_adapter"]["type"] == "odata_adapter", "Wrong receiver_adapter type"
    assert component["receiver_adapter"]["operation"] == "POST", "Wrong operation"
    
    print("✅ request_reply component successfully got receiver_adapter added")
    return True

def test_correct_component_unchanged():
    """Test that correctly formatted request_reply components are unchanged"""
    print("🧪 Testing that correct components remain unchanged...")
    
    # Create test data with correctly formatted request_reply component
    test_data = {
        "process_name": "Test Process",
        "endpoints": [
            {
                "method": "POST",
                "path": "/test",
                "components": [
                    {
                        "type": "request_reply",
                        "name": "Create_Salesforce_Opportunity",
                        "id": "request_reply_1",
                        "receiver_adapter": {
                            "type": "odata_adapter",
                            "operation": "POST",
                            "endpoint": "/services/data/v53.0/sobjects/Opportunity",
                            "connection": "salesforce_odata_connection"
                        },
                        "config": {
                            "endpoint_path": "/services/data/v53.0/sobjects/Opportunity",
                            "method": "POST"
                        }
                    }
                ]
            }
        ]
    }
    
    # Initialize the generator and apply the fix
    generator = EnhancedGenAIIFlowGenerator()
    original_json = json.dumps(test_data, sort_keys=True)
    fixed_data = generator.validate_and_fix_components(test_data)
    fixed_json = json.dumps(fixed_data, sort_keys=True)
    
    # Check that nothing changed
    assert original_json == fixed_json, "Correctly formatted component was modified"
    
    print("✅ Correctly formatted component remained unchanged")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing receiver_adapter validation and fix...")
    print("=" * 60)
    
    try:
        test_standalone_odata_fix()
        test_request_reply_without_adapter_fix()
        test_correct_component_unchanged()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED! The receiver_adapter fix is working correctly.")
        print("✅ Standalone 'odata' components will be converted to 'request_reply' with receiver_adapter")
        print("✅ 'request_reply' components without receiver_adapter will get one added")
        print("✅ Correctly formatted components remain unchanged")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
