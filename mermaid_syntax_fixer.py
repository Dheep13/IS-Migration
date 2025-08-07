#!/usr/bin/env python3
"""
Mermaid Syntax Validator and Fixer

This script validates and fixes common Mermaid diagram syntax errors in HTML files.
It can be used as a post-processing step after document generation.
"""

import re
import os
import sys
import argparse
from typing import List, Tuple, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MermaidSyntaxFixer:
    """Class to validate and fix Mermaid diagram syntax errors"""
    
    def __init__(self):
        self.common_fixes = {
            # Fix invalid node connections to subgraphs
            r'(\w+)\s*\.?-\.?->\s*(\w+)\s*\n.*?subgraph\s+\2': self._fix_subgraph_connection,
            # Fix invalid characters in node IDs
            r'([A-Za-z0-9_]+)([^A-Za-z0-9_\[\](){}"\'`\s\-\>])+': self._fix_node_id,
            # Fix missing quotes in labels with special characters
            r'\[([^\]]*[&<>].*?)\]': self._fix_special_chars_in_labels,
            # Fix invalid edge syntax
            r'(\w+)\s*-+>\s*\|([^|]*)\|\s*(\w+)': r'\1 -->|\2| \3',
        }
    
    def validate_and_fix_html_file(self, html_file_path: str, output_path: str = None) -> bool:
        """
        Validate and fix Mermaid diagrams in an HTML file
        
        Args:
            html_file_path: Path to the HTML file
            output_path: Optional output path (defaults to overwriting input)
            
        Returns:
            bool: True if fixes were applied, False otherwise
        """
        if not os.path.exists(html_file_path):
            logger.error(f"File not found: {html_file_path}")
            return False
        
        logger.info(f"Processing HTML file: {html_file_path}")
        
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract and fix Mermaid diagrams
        fixed_content, fixes_applied = self._fix_mermaid_diagrams_in_html(html_content)
        
        if fixes_applied:
            # Write the fixed content
            output_file = output_path or html_file_path
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            logger.info(f"✅ Applied {fixes_applied} fixes to {output_file}")
            return True
        else:
            logger.info("✅ No syntax errors found in Mermaid diagrams")
            return False
    
    def _fix_mermaid_diagrams_in_html(self, html_content: str) -> Tuple[str, int]:
        """Extract and fix all Mermaid diagrams in HTML content"""
        fixes_applied = 0
        
        # Pattern to match Mermaid diagrams in HTML
        mermaid_pattern = r'<pre class="mermaid">\s*(.*?)\s*</pre>'
        
        def fix_diagram(match):
            nonlocal fixes_applied
            diagram_content = match.group(1)
            
            logger.info("🔍 Validating Mermaid diagram...")
            fixed_diagram, diagram_fixes = self._fix_mermaid_syntax(diagram_content)
            
            if diagram_fixes > 0:
                fixes_applied += diagram_fixes
                logger.info(f"🔧 Applied {diagram_fixes} fixes to diagram")
                return f'<pre class="mermaid">\n{fixed_diagram}\n</pre>'
            
            return match.group(0)
        
        fixed_html = re.sub(mermaid_pattern, fix_diagram, html_content, flags=re.DOTALL)
        return fixed_html, fixes_applied
    
    def _fix_mermaid_syntax(self, diagram_content: str) -> Tuple[str, int]:
        """Fix syntax errors in a single Mermaid diagram"""
        fixes_applied = 0
        fixed_content = diagram_content

        # Fix 1: Remove problematic subgraph connections
        if 'subgraph' in fixed_content and '-.-> SubProcesses' in fixed_content:
            logger.info("🔧 Fixing subgraph connection issue")
            fixed_content = self._fix_main_process_flow(fixed_content)
            fixes_applied += 1

        # Fix 2: Fix disconnected flows (multiple Start connections)
        fixed_content, flow_fixes = self._fix_disconnected_flows(fixed_content)
        fixes_applied += flow_fixes

        # Fix 3: Remove disconnected subgraphs
        fixed_content, subgraph_fixes = self._remove_disconnected_subgraphs(fixed_content)
        fixes_applied += subgraph_fixes

        # Fix 4: Validate node IDs
        fixed_content, node_fixes = self._fix_node_ids(fixed_content)
        fixes_applied += node_fixes

        # Fix 5: Fix edge syntax
        fixed_content, edge_fixes = self._fix_edge_syntax(fixed_content)
        fixes_applied += edge_fixes

        # Fix 6: Remove duplicate class definitions
        fixed_content, class_fixes = self._remove_duplicate_class_definitions(fixed_content)
        fixes_applied += class_fixes

        # Fix 7: Fix orphaned nodes (disabled - was removing needed definitions)
        # fixed_content, orphan_fixes = self._fix_orphaned_nodes(fixed_content)
        # fixes_applied += orphan_fixes

        return fixed_content, fixes_applied
    
    def _fix_main_process_flow(self, content: str) -> str:
        """Fix the specific main process flow diagram issue"""
        # Remove the problematic subgraph and its connection
        lines = content.split('\n')
        fixed_lines = []
        in_subgraph = False
        
        for line in lines:
            # Skip subgraph definition and its contents
            if 'subgraph SubProcesses' in line:
                in_subgraph = True
                continue
            elif in_subgraph and line.strip() == 'end':
                in_subgraph = False
                continue
            elif in_subgraph:
                continue
            # Skip the problematic connection
            elif '-.-> SubProcesses' in line:
                continue
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_disconnected_flows(self, content: str) -> Tuple[str, int]:
        """Fix disconnected flows, especially multiple Start node connections and undefined references"""
        fixes = 0
        lines = content.split('\n')
        fixed_lines = []

        # Find all node definitions and references
        defined_nodes = set()
        referenced_nodes = set()

        # First pass: collect all defined nodes and references
        for line in lines:
            line_stripped = line.strip()

            # Find node definitions (nodes with shapes)
            node_match = re.match(r'(\w+)(\[|\{|\()', line_stripped)
            if node_match:
                defined_nodes.add(node_match.group(1))

            # Find node references in connections
            if '-->' in line_stripped:
                parts = line_stripped.split('-->')
                if len(parts) >= 2:
                    # Source node
                    source = parts[0].strip().split()[0]
                    referenced_nodes.add(source)

                    # Target node (remove labels)
                    target_part = parts[1].strip()
                    target_part = re.sub(r'\|[^|]*\|', '', target_part)
                    target = target_part.split()[0]
                    referenced_nodes.add(target)

        # Find undefined references
        undefined_refs = referenced_nodes - defined_nodes

        if undefined_refs:
            logger.info(f"🔧 Fixing {len(undefined_refs)} undefined node references: {undefined_refs}")

            # Add missing node definitions or fix references
            for line in lines:
                line_stripped = line.strip()

                # Check if this line references an undefined node
                needs_fix = False
                for undefined in undefined_refs:
                    if line_stripped.startswith(f"{undefined} -->") or f"--> {undefined}" in line_stripped:
                        needs_fix = True
                        break

                if needs_fix:
                    # Try to fix common naming issues
                    fixed_line = line
                    for undefined in undefined_refs:
                        # Common fix: SendFilesCheck -> SendFilesToVendor
                        if 'SendFilesCheck' in undefined:
                            fixed_line = fixed_line.replace('SendFilesCheck', 'SendFilesToVendor')
                            fixes += 1
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
        else:
            # Handle multiple Start connections
            start_connections = []
            for line in lines:
                if line.strip().startswith('Start') and '-->' in line:
                    start_connections.append(line.strip())

            if len(start_connections) > 1:
                logger.info(f"🔧 Fixing {len(start_connections)} disconnected Start connections")

                # Keep only the first Start connection, remove others
                kept_connection = None
                for line in lines:
                    line_stripped = line.strip()

                    if line_stripped.startswith('Start') and '-->' in line_stripped:
                        if kept_connection is None:
                            kept_connection = line_stripped
                            fixed_lines.append(line)
                        else:
                            # Skip this duplicate Start connection
                            fixes += 1
                            continue
                    else:
                        fixed_lines.append(line)
            else:
                fixed_lines = lines

        return '\n'.join(fixed_lines), fixes

    def _remove_disconnected_subgraphs(self, content: str) -> Tuple[str, int]:
        """Remove subgraphs that are not properly connected"""
        fixes = 0
        # This is a placeholder for more sophisticated subgraph validation
        return content, fixes
    
    def _fix_node_ids(self, content: str) -> Tuple[str, int]:
        """Fix invalid characters in node IDs"""
        fixes = 0
        # Replace invalid characters in node IDs
        pattern = r'([A-Za-z][A-Za-z0-9_]*)[^A-Za-z0-9_\[\](){}"\'`\s\-\>]*(\[|\{|\()'
        
        def replace_invalid_chars(match):
            nonlocal fixes
            fixes += 1
            return f"{match.group(1)}{match.group(2)}"
        
        fixed_content = re.sub(pattern, replace_invalid_chars, content)
        return fixed_content, fixes
    
    def _fix_edge_syntax(self, content: str) -> Tuple[str, int]:
        """Fix common edge syntax errors"""
        fixes = 0
        
        # Fix arrow syntax
        patterns = [
            (r'(\w+)\s*-+>\s*\|([^|]*)\|\s*(\w+)', r'\1 -->|\2| \3'),
            (r'(\w+)\s*-+\.\s*-+>\s*(\w+)', r'\1 -.-> \2'),
        ]
        
        fixed_content = content
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, fixed_content)
            if new_content != fixed_content:
                fixes += 1
                fixed_content = new_content
        
        return fixed_content, fixes
    
    def _remove_duplicate_class_definitions(self, content: str) -> Tuple[str, int]:
        """Remove duplicate classDef statements"""
        fixes = 0
        lines = content.split('\n')
        seen_classes = set()
        fixed_lines = []
        
        for line in lines:
            if line.strip().startswith('classDef'):
                class_name = line.split()[1] if len(line.split()) > 1 else None
                if class_name and class_name in seen_classes:
                    fixes += 1
                    continue
                elif class_name:
                    seen_classes.add(class_name)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines), fixes

    def _fix_orphaned_nodes(self, content: str) -> Tuple[str, int]:
        """Fix orphaned nodes by adding missing definitions instead of removing them"""
        fixes = 0
        lines = content.split('\n')

        # Find all node references in connections
        referenced_nodes = set()
        defined_nodes = set()

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('%%') or line.startswith('classDef'):
                continue

            # Find node definitions (nodes with shapes)
            node_match = re.match(r'(\w+)(\[|\{|\()', line)
            if node_match:
                defined_nodes.add(node_match.group(1))

            # Find connections and extract referenced nodes
            if '-->' in line:
                parts = line.split('-->')
                if len(parts) >= 2:
                    # Extract source node
                    source = parts[0].strip().split()[0]
                    referenced_nodes.add(source)

                    # Extract target node (remove labels)
                    target_part = parts[1].strip()
                    target_part = re.sub(r'\|[^|]*\|', '', target_part)
                    target = target_part.split()[0]
                    referenced_nodes.add(target)

        # Find missing node definitions
        missing_definitions = referenced_nodes - defined_nodes

        if missing_definitions:
            logger.info(f"🔧 Adding {len(missing_definitions)} missing node definitions")

            # Add missing node definitions before the first connection
            fixed_lines = []
            first_connection_added = False

            for line in lines:
                # Add missing definitions before the first connection
                if '-->' in line and not first_connection_added:
                    # Add missing node definitions
                    for node in sorted(missing_definitions):
                        if node.endswith(':::event') or 'End' in node or 'Start' in node:
                            fixed_lines.append(f"{node.split(':::')[0]}((End)):::event")
                        elif ':::router' in node or '{' in node:
                            fixed_lines.append(f"{node.split(':::')[0]}{{{node.split(':::')[0]}}}:::router")
                        elif ':::contentModifier' in node or '[' in node:
                            fixed_lines.append(f"{node.split(':::')[0]}[{node.split(':::')[0]}]:::contentModifier")
                        else:
                            # Default to rectangle
                            fixed_lines.append(f"{node}[{node}]")
                        fixes += 1

                    fixed_lines.append("")  # Add blank line
                    first_connection_added = True

                fixed_lines.append(line)

            return '\n'.join(fixed_lines), fixes

        return content, fixes

    def _fix_subgraph_connection(self, match):
        """Fix invalid subgraph connections"""
        # Remove the connection entirely
        return ""
    
    def _fix_node_id(self, match):
        """Fix invalid node ID characters"""
        return match.group(1)
    
    def _fix_special_chars_in_labels(self, match):
        """Fix special characters in labels by adding quotes"""
        label = match.group(1)
        return f'["{label}"]'

def auto_fix_html_file(html_file_path: str) -> bool:
    """
    Convenience function to automatically fix Mermaid syntax in an HTML file

    Args:
        html_file_path: Path to the HTML file to fix

    Returns:
        bool: True if fixes were applied, False otherwise
    """
    fixer = MermaidSyntaxFixer()
    return fixer.validate_and_fix_html_file(html_file_path)

def main():
    parser = argparse.ArgumentParser(description='Fix Mermaid syntax errors in HTML files')
    parser.add_argument('input_file', help='Input HTML file path')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--batch', '-b', help='Process all HTML files in directory')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    fixer = MermaidSyntaxFixer()

    try:
        if args.batch:
            # Process all HTML files in directory
            import glob
            html_files = glob.glob(os.path.join(args.batch, "*.html"))
            total_fixes = 0

            for html_file in html_files:
                logger.info(f"Processing: {html_file}")
                success = fixer.validate_and_fix_html_file(html_file)
                if success:
                    total_fixes += 1

            print(f"✅ Processed {len(html_files)} files, applied fixes to {total_fixes} files")
        else:
            # Process single file
            success = fixer.validate_and_fix_html_file(args.input_file, args.output)

            if success:
                print("✅ Mermaid syntax fixes applied successfully!")
            else:
                print("✅ No syntax errors found.")

    except Exception as e:
        logger.error(f"❌ Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
