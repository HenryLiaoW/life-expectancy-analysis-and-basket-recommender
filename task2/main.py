#!/usr/bin/env python3
"""
Convenient launcher for Supermarket Recommendation System CLI

This script sets up the Python path and launches the CLI application.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import and run CLI
from task2.cli import main

if __name__ == "__main__":
    main()
