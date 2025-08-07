#!/usr/bin/env python3
"""
Enhanced Documentation Generator with Automatic Mermaid Syntax Fixing

This script generates documentation and automatically fixes any Mermaid syntax errors.
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from mermaid_syntax_fixer import auto_fix_html_file
    from markdown_to_html_converter import convert_markdown_to_html
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedDocumentationGenerator:
    """Enhanced documentation generator with automatic Mermaid fixing"""
    
    def __init__(self):
        self.temp_files = []
    
    def generate_documentation_with_fixes(self, markdown_file: str, output_file: str = None, 
                                        custom_title: str = None) -> str:
        """
        Generate HTML documentation from markdown and automatically fix Mermaid syntax
        
        Args:
            markdown_file: Path to the markdown file
            output_file: Optional output HTML file path
            custom_title: Optional custom title for the document
            
        Returns:
            str: Path to the generated and fixed HTML file
        """
        logger.info("🚀 Starting enhanced documentation generation...")
        
        # Step 1: Convert markdown to HTML
        logger.info("📝 Converting markdown to HTML...")
        try:
            html_file = convert_markdown_to_html(markdown_file, output_file, custom_title)
            logger.info(f"✅ HTML generated: {html_file}")
        except Exception as e:
            logger.error(f"❌ Error converting markdown to HTML: {e}")
            raise
        
        # Step 2: Fix Mermaid syntax errors
        logger.info("🔧 Fixing Mermaid syntax errors...")
        try:
            fixes_applied = auto_fix_html_file(html_file)
            if fixes_applied:
                logger.info("✅ Mermaid syntax fixes applied successfully!")
            else:
                logger.info("✅ No Mermaid syntax errors found")
        except Exception as e:
            logger.error(f"❌ Error fixing Mermaid syntax: {e}")
            # Don't fail the entire process for Mermaid fixes
            logger.warning("⚠️ Continuing with unfixed Mermaid diagrams...")
        
        # Step 3: Validate the final HTML
        if os.path.exists(html_file):
            file_size = os.path.getsize(html_file)
            logger.info(f"📊 Final HTML file size: {file_size:,} bytes")
            
            # Basic validation
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                mermaid_count = content.count('<pre class="mermaid">')
                logger.info(f"📈 Mermaid diagrams found: {mermaid_count}")
        
        logger.info("🎉 Enhanced documentation generation completed!")
        return html_file
    
    def batch_process_directory(self, directory: str, pattern: str = "*.md") -> list:
        """
        Process all markdown files in a directory
        
        Args:
            directory: Directory containing markdown files
            pattern: File pattern to match (default: *.md)
            
        Returns:
            list: List of generated HTML files
        """
        import glob
        
        logger.info(f"🔍 Searching for markdown files in: {directory}")
        markdown_files = glob.glob(os.path.join(directory, pattern))
        
        if not markdown_files:
            logger.warning(f"⚠️ No markdown files found matching pattern: {pattern}")
            return []
        
        logger.info(f"📚 Found {len(markdown_files)} markdown files")
        generated_files = []
        
        for md_file in markdown_files:
            try:
                logger.info(f"📝 Processing: {os.path.basename(md_file)}")
                html_file = self.generate_documentation_with_fixes(md_file)
                generated_files.append(html_file)
                logger.info(f"✅ Generated: {os.path.basename(html_file)}")
            except Exception as e:
                logger.error(f"❌ Error processing {md_file}: {e}")
                continue
        
        logger.info(f"🎉 Batch processing completed! Generated {len(generated_files)} HTML files")
        return generated_files
    
    def cleanup_temp_files(self):
        """Clean up any temporary files created during processing"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.debug(f"🗑️ Cleaned up temp file: {temp_file}")
            except Exception as e:
                logger.warning(f"⚠️ Could not clean up {temp_file}: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Enhanced Documentation Generator with Mermaid Syntax Fixing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate documentation from a single markdown file
  python enhanced_documentation_generator.py input.md
  
  # Generate with custom output file and title
  python enhanced_documentation_generator.py input.md -o output.html -t "My Documentation"
  
  # Batch process all markdown files in a directory
  python enhanced_documentation_generator.py --batch ./docs/
  
  # Process with verbose output
  python enhanced_documentation_generator.py input.md --verbose
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input markdown file or directory (for batch mode)')
    parser.add_argument('--output', '-o', help='Output HTML file path')
    parser.add_argument('--title', '-t', help='Custom title for the HTML document')
    parser.add_argument('--batch', '-b', action='store_true', help='Batch process directory')
    parser.add_argument('--pattern', '-p', default='*.md', help='File pattern for batch mode (default: *.md)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.input:
        parser.print_help()
        sys.exit(1)
    
    generator = EnhancedDocumentationGenerator()
    
    try:
        if args.batch:
            # Batch mode
            if not os.path.isdir(args.input):
                logger.error(f"❌ Directory not found: {args.input}")
                sys.exit(1)
            
            generated_files = generator.batch_process_directory(args.input, args.pattern)
            
            if generated_files:
                print(f"\n🎉 Successfully generated {len(generated_files)} HTML files:")
                for html_file in generated_files:
                    print(f"  📄 {html_file}")
            else:
                print("❌ No files were generated")
                sys.exit(1)
        else:
            # Single file mode
            if not os.path.exists(args.input):
                logger.error(f"❌ Input file not found: {args.input}")
                sys.exit(1)
            
            html_file = generator.generate_documentation_with_fixes(
                args.input, args.output, args.title
            )
            
            print(f"\n🎉 Documentation generated successfully!")
            print(f"📄 Input:  {args.input}")
            print(f"📄 Output: {html_file}")
            print(f"🌐 Open the HTML file in your browser to view the documentation")
    
    except KeyboardInterrupt:
        logger.info("⏹️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        generator.cleanup_temp_files()

if __name__ == "__main__":
    main()
