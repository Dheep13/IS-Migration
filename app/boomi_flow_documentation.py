#!/usr/bin/env python3
"""
Boomi Flow Documentation Generator

This module provides functionality to parse Boomi process XML files
and generate comprehensive documentation for migration to SAP Integration Suite.
"""

import os
import xml.etree.ElementTree as ET
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
# LLM Mermaid fixer available if needed
# from llm_mermaid_fixer import fix_documentation_with_llm

logger = logging.getLogger(__name__)

class BoomiFlowDocumentationGenerator:
    """Generator for Boomi process documentation"""
    
    def __init__(self):
        self.namespaces = {
            'bns': 'http://api.platform.boomi.com/',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
        self.parsed_processes = []
        self.parsed_maps = []
        self.parsed_connectors = []
    
    def process_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Process a directory containing Boomi XML files
        
        Args:
            directory_path (str): Path to directory containing Boomi files
            
        Returns:
            Dict containing processing results
        """
        try:
            logger.info(f"Processing Boomi directory: {directory_path}")
            
            # Find and process all XML files
            xml_files = self._find_xml_files(directory_path)
            logger.info(f"Found {len(xml_files)} XML files to process")
            
            results = {
                'total_files': len(xml_files),
                'processed_files': 0,
                'processes': [],
                'maps': [],
                'connectors': [],
                'errors': []
            }
            
            for xml_file in xml_files:
                try:
                    result = self._process_xml_file(xml_file)
                    if result:
                        if result['type'] == 'process':
                            results['processes'].append(result)
                        elif result['type'] == 'map':
                            results['maps'].append(result)
                        elif result['type'] == 'connector':
                            results['connectors'].append(result)
                        
                        results['processed_files'] += 1
                        
                except Exception as e:
                    error_msg = f"Error processing {xml_file}: {str(e)}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
            
            logger.info(f"Successfully processed {results['processed_files']} out of {results['total_files']} files")
            return results
            
        except Exception as e:
            logger.error(f"Error processing Boomi directory: {e}")
            raise
    
    def _find_xml_files(self, directory_path: str) -> List[str]:
        """Find all XML files in the directory"""
        xml_files = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.xml'):
                    xml_files.append(os.path.join(root, file))
        
        return xml_files

    def _split_xml_documents(self, content: str) -> List[str]:
        """Split content that may contain multiple XML documents"""
        import re

        # Find all XML declarations and split on them
        xml_pattern = r'<\?xml[^>]*\?>'
        parts = re.split(xml_pattern, content)

        # Remove empty parts and reconstruct XML documents
        xml_documents = []
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'

        for part in parts:
            part = part.strip()
            if part and part.startswith('<'):
                xml_documents.append(xml_declaration + part)

        # If no split occurred, return the original content
        if not xml_documents:
            xml_documents = [content.strip()]

        return xml_documents
    
    def _process_xml_file(self, xml_file_path: str) -> Optional[Dict[str, Any]]:
        """Process a single XML file"""
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Handle multiple XML documents in one file (common in Boomi exports)
            xml_documents = self._split_xml_documents(content)

            results = []
            for xml_doc in xml_documents:
                try:
                    root = ET.fromstring(xml_doc)

                    # Determine the type of Boomi component
                    component_type = self._determine_component_type(root)

                    if component_type == 'process':
                        result = self._parse_process(root, xml_file_path)
                    elif component_type == 'map':
                        result = self._parse_map(root, xml_file_path)
                    elif component_type == 'connector':
                        result = self._parse_connector(root, xml_file_path)
                    else:
                        logger.warning(f"Unknown component type '{component_type}' in {xml_file_path}")
                        continue

                    if result:
                        results.append(result)

                except ET.ParseError as e:
                    logger.error(f"XML parsing error in document from {xml_file_path}: {e}")
                    continue

            # Return the first valid result (or combine them if needed)
            return results[0] if results else None

        except Exception as e:
            logger.error(f"Error processing XML file {xml_file_path}: {e}")
            return None
    
    def _determine_component_type(self, root: ET.Element) -> str:
        """Determine the type of Boomi component"""
        # Check the type attribute on the Component element first
        component_type = root.get('type', '')

        if component_type == 'process':
            return 'process'
        elif component_type == 'transform.map':
            return 'map'
        elif component_type in ['connector-action', 'connector']:
            return 'connector'

        # Fallback: check for nested elements in bns:object
        bns_object = root.find('.//{http://api.platform.boomi.com/}object')
        if bns_object is not None:
            # Check for process element
            if bns_object.find('process') is not None:
                return 'process'
            # Check for Map element
            elif bns_object.find('Map') is not None:
                return 'map'
            # Check for Operation element
            elif bns_object.find('Operation') is not None:
                return 'connector'

        # Additional fallback checks
        if root.find('.//process') is not None:
            return 'process'
        elif root.find('.//Map') is not None:
            return 'map'
        elif root.find('.//Operation') is not None:
            return 'connector'

        logger.warning(f"Unknown component type: {component_type}")
        return 'unknown'
    
    def _parse_process(self, root: ET.Element, file_path: str) -> Dict[str, Any]:
        """Parse a Boomi process component"""
        component_info = self._extract_component_info(root)

        # Look for process element in bns:object first
        bns_object = root.find('.//{http://api.platform.boomi.com/}object')
        process_elem = None

        if bns_object is not None:
            process_elem = bns_object.find('process')

        # Fallback to direct search
        if process_elem is None:
            process_elem = root.find('.//process')

        if process_elem is None:
            logger.warning(f"No process element found in {file_path}")
            return None
        
        shapes = self._extract_shapes(process_elem)
        connections = self._extract_connections(shapes)
        
        return {
            'type': 'process',
            'file_path': file_path,
            'component': component_info,
            'process': {
                'allow_simultaneous': process_elem.get('allowSimultaneous'),
                'enable_user_log': process_elem.get('enableUserLog'),
                'process_log_on_error_only': process_elem.get('processLogOnErrorOnly'),
                'workload': process_elem.get('workload'),
                'shapes': shapes,
                'connections': connections
            },
            'integration_patterns': self._identify_integration_patterns(root)
        }
    
    def _parse_map(self, root: ET.Element, file_path: str) -> Dict[str, Any]:
        """Parse a Boomi map component"""
        component_info = self._extract_component_info(root)

        # Look for Map element in bns:object first
        bns_object = root.find('.//{http://api.platform.boomi.com/}object')
        map_elem = None

        if bns_object is not None:
            map_elem = bns_object.find('Map')

        # Fallback to direct search
        if map_elem is None:
            map_elem = root.find('.//Map')

        if map_elem is None:
            logger.warning(f"No Map element found in {file_path}")
            return None
        
        mappings = []
        for mapping in map_elem.findall('.//Mapping'):
            mappings.append({
                'from_key': mapping.get('fromKey'),
                'from_type': mapping.get('fromType'),
                'to_key': mapping.get('toKey'),
                'to_name_path': mapping.get('toNamePath'),
                'to_type': mapping.get('toType')
            })
        
        return {
            'type': 'map',
            'file_path': file_path,
            'component': component_info,
            'map': {
                'from_profile': map_elem.get('fromProfile'),
                'to_profile': map_elem.get('toProfile'),
                'mappings': mappings
            }
        }
    
    def _parse_connector(self, root: ET.Element, file_path: str) -> Dict[str, Any]:
        """Parse a Boomi connector component"""
        component_info = self._extract_component_info(root)

        # Look for Operation element in bns:object first
        bns_object = root.find('.//{http://api.platform.boomi.com/}object')
        operation = None

        if bns_object is not None:
            operation = bns_object.find('Operation')

        # Fallback to direct search
        if operation is None:
            operation = root.find('.//Operation')

        if operation is None:
            logger.warning(f"No Operation element found in {file_path}")
            return None
        
        config = operation.find('Configuration')
        connector_info = {'type': 'generic'}
        
        if config is not None:
            # Extract Salesforce-specific configuration
            sf_action = config.find('SalesforceSendAction')
            if sf_action is not None:
                connector_info = {
                    'type': 'salesforce',
                    'object_action': sf_action.get('objectAction'),
                    'object_name': sf_action.get('objectName'),
                    'batch_size': sf_action.get('batchSize'),
                    'use_bulk_api': sf_action.get('useBulkAPI') == 'true'
                }
        
        return {
            'type': 'connector',
            'file_path': file_path,
            'component': component_info,
            'connector': connector_info
        }
    
    def _extract_component_info(self, root: ET.Element) -> Dict[str, Any]:
        """Extract basic component information"""
        return {
            'id': root.get('componentId'),
            'name': root.get('name'),
            'type': root.get('type'),
            'version': root.get('version'),
            'created_by': root.get('createdBy'),
            'created_date': root.get('createdDate'),
            'modified_by': root.get('modifiedBy'),
            'modified_date': root.get('modifiedDate'),
            'folder_path': root.get('folderFullPath'),
            'description': self._get_description(root)
        }
    
    def _extract_shapes(self, process_elem: ET.Element) -> List[Dict[str, Any]]:
        """Extract shape information from process"""
        shapes = []

        # Look for shapes container first
        shapes_container = process_elem.find('shapes')
        if shapes_container is not None:
            shape_elements = shapes_container.findall('shape')
        else:
            # Fallback to direct search
            shape_elements = process_elem.findall('shape')
            if not shape_elements:
                shape_elements = process_elem.findall('.//shape')

        for shape in shape_elements:
            shape_info = {
                'name': shape.get('name'),
                'type': shape.get('shapetype'),
                'image': shape.get('image'),
                'user_label': shape.get('userlabel'),
                'position': {
                    'x': float(shape.get('x', 0)),
                    'y': float(shape.get('y', 0))
                },
                'configuration': self._extract_shape_configuration(shape)
            }
            
            # Extract drag points (connections)
            dragpoints = []
            # Look for dragpoints container first
            dragpoints_container = shape.find('dragpoints')
            if dragpoints_container is not None:
                dragpoint_elements = dragpoints_container.findall('dragpoint')
            else:
                # Fallback to direct search
                dragpoint_elements = shape.findall('dragpoint')
                if not dragpoint_elements:
                    dragpoint_elements = shape.findall('.//dragpoint')

            for dragpoint in dragpoint_elements:
                dragpoints.append({
                    'name': dragpoint.get('name'),
                    'to_shape': dragpoint.get('toShape'),
                    'position': {
                        'x': float(dragpoint.get('x', 0)),
                        'y': float(dragpoint.get('y', 0))
                    }
                })
            shape_info['dragpoints'] = dragpoints
            
            shapes.append(shape_info)
        
        return shapes
    
    def _extract_shape_configuration(self, shape: ET.Element) -> Dict[str, Any]:
        """Extract configuration from a shape"""
        config = {}
        config_elem = shape.find('configuration')
        
        if config_elem is not None:
            # Extract connector actions
            connector_action = config_elem.find('connectoraction')
            if connector_action is not None:
                config['connector_action'] = {
                    'action_type': connector_action.get('actionType'),
                    'connector_type': connector_action.get('connectorType'),
                    'connection_id': connector_action.get('connectionId'),
                    'operation_id': connector_action.get('operationId')
                }
            
            # Extract map configuration
            map_elem = config_elem.find('map')
            if map_elem is not None:
                config['map'] = {
                    'map_id': map_elem.get('mapId')
                }
            
            # Extract document properties
            doc_props = config_elem.find('documentproperties')
            if doc_props is not None:
                config['document_properties'] = self._extract_document_properties(doc_props)
        
        return config
    
    def _extract_document_properties(self, doc_props: ET.Element) -> List[Dict[str, Any]]:
        """Extract document properties configuration"""
        properties = []
        
        for prop in doc_props.findall('documentproperty'):
            prop_info = {
                'name': prop.get('name'),
                'property_id': prop.get('propertyId'),
                'default_value': prop.get('defaultValue'),
                'persist': prop.get('persist') == 'true',
                'is_dynamic_credential': prop.get('isDynamicCredential') == 'true'
            }
            properties.append(prop_info)
        
        return properties
    
    def _extract_connections(self, shapes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract connections between shapes"""
        connections = []
        
        for shape in shapes:
            for dragpoint in shape.get('dragpoints', []):
                if dragpoint.get('to_shape'):
                    connections.append({
                        'from_shape': shape['name'],
                        'to_shape': dragpoint['to_shape'],
                        'from_position': dragpoint['position'],
                        'connection_type': 'flow'
                    })
        
        return connections
    
    def _identify_integration_patterns(self, root: ET.Element) -> List[str]:
        """Identify common integration patterns in the Boomi process"""
        patterns = []
        
        # Check for common patterns based on component types and configurations
        if root.find('.//connectoraction[@actionType="Listen"]') is not None:
            patterns.append('event_listener')
        
        if root.find('.//connectoraction[@actionType="Send"]') is not None:
            patterns.append('data_sender')
        
        if root.find('.//Map') is not None:
            patterns.append('data_transformation')
        
        if root.find('.//documentproperties') is not None:
            patterns.append('dynamic_properties')
        
        if root.find('.//SalesforceSendAction') is not None:
            patterns.append('salesforce_integration')
        
        return patterns
    
    def _get_description(self, root: ET.Element) -> str:
        """Extract description from component"""
        # Try with namespace first
        desc_elem = root.find('.//{http://api.platform.boomi.com/}description')
        if desc_elem is not None:
            return desc_elem.text or ""

        # Fallback to direct search
        desc_elem = root.find('.//description')
        return desc_elem.text if desc_elem is not None else ""
    
    def generate_documentation(self, processing_results: Dict[str, Any]) -> str:
        """Generate comprehensive markdown documentation from processing results"""
        doc_lines = []
        
        # Header
        doc_lines.append("# Boomi Integration Documentation")
        doc_lines.append("")
        doc_lines.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc_lines.append("")
        
        # Summary
        doc_lines.append("## Summary")
        doc_lines.append("")
        doc_lines.append(f"- **Total Files Processed:** {processing_results['processed_files']}")
        doc_lines.append(f"- **Processes:** {len(processing_results['processes'])}")
        doc_lines.append(f"- **Maps:** {len(processing_results['maps'])}")
        doc_lines.append(f"- **Connectors:** {len(processing_results['connectors'])}")
        if processing_results['errors']:
            doc_lines.append(f"- **Errors:** {len(processing_results['errors'])}")
        doc_lines.append("")
        
        # Processes
        if processing_results['processes']:
            doc_lines.append("## Boomi Processes")
            doc_lines.append("")
            
            for i, process in enumerate(processing_results['processes'], 1):
                component = process['component']
                process_info = process['process']
                
                doc_lines.append(f"### {i}. {component.get('name', 'Unnamed Process')}")
                doc_lines.append("")
                
                if component.get('description'):
                    doc_lines.append(f"**Description:** {component['description']}")
                    doc_lines.append("")
                
                # Component details
                doc_lines.append("#### Component Information")
                doc_lines.append("")
                doc_lines.append(f"- **Type:** {component.get('type', 'Unknown')}")
                doc_lines.append(f"- **Version:** {component.get('version', 'Unknown')}")
                doc_lines.append(f"- **Created By:** {component.get('created_by', 'Unknown')}")
                doc_lines.append(f"- **Folder Path:** {component.get('folder_path', 'Unknown')}")
                doc_lines.append("")
                
                # Integration patterns
                if process.get('integration_patterns'):
                    doc_lines.append("#### Integration Patterns")
                    doc_lines.append("")
                    for pattern in process['integration_patterns']:
                        doc_lines.append(f"- {pattern.replace('_', ' ').title()}")
                    doc_lines.append("")
                
                # Process flow
                doc_lines.append("#### Process Flow")
                doc_lines.append("")
                doc_lines.append(self._generate_flow_diagram(process_info['shapes'], process_info['connections']))
                doc_lines.append("")
        
        # Maps
        if processing_results['maps']:
            doc_lines.append("## Data Mappings")
            doc_lines.append("")
            
            for i, map_info in enumerate(processing_results['maps'], 1):
                component = map_info['component']
                map_data = map_info['map']
                
                doc_lines.append(f"### {i}. {component.get('name', 'Unnamed Map')}")
                doc_lines.append("")
                
                doc_lines.append("| From | To | Type |")
                doc_lines.append("|------|----|----- |")
                for mapping in map_data.get('mappings', []):
                    from_path = mapping.get('from_key', 'Unknown')
                    to_path = mapping.get('to_name_path', 'Unknown')
                    mapping_type = mapping.get('to_type', 'Unknown')
                    doc_lines.append(f"| {from_path} | {to_path} | {mapping_type} |")
                doc_lines.append("")
        
        # Connectors
        if processing_results['connectors']:
            doc_lines.append("## Connectors")
            doc_lines.append("")
            
            for i, connector in enumerate(processing_results['connectors'], 1):
                component = connector['component']
                connector_info = connector['connector']
                
                doc_lines.append(f"### {i}. {component.get('name', 'Unnamed Connector')}")
                doc_lines.append("")
                doc_lines.append(f"- **Type:** {connector_info.get('type', 'Unknown')}")
                if connector_info.get('object_name'):
                    doc_lines.append(f"- **Object:** {connector_info['object_name']}")
                if connector_info.get('object_action'):
                    doc_lines.append(f"- **Action:** {connector_info['object_action']}")
                doc_lines.append("")
        
        # Errors
        if processing_results['errors']:
            doc_lines.append("## Processing Errors")
            doc_lines.append("")
            for error in processing_results['errors']:
                doc_lines.append(f"- {error}")
            doc_lines.append("")
        
        return "\n".join(doc_lines)
    
    def _generate_flow_diagram(self, shapes: List[Dict[str, Any]], connections: List[Dict[str, Any]]) -> str:
        """Generate a text-based flow diagram"""
        diagram_lines = ["```mermaid", "graph TD"]
        
        # Add shapes
        for shape in shapes:
            shape_name = shape['name']
            shape_type = shape['type']
            label = shape.get('user_label') or shape_name
            
            if shape_type == 'start':
                diagram_lines.append(f"    {shape_name}([{label}])")
            elif shape_type == 'stop':
                diagram_lines.append(f"    {shape_name}([{label}])")
            elif shape_type == 'connectoraction':
                diagram_lines.append(f"    {shape_name}[{label}]")
            elif shape_type == 'map':
                diagram_lines.append(f"    {shape_name}{{Transform: {label}}}")
            else:
                diagram_lines.append(f"    {shape_name}[{label}]")
        
        # Add connections
        for connection in connections:
            from_shape = connection['from_shape']
            to_shape = connection['to_shape']
            diagram_lines.append(f"    {from_shape} --> {to_shape}")
        
        diagram_lines.append("```")
        return "\n".join(diagram_lines)
