#!/usr/bin/env python3
"""
Comprehensive analysis of All_Iflow_Artifacts to identify all SAP Integration Suite components
and compare them against our current enhanced templates to find gaps.
"""

import re
import os
from collections import defaultdict

def analyze_all_artifacts():
    """Analyze the All Artifacts.iflw file to extract all component types"""
    
    file_path = r"c:\Users\deepan\OneDrive - IT Resonance\Documents\DheepLearningITR\mule_cf_deployment\All_Iflow_Artifacts\src\main\resources\scenarioflows\integrationflow\All Artifacts.iflw"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 SAP Integration Suite - All Artifacts Analysis")
    print("=" * 60)
    
    # Extract all activity types
    activity_types = re.findall(r'<key>activityType</key>\s*<value>([^<]*)</value>', content)
    sub_activity_types = re.findall(r'<key>subActivityType</key>\s*<value>([^<]*)</value>', content)
    
    print(f"📋 Found Activity Types ({len(set(activity_types))} unique):")
    activity_counts = defaultdict(int)
    for activity in activity_types:
        activity_counts[activity] += 1
    
    for activity, count in sorted(activity_counts.items()):
        print(f"  - {activity}: {count} instances")
    
    print(f"\n📋 Found Sub-Activity Types ({len(set(sub_activity_types))} unique):")
    sub_activity_counts = defaultdict(int)
    for sub_activity in sub_activity_types:
        sub_activity_counts[sub_activity] += 1
    
    for sub_activity, count in sorted(sub_activity_counts.items()):
        print(f"  - {sub_activity}: {count} instances")
    
    # Extract component types (adapters)
    component_types = re.findall(r'<key>ComponentType</key>\s*<value>([^<]*)</value>', content)
    print(f"\n🔧 Found Component Types (Adapters) ({len(set(component_types))} unique):")
    component_counts = defaultdict(int)
    for component in component_types:
        component_counts[component] += 1
    
    for component, count in sorted(component_counts.items()):
        print(f"  - {component}: {count} instances")
    
    # Extract message protocols
    message_protocols = re.findall(r'<key>MessageProtocol</key>\s*<value>([^<]*)</value>', content)
    print(f"\n📡 Found Message Protocols ({len(set(message_protocols))} unique):")
    protocol_counts = defaultdict(int)
    for protocol in message_protocols:
        protocol_counts[protocol] += 1
    
    for protocol, count in sorted(protocol_counts.items()):
        print(f"  - {protocol}: {count} instances")
    
    # Extract transport protocols
    transport_protocols = re.findall(r'<key>TransportProtocol</key>\s*<value>([^<]*)</value>', content)
    print(f"\n🚚 Found Transport Protocols ({len(set(transport_protocols))} unique):")
    transport_counts = defaultdict(int)
    for transport in transport_protocols:
        transport_counts[transport] += 1
    
    for transport, count in sorted(transport_counts.items()):
        print(f"  - {transport}: {count} instances")
    
    # Extract cmdVariantUri patterns
    cmd_variants = re.findall(r'<key>cmdVariantUri</key>\s*<value>([^<]*)</value>', content)
    print(f"\n⚙️  Found Command Variant URIs ({len(set(cmd_variants))} unique):")
    for i, variant in enumerate(sorted(set(cmd_variants)), 1):
        print(f"  {i:2d}. {variant}")
    
    return {
        'activity_types': activity_counts,
        'sub_activity_types': sub_activity_counts,
        'component_types': component_counts,
        'message_protocols': protocol_counts,
        'transport_protocols': transport_counts,
        'cmd_variants': set(cmd_variants)
    }

def check_template_coverage():
    """Check what we have in our enhanced templates"""
    
    print("\n" + "=" * 60)
    print("🎯 Enhanced Template Coverage Analysis")
    print("=" * 60)
    
    # Check both template files
    enhanced_template_file = "enhanced_iflow_templates.py"
    bpmn_template_file = "bpmn_templates.py"
    
    # Analyze both template files
    all_template_methods = []
    all_template_activities = set()
    all_template_components = set()

    for template_file, file_name in [(enhanced_template_file, "Enhanced"), (bpmn_template_file, "BPMN")]:
        if os.path.exists(template_file):
            print(f"\n📋 Analyzing {file_name} Templates ({template_file}):")

            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()

            # Extract template methods
            template_methods = re.findall(r'def (\w+_template|.*_pattern)\(', template_content)
            all_template_methods.extend(template_methods)

            print(f"  Methods: {len(template_methods)}")

            # Extract activity types from templates
            template_activities = re.findall(r'<key>activityType</key>\s*<value>([^<]*)</value>', template_content)
            all_template_activities.update(template_activities)

            print(f"  Activity Types: {len(set(template_activities))}")

            # Extract component types from templates
            template_components = re.findall(r'<key>ComponentType</key>\s*<value>([^<]*)</value>', template_content)
            all_template_components.update(template_components)

            print(f"  Component Types: {len(set(template_components))}")
        else:
            print(f"⚠️  {file_name} template file not found: {template_file}")

    print(f"\n📊 Combined Template Analysis:")
    print(f"📋 Total Template Methods ({len(all_template_methods)}):")
    for i, method in enumerate(sorted(set(all_template_methods)), 1):
        print(f"  {i:2d}. {method}")

    print(f"\n🔧 All Activity Types in Templates ({len(all_template_activities)}):")
    for activity in sorted(all_template_activities):
        print(f"  - {activity}")

    print(f"\n📡 All Component Types in Templates ({len(all_template_components)}):")
    for component in sorted(all_template_components):
        print(f"  - {component}")
    
    return {
        'template_methods': all_template_methods,
        'template_activities': all_template_activities,
        'template_components': all_template_components
    }

