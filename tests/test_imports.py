#!/usr/bin/env python3
"""
Test imports to ensure the new project structure works correctly
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        # Test core imports
        from core.main import main
        print("✅ Core imports successful")
        
        # Test config imports
        from config.config import Config
        print("✅ Config imports successful")
        
        # Test models imports
        from models.models import ChatMessage, MessageType, ThreadAnalysis
        print("✅ Models imports successful")
        
        # Test services imports
        from services.whatsapp_analyzer import WhatsAppAnalyzer
        from services.whatsapp_service import WhatsAppAnalysisService
        from services.gmail_analyzer import GmailAnalyzer
        from services.google_sheets_manager import GoogleSheetsManager
        print("✅ Services imports successful")
        
        # Test utils imports
        from utils.file_manager import FileManager
        print("✅ Utils imports successful")
        
        print("\n🎉 All imports successful! The new project structure is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 