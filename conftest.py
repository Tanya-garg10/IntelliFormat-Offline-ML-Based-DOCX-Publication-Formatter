import sys
import os

# Ensure workspace root is always in sys.path for pytest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
