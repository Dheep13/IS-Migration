#!/usr/bin/env python3
"""
Simple test to verify BPMN templates are working correctly
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_bpmn_templates():
    """Test that BPMN templates can be imported and used"""
    print("🧪 Testing BPMN Templates...")
    
    try:
        from bpmn_templates import BpmnTemplates
        print("✅ Successfully imported BpmnTemplates")
        
        # Initialize templates
        templates = BpmnTemplates()
        print("✅ Successfully initialized BpmnTemplates")
        
        # Test basic template methods
        print("\n📋 Testing Basic Template Methods:")
        
        # Test start event
        start_event = templates.start_event_template("StartEvent_1", "Start")
        print(f"✅ start_event_template: {len(start_event)} characters")
        
        # Test end event
        end_event = templates.end_event_template("EndEvent_1", "End")
        print(f"✅ end_event_template: {len(end_event)} characters")
        
        # Test sequence flow
        seq_flow = templates.sequence_flow_template("Flow_1", "StartEvent_1", "EndEvent_1")
        print(f"✅ sequence_flow_template: {len(seq_flow)} characters")
        
        # Test adapter methods
        print("\n📋 Testing Adapter Methods:")
        
        # Test iflow_configuration_template (adapter method)
        if hasattr(templates, 'iflow_configuration_template'):
            iflow_config = templates.iflow_configuration_template()
            print(f"✅ iflow_configuration_template: Available")
        else:
            print(f"❌ iflow_configuration_template: NOT AVAILABLE")
            return False
        
        # Test generate_unique_id (adapter method)
        if hasattr(templates, 'generate_unique_id'):
            unique_id = templates.generate_unique_id("Test")
            print(f"✅ generate_unique_id: {unique_id}")
        else:
            print(f"❌ generate_unique_id: NOT AVAILABLE")
            return False
        
        # Test participant_template (adapter method)
        if hasattr(templates, 'participant_template'):
            participant = templates.participant_template("Participant_1", "Test Participant")
            print(f"✅ participant_template: {len(participant)} characters")
        else:
            print(f"❌ participant_template: NOT AVAILABLE")
            return False
        
        # Test odata_request_reply_pattern (adapter method)
        if hasattr(templates, 'odata_request_reply_pattern'):
            odata_pattern = templates.odata_request_reply_pattern(
                "ServiceTask_1", "Participant_1", "MessageFlow_1", "Test OData", "https://example.com"
            )
            print(f"✅ odata_request_reply_pattern: {len(str(odata_pattern))} characters")
        else:
            print(f"❌ odata_request_reply_pattern: NOT AVAILABLE")
            return False
        
        print("\n🎉 ALL BPMN TEMPLATE TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    print("🚀 BPMN Templates Test")
    print("=" * 40)
    
    success = test_bpmn_templates()
    
    print("=" * 40)
    if success:
        print("🎉 BPMN Templates are working correctly!")
    else:
        print("❌ BPMN Templates have issues!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