def identify_gaps(artifacts_data, template_data):
    """Identify gaps between SAP artifacts and our templates"""
    
    print("\n" + "=" * 60)
    print("🚨 GAP ANALYSIS: Missing Templates")
    print("=" * 60)
    
    # Activity types we don't have templates for
    artifact_activities = set(artifacts_data['activity_types'].keys())
    template_activities = template_data['template_activities']
    
    missing_activities = artifact_activities - template_activities
    print(f"❌ Missing Activity Type Templates ({len(missing_activities)}):")
    for activity in sorted(missing_activities):
        count = artifacts_data['activity_types'][activity]
        print(f"  - {activity} ({count} instances in SAP)")
    
    # Component types we don't have templates for
    artifact_components = set(artifacts_data['component_types'].keys())
    template_components = template_data['template_components']
    
    missing_components = artifact_components - template_components
    print(f"\n❌ Missing Component Type Templates ({len(missing_components)}):")
    for component in sorted(missing_components):
        count = artifacts_data['component_types'][component]
        print(f"  - {component} ({count} instances in SAP)")
    
    # What we have covered
    covered_activities = artifact_activities & template_activities
    covered_components = artifact_components & template_components
    
    print(f"\n✅ Covered Activity Types ({len(covered_activities)}):")
    for activity in sorted(covered_activities):
        count = artifacts_data['activity_types'][activity]
        print(f"  - {activity} ({count} instances in SAP)")
    
    print(f"\n✅ Covered Component Types ({len(covered_components)}):")
    for component in sorted(covered_components):
        count = artifacts_data['component_types'][component]
        print(f"  - {component} ({count} instances in SAP)")
    
    # Calculate coverage percentage
    activity_coverage = len(covered_activities) / len(artifact_activities) * 100 if artifact_activities else 0
    component_coverage = len(covered_components) / len(artifact_components) * 100 if artifact_components else 0
    
    print(f"\n📊 Coverage Statistics:")
    print(f"  - Activity Types: {activity_coverage:.1f}% ({len(covered_activities)}/{len(artifact_activities)})")
    print(f"  - Component Types: {component_coverage:.1f}% ({len(covered_components)}/{len(artifact_components)})")
    
    return {
        'missing_activities': missing_activities,
        'missing_components': missing_components,
        'covered_activities': covered_activities,
        'covered_components': covered_components,
        'activity_coverage': activity_coverage,
        'component_coverage': component_coverage
    }

def main():
    """Main analysis function"""
    
    try:
        # Analyze SAP artifacts
        artifacts_data = analyze_all_artifacts()
        if not artifacts_data:
            return False
        
        # Check our template coverage
        template_data = check_template_coverage()
        
        # Identify gaps
        gap_analysis = identify_gaps(artifacts_data, template_data)
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 SUMMARY & RECOMMENDATIONS")
        print("=" * 60)
        
        if gap_analysis['activity_coverage'] > 80 and gap_analysis['component_coverage'] > 80:
            print("🎉 EXCELLENT: High template coverage!")
        elif gap_analysis['activity_coverage'] > 60 and gap_analysis['component_coverage'] > 60:
            print("✅ GOOD: Decent template coverage, some gaps to fill")
        else:
            print("⚠️  NEEDS WORK: Significant template gaps identified")
        
        print(f"\n📋 Priority Missing Templates:")
        
        # Show high-priority missing templates (those with multiple instances)
        high_priority_activities = [
            activity for activity in gap_analysis['missing_activities']
            if artifacts_data['activity_types'][activity] > 1
        ]
        
        if high_priority_activities:
            print(f"  🔥 High Priority Activity Types:")
            for activity in sorted(high_priority_activities):
                count = artifacts_data['activity_types'][activity]
                print(f"    - {activity} ({count} instances)")
        
        if gap_analysis['missing_components']:
            print(f"  🔥 Missing Component Types:")
            for component in sorted(gap_analysis['missing_components']):
                count = artifacts_data['component_types'][component]
                print(f"    - {component} ({count} instances)")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
