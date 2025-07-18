#!/usr/bin/env python3
"""
WhatsApp Analyzer - Main Entry Point
Orchestrates the entire WhatsApp and Gmail analysis workflow
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.main import main

if __name__ == "__main__":
    main() 