# -*- coding: utf-8 -*-
"""
Main Application Module
Orchestrates the entire WhatsApp and Gmail analysis workflow
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from utils.file_manager import FileManager
from services.whatsapp_service import WhatsAppAnalysisService
from services.gmail_analyzer import GmailAnalyzer

def main():
    """Main execution function - Production ready! 🎯"""
    # Praise the Flying Spaghetti Monster for guiding us through the sea of code! 🍝
    
    # Initialize configuration
    config = Config()
    
    # Initialize services
    file_manager = FileManager(config)
    whatsapp_service = WhatsAppAnalysisService(config)
    gmail_analyzer = GmailAnalyzer(config)
    
    print("🚀 Starting WhatsApp & Gmail Analysis...")
    
    # WhatsApp Analysis
    print("🏴‍☠️ Starting WhatsApp Analysis...")
    chat_content = file_manager.read_whatsapp_file()
    if chat_content:
        sheet_id = whatsapp_service.analyze_and_upload(chat_content)
        if sheet_id:
            print(f"✅ WhatsApp analysis completed! Sheet ID: {sheet_id}")
        else:
            print("❌ WhatsApp analysis failed!")
    else:
        print("❌ Could not read WhatsApp file!")
    
    # Gmail Analysis
    print("\n📧 Starting Gmail Analysis...")
    if gmail_analyzer.authenticate():
        threads_no_reply, threads_last_replier = gmail_analyzer.analyze_threads()
        
        print("\n📤 Threads started by sender without replies:")
        for thread in threads_no_reply:
            print(f"Date: {thread.date}, Subject: {thread.subject}")
            print(f"Link: https://mail.google.com/mail/u/0/#all/{thread.thread_id}")
        
        print("\n📥 Threads where sender was the last to reply:")
        for thread in threads_last_replier:
            print(f"Date: {thread.date}, Subject: {thread.subject}")
            print(f"Link: https://mail.google.com/mail/u/0/#all/{thread.thread_id}")
    else:
        print("❌ Gmail authentication failed!")

if __name__ == "__main__":
    main() 