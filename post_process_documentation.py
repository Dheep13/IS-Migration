#!/usr/bin/env python3
"""
Post-processing utilities for generated documentation

This module provides functions to automatically fix common issues in generated documentation,
particularly Mermaid syntax errors.
"""

import os
import sys
import logging
from typing import Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from minimal_mermaid_fixer import fix_mermaid_syntax_errors
except ImportError:
    try:
        from mermaid_syntax_fixer import auto_fix_html_file as fix_mermaid_syntax_errors
    except ImportError:
        print("Warning: mermaid syntax fixer not available")
        fix_mermaid_syntax_errors = None

# Component mapping improvement is now handled at source in documentation_enhancer.py

logger = logging.getLogger(__name__)

def post_process_html_documentation(html_file_path: str,
                                  fix_mermaid: bool = True,
                                  validate_html: bool = True) -> bool:
    """
    Post-process generated HTML documentation to fix common issues

    Args:
        html_file_path: Path to the HTML file to process
        fix_mermaid: Whether to fix Mermaid syntax errors
        validate_html: Whether to validate HTML structure

    Returns:
        bool: True if any fixes were applied, False otherwise
    """
    if not os.path.exists(html_file_path):
        logger.error(f"HTML file not found: {html_file_path}")
        return False
    
    fixes_applied = False
    
    # Fix Mermaid syntax errors
    if fix_mermaid and fix_mermaid_syntax_errors:
        try:
            logger.info("🔧 Fixing Mermaid syntax errors...")
            mermaid_fixes = fix_mermaid_syntax_errors(html_file_path)
            if mermaid_fixes:
                logger.info("✅ Mermaid syntax fixes applied")
                fixes_applied = True
            else:
                logger.info("✅ No Mermaid syntax errors found")
        except Exception as e:
            logger.warning(f"⚠️ Could not fix Mermaid syntax: {e}")

    # Component mapping improvement is now handled at source in documentation_enhancer.py

    # Basic HTML validation
    if validate_html:
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for basic HTML structure
            if not content.strip().startswith('<!DOCTYPE html>'):
                logger.warning("⚠️ HTML file missing DOCTYPE declaration")
            
            # Count Mermaid diagrams
            mermaid_count = content.count('<pre class="mermaid">')
            if mermaid_count > 0:
                logger.info(f"📊 Found {mermaid_count} Mermaid diagrams")
            
            # Check file size
            file_size = len(content)
            logger.info(f"📄 HTML file size: {file_size:,} characters")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not validate HTML: {e}")
    
    return fixes_applied

def integrate_with_boomi_generator():
    """
    Integration function that can be called from the Boomi documentation generator
    """
    def post_process_wrapper(html_file_path: str) -> None:
        """Wrapper function for easy integration"""
        try:
            post_process_html_documentation(html_file_path)
        except Exception as e:
            logger.warning(f"Post-processing failed: {e}")
    
    return post_process_wrapper

# Convenience function for direct import
def fix_mermaid_in_html(html_file_path: str) -> bool:
    """
    Simple function to fix Mermaid syntax in an HTML file

    Args:
        html_file_path: Path to the HTML file

    Returns:
        bool: True if fixes were applied
    """
    if fix_mermaid_syntax_errors:
        return fix_mermaid_syntax_errors(html_file_path)
    else:
        logger.warning("Mermaid syntax fixer not available")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Post-process HTML documentation')
    parser.add_argument('html_file', help='HTML file to process')
    parser.add_argument('--no-mermaid', action='store_true', help='Skip Mermaid fixes')
    parser.add_argument('--no-validation', action='store_true', help='Skip HTML validation')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    success = post_process_html_documentation(
        args.html_file,
        fix_mermaid=not args.no_mermaid,
        validate_html=not args.no_validation
    )
    
    if success:
        print("✅ Post-processing completed with fixes applied")
    else:
        print("✅ Post-processing completed, no fixes needed")
