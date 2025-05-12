import os
import sys

# Add paths to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
getiflow_path = os.path.join(parent_dir, "GetIflowEquivalent")
local_getiflow_path = os.path.join(current_dir, "GetIflowEquivalent")

print(f"Current directory: {current_dir}")
print(f"Parent directory: {parent_dir}")
print(f"GetIflowEquivalent path (parent): {getiflow_path}")
print(f"GetIflowEquivalent path (local): {local_getiflow_path}")

# Check if directories exist
print(f"Parent GetIflowEquivalent exists: {os.path.exists(getiflow_path)}")
print(f"Local GetIflowEquivalent exists: {os.path.exists(local_getiflow_path)}")

# Add paths to sys.path
if os.path.exists(getiflow_path):
    sys.path.insert(0, getiflow_path)
    print(f"Added {getiflow_path} to sys.path")

if os.path.exists(local_getiflow_path):
    sys.path.insert(0, local_getiflow_path)
    print(f"Added {local_getiflow_path} to sys.path")

# Try to import
try:
    print("Trying to import from GetIflowEquivalent.main...")
    from GetIflowEquivalent.main import process_markdown_for_iflow
    print("Successfully imported process_markdown_for_iflow from GetIflowEquivalent.main")
except ImportError as e:
    print(f"Error importing from GetIflowEquivalent.main: {str(e)}")
    try:
        print("Trying to import from main...")
        from main import process_markdown_for_iflow
        print("Successfully imported process_markdown_for_iflow from main")
    except ImportError as e:
        print(f"Error importing from main: {str(e)}")
        print("All import attempts failed")

# Print sys.path
print("\nPython path:")
for path in sys.path:
    print(f"  {path}")
