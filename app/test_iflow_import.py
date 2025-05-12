"""
Test script to verify that the iflow_matcher module can be imported correctly.
"""

import os
import sys

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print("Files in current directory:", os.listdir("."))

try:
    print("\nTrying to import iflow_matcher...")
    import iflow_matcher
    print("Successfully imported iflow_matcher module")
    
    print("\nTrying to import process_markdown_for_iflow from iflow_matcher...")
    from iflow_matcher import process_markdown_for_iflow
    print("Successfully imported process_markdown_for_iflow function")
    
    print("\nModule details:")
    print("Module file:", iflow_matcher.__file__)
    print("Module name:", iflow_matcher.__name__)
    
    print("\nFunction details:")
    print("Function name:", process_markdown_for_iflow.__name__)
    print("Function module:", process_markdown_for_iflow.__module__)
    
    print("\nImport test successful!")
except ImportError as e:
    print(f"\nImport error: {str(e)}")
    print("Import test failed!")
except Exception as e:
    print(f"\nUnexpected error: {str(e)}")
    print("Import test failed!")
