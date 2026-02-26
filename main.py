#!/usr/bin/env python3
"""
WhatsApp Analyzer - Main Entry Point
Orchestrates the entire WhatsApp and Gmail analysis workflow
"""

import sys
import os

from dotenv import load_dotenv

load_dotenv()

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.main import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1) 