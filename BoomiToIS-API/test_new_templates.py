#!/usr/bin/env python3
"""
Test script for new iFlow templates and positioning system.
This script tests all the newly added templates to ensure they generate valid XML
and that the positioning system works correctly.
"""

import sys
import os
import xml.etree.ElementTree as ET
from bpmn_templates import BpmnTemplates, ComponentPositionManager, TemplateBpmnGenerator

def test_xml_validity(xml_content, component_name):
    """Test if the generated XML is valid."""
    try:
        ET.fromstring(xml_content)
        print(f"✅ {component_name}: XML is valid")
        return True
    except ET.ParseError as e:
        print(f"❌ {component_name}: XML is invalid - {e}")
        return False

def test_positioning_system():
    """Test the ComponentPositionManager."""
    print("\n🧪 Testing ComponentPositionManager...")
    
    position_manager = ComponentPositionManager()
    
    # Test basic positioning
    pos1 = position_manager.calculate_position("test_component_1", "activity")
    pos2 = position_manager.calculate_position("test_component_2", "activity")
    
    # Check if positions are different and properly spaced
    if pos2["x"] - pos1["x"] == position_manager.component_spacing_x:
        print("✅ Component spacing is correct")
    else:
        print(f"❌ Component spacing is incorrect: {pos2['x'] - pos1['x']} != {position_manager.component_spacing_x}")
    
    # Test event positioning
    event_pos = position_manager.calculate_position("test_event", "start_event")
    if event_pos["width"] == 32 and event_pos["height"] == 32:
        print("✅ Event dimensions are correct")
    else:
        print(f"❌ Event dimensions are incorrect: {event_pos['width']}x{event_pos['height']} != 32x32")
    
    # Test waypoint calculation
    waypoints = position_manager.calculate_sequence_flow_waypoints("test_component_1", "test_component_2")
    if all(key in waypoints for key in ["source_x", "source_y", "target_x", "target_y"]):
        print("✅ Waypoint calculation works")
    else:
        print("❌ Waypoint calculation failed")

def test_new_templates():
    """Test all newly added templates."""
    print("\n🧪 Testing New Templates...")
    
    templates = BpmnTemplates()
    test_results = []
    
    # Test mapping components
    print("\n📋 Testing Mapping Components...")
    
    # Operation Mapping
    op_mapping = templates.operation_mapping_template(
        id="OpMapping_1", 
        name="Test Operation Mapping",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(op_mapping["definition"], "Operation Mapping"))
    
    # XSLT Mapping
    xslt_mapping = templates.xslt_mapping_template(
        id="XSLT_1",
        name="Test XSLT Mapping", 
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(xslt_mapping["definition"], "XSLT Mapping"))
    
    # Message Mapping
    msg_mapping = templates.message_mapping_template(
        id="MsgMapping_1",
        name="Test Message Mapping",
        incoming_flow="Flow_In", 
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(msg_mapping["definition"], "Message Mapping"))
    
    # Test validation components
    print("\n🔍 Testing Validation Components...")
    
    # XML Validator
    xml_validator = templates.xml_validator_template(
        id="XMLValidator_1",
        name="Test XML Validator",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(xml_validator["definition"], "XML Validator"))
    
    # Test processing components
    print("\n⚙️ Testing Processing Components...")
    
    # Filter
    filter_comp = templates.filter_template(
        id="Filter_1",
        name="Test Filter",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(filter_comp["definition"], "Filter"))
    
    # Groovy Script
    groovy_script = templates.groovy_script_template(
        id="Groovy_1",
        name="Test Groovy Script",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(groovy_script["definition"], "Groovy Script"))
    
    # XML Modifier
    xml_modifier = templates.xml_modifier_template(
        id="XMLModifier_1",
        name="Test XML Modifier",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(xml_modifier["definition"], "XML Modifier"))
    
    # Write Variables
    write_vars = templates.write_variables_template(
        id="WriteVars_1",
        name="Test Write Variables",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(write_vars["definition"], "Write Variables"))
    
    # Test splitter components
    print("\n✂️ Testing Splitter Components...")
    
    # EDI Splitter
    edi_splitter = templates.edi_splitter_template(
        id="EDISplitter_1",
        name="Test EDI Splitter",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(edi_splitter["definition"], "EDI Splitter"))
    
    # IDoc Splitter
    idoc_splitter = templates.idoc_splitter_template(
        id="IDocSplitter_1",
        name="Test IDoc Splitter",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(idoc_splitter["definition"], "IDoc Splitter"))
    
    # General Splitter
    general_splitter = templates.general_splitter_template(
        id="GeneralSplitter_1",
        name="Test General Splitter",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(general_splitter["definition"], "General Splitter"))
    
    return test_results

def test_gateway_components():
    """Test gateway components."""
    print("\n🚦 Testing Gateway Components...")
    
    templates = BpmnTemplates()
    test_results = []
    
    # Sequential Multicast
    seq_multicast = templates.sequential_multicast_template(
        id="SeqMulticast_1",
        name="Test Sequential Multicast",
        incoming_flow="Flow_In",
        outgoing_flows=["Flow_Out1", "Flow_Out2"]
    )
    test_results.append(test_xml_validity(seq_multicast["definition"], "Sequential Multicast"))
    
    # Parallel Multicast
    par_multicast = templates.parallel_multicast_template(
        id="ParMulticast_1", 
        name="Test Parallel Multicast",
        incoming_flow="Flow_In",
        outgoing_flows=["Flow_Out1", "Flow_Out2"]
    )
    test_results.append(test_xml_validity(par_multicast["definition"], "Parallel Multicast"))
    
    # Join
    join_comp = templates.join_template(
        id="Join_1",
        name="Test Join",
        incoming_flows=["Flow_In1", "Flow_In2"],
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(join_comp["definition"], "Join"))
    
    # Router
    router_comp = templates.router_template(
        id="Router_1",
        name="Test Router",
        incoming_flow="Flow_In",
        outgoing_flows=["Flow_Out1", "Flow_Out2"]
    )
    test_results.append(test_xml_validity(router_comp["definition"], "Router"))
    
    return test_results

def test_storage_components():
    """Test storage components."""
    print("\n💾 Testing Storage Components...")
    
    templates = BpmnTemplates()
    test_results = []
    
    # Select
    select_comp = templates.select_template(
        id="Select_1",
        name="Test Select",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(select_comp["definition"], "Select"))
    
    # Write
    write_comp = templates.write_template(
        id="Write_1",
        name="Test Write",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(write_comp["definition"], "Write"))
    
    # Get
    get_comp = templates.get_template(
        id="Get_1",
        name="Test Get",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(get_comp["definition"], "Get"))
    
    # Persist
    persist_comp = templates.persist_template(
        id="Persist_1",
        name="Test Persist",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(persist_comp["definition"], "Persist"))
    
    # ID Mapping
    id_mapping = templates.id_mapping_template(
        id="IDMapping_1",
        name="Test ID Mapping",
        incoming_flow="Flow_In",
        outgoing_flow="Flow_Out"
    )
    test_results.append(test_xml_validity(id_mapping["definition"], "ID Mapping"))
    
    return test_results

def main():
    """Main test function."""
    print("🚀 Starting Template Tests...")
    
    all_results = []
    
    # Test positioning system
    test_positioning_system()
    
    # Test all new templates
    all_results.extend(test_new_templates())
    all_results.extend(test_gateway_components())
    all_results.extend(test_storage_components())
    
    # Summary
    passed = sum(all_results)
    total = len(all_results)
    
    print(f"\n📊 Test Summary:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Templates are working correctly.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
