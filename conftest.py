import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

print(f"Added {Path(__file__).parent} to sys.path")