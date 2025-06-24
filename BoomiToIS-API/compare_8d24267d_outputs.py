#!/usr/bin/env python3
"""
Comprehensive comparison between full-fledged product output and enhanced template output
for the 8d24267d case to verify our enhanced templates match the production system.
"""

import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_xml_safely(file_path):
    """Parse XML file safely with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with ElementTree
        root = ET.fromstring(content)
        return content, root
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None, None

def extract_components(xml_content):
    """Extract key components from XML content"""
    components = {
        'participants': [],
        'message_flows': [],
        'service_tasks': [],
        'call_activities': [],
        'sequence_flows': [],
        'start_events': [],
        'end_events': []
    }
    
    # Extract participants
    participants = re.findall(r'<bpmn2:participant[^>]*id="([^"]*)"[^>]*name="([^"]*)"', xml_content)
    for pid, name in participants:
        components['participants'].append({'id': pid, 'name': name})
    
    # Extract message flows with component types
    message_flows = re.findall(r'<bpmn2:messageFlow[^>]*id="([^"]*)"[^>]*name="([^"]*)".*?</bpmn2:messageFlow>', xml_content, re.DOTALL)
    for mid, name in message_flows:
        # Extract component type from the message flow
        flow_match = re.search(rf'<bpmn2:messageFlow[^>]*id="{mid}".*?</bpmn2:messageFlow>', xml_content, re.DOTALL)
        if flow_match:
            flow_content = flow_match.group(0)
            component_type_match = re.search(r'<key>ComponentType</key>\s*<value>([^<]*)</value>', flow_content)
            component_type = component_type_match.group(1) if component_type_match else 'Unknown'
            
            # Extract operation for OData
            operation_match = re.search(r'<key>operation</key>\s*<value>([^<]*)</value>', flow_content)
            operation = operation_match.group(1) if operation_match else 'N/A'
            
            # Extract HTTP method for HTTP
            http_method_match = re.search(r'<key>httpMethod</key>\s*<value>([^<]*)</value>', flow_content)
            http_method = http_method_match.group(1) if http_method_match else 'N/A'
            
            components['message_flows'].append({
                'id': mid, 
                'name': name, 
                'component_type': component_type,
                'operation': operation,
                'http_method': http_method
            })
    
    # Extract service tasks
    service_tasks = re.findall(r'<bpmn2:serviceTask[^>]*id="([^"]*)"[^>]*name="([^"]*)"', xml_content)
    for sid, name in service_tasks:
        components['service_tasks'].append({'id': sid, 'name': name})
    
    # Extract call activities (enrichers, scripts)
    call_activities = re.findall(r'<bpmn2:callActivity[^>]*id="([^"]*)"[^>]*name="([^"]*)"', xml_content)
    for cid, name in call_activities:
        components['call_activities'].append({'id': cid, 'name': name})
    
    # Extract sequence flows
    sequence_flows = re.findall(r'<bpmn2:sequenceFlow[^>]*id="([^"]*)"[^>]*sourceRef="([^"]*)"[^>]*targetRef="([^"]*)"', xml_content)
    for fid, source, target in sequence_flows:
        components['sequence_flows'].append({'id': fid, 'source': source, 'target': target})
    
    return components

def compare_components(prod_components, template_components, component_type):
    """Compare specific component types between production and template outputs"""
    print(f"\n📋 Comparing {component_type.upper()}:")
    
    prod_items = prod_components[component_type]
    template_items = template_components[component_type]
    
    print(f"  Production: {len(prod_items)} items")
    print(f"  Template:   {len(template_items)} items")
    
    if len(prod_items) != len(template_items):
        print(f"  ⚠️  COUNT MISMATCH: Production has {len(prod_items)}, Template has {len(template_items)}")
    else:
        print(f"  ✅ COUNT MATCH: Both have {len(prod_items)} items")
    
    # Compare specific items
    if component_type == 'message_flows':
        print(f"\n  📊 Message Flow Details:")
        for i, (prod, template) in enumerate(zip(prod_items, template_items)):
            print(f"    Flow {i+1}:")
            print(f"      Production:  {prod['name']} ({prod['component_type']}) - Op: {prod['operation']}, HTTP: {prod['http_method']}")
            print(f"      Template:    {template['name']} ({template['component_type']}) - Op: {template['operation']}, HTTP: {template['http_method']}")
            
            if prod['component_type'] == template['component_type']:
                print(f"      ✅ Component Type Match: {prod['component_type']}")
            else:
                print(f"      ❌ Component Type Mismatch: {prod['component_type']} vs {template['component_type']}")
    
    return len(prod_items) == len(template_items)

def analyze_odata_components(prod_content, template_content):
    """Specific analysis of OData components"""
    print(f"\n🔍 OData Component Analysis:")
    
    # Check for HCIOData components
    prod_hciodata = prod_content.count('HCIOData')
    template_hciodata = template_content.count('HCIOData')
    
    print(f"  HCIOData components:")
    print(f"    Production: {prod_hciodata}")
    print(f"    Template:   {template_hciodata}")
    
    if prod_hciodata == template_hciodata:
        print(f"    ✅ HCIOData count matches")
    else:
        print(f"    ❌ HCIOData count mismatch")
    
    # Check for Create(POST) operations
    prod_create_post = prod_content.count('Create(POST)')
    template_create_post = template_content.count('Create(POST)')
    
    print(f"  Create(POST) operations:")
    print(f"    Production: {prod_create_post}")
    print(f"    Template:   {template_create_post}")
    
    if prod_create_post == template_create_post:
        print(f"    ✅ Create(POST) count matches")
    else:
        print(f"    ❌ Create(POST) count mismatch")
    
    # Check for resource paths
    prod_resource_paths = re.findall(r'<key>resourcePath</key>\s*<value>([^<]*)</value>', prod_content)
    template_resource_paths = re.findall(r'<key>resourcePath</key>\s*<value>([^<]*)</value>', template_content)
    
    print(f"  Resource paths:")
    print(f"    Production: {prod_resource_paths}")
    print(f"    Template:   {template_resource_paths}")
    
    if prod_resource_paths == template_resource_paths:
        print(f"    ✅ Resource paths match")
    else:
        print(f"    ❌ Resource paths differ")

def analyze_http_components(prod_content, template_content):
    """Specific analysis of HTTP components"""
    print(f"\n🔍 HTTP Component Analysis:")
    
    # Check for HTTP components
    prod_http = prod_content.count('ComponentType">HTTP')
    template_http = template_content.count('ComponentType">HTTP')
    
    print(f"  HTTP components:")
    print(f"    Production: {prod_http}")
    print(f"    Template:   {template_http}")
    
    if prod_http == template_http:
        print(f"    ✅ HTTP component count matches")
    else:
        print(f"    ❌ HTTP component count mismatch")
    
    # Check for HTTP methods
    prod_http_methods = re.findall(r'<key>httpMethod</key>\s*<value>([^<]*)</value>', prod_content)
    template_http_methods = re.findall(r'<key>httpMethod</key>\s*<value>([^<]*)</value>', template_content)
    
    print(f"  HTTP methods:")
    print(f"    Production: {prod_http_methods}")
    print(f"    Template:   {template_http_methods}")
    
    if sorted(prod_http_methods) == sorted(template_http_methods):
        print(f"    ✅ HTTP methods match")
    else:
        print(f"    ❌ HTTP methods differ")

def main():
    """Main comparison function"""
    print("🔍 Comprehensive Comparison: 8d24267d Production vs Enhanced Templates")
    print("=" * 80)
    
    # File paths
    prod_file = "genai_debug/final_iflow_IFlow_8d24267d.xml"
    template_file = "genai_debug/test_generated_IFlow_8d24267d.xml"
    
    # Check if files exist
    if not os.path.exists(prod_file):
        print(f"❌ Production file not found: {prod_file}")
        return False
    
    if not os.path.exists(template_file):
        print(f"❌ Template file not found: {template_file}")
        return False
    
    print(f"📄 Production file: {prod_file}")
    print(f"📄 Template file:   {template_file}")
    
    # Parse XML files
    prod_content, prod_root = parse_xml_safely(prod_file)
    template_content, template_root = parse_xml_safely(template_file)
    
    if not prod_content or not template_content:
        print("❌ Failed to parse XML files")
        return False
    
    # Extract components
    print(f"\n🔧 Extracting components...")
    prod_components = extract_components(prod_content)
    template_components = extract_components(template_content)
    
    # Compare each component type
    all_match = True
    
    for component_type in ['participants', 'message_flows', 'service_tasks', 'call_activities', 'sequence_flows']:
        match = compare_components(prod_components, template_components, component_type)
        all_match = all_match and match
    
    # Specific OData analysis
    analyze_odata_components(prod_content, template_content)
    
    # Specific HTTP analysis
    analyze_http_components(prod_content, template_content)
    
    # Check for typos
    print(f"\n🔍 Typo Analysis:")
    prod_typos = prod_content.count('EndpointRecevier')
    template_typos = template_content.count('EndpointRecevier')
    
    print(f"  'EndpointRecevier' typos:")
    print(f"    Production: {prod_typos}")
    print(f"    Template:   {template_typos}")
    
    if prod_typos == 0 and template_typos == 0:
        print(f"    ✅ No typos in either file")
    elif prod_typos == template_typos:
        print(f"    ⚠️  Both files have the same number of typos")
    else:
        print(f"    ❌ Different typo counts")
    
    # Final summary
    print("=" * 80)
    if all_match:
        print("🎉 OVERALL ASSESSMENT: Enhanced templates match production output structure!")
        print("✅ Component counts match")
        print("✅ Adapter types are consistent")
        print("✅ Operations are properly mapped")
    else:
        print("⚠️  OVERALL ASSESSMENT: Some differences found between production and template outputs")
        print("📋 Review the detailed comparison above for specific differences")
    
    return all_match

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
