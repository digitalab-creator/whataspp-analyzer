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


def main() -> None:
    """Run WhatsApp and Gmail analysis."""
    config = Config()
    file_manager = FileManager(config)
    whatsapp_service = WhatsAppAnalysisService(config)
    gmail_analyzer = GmailAnalyzer(config)

    print("Starting WhatsApp & Gmail Analysis...")

    # WhatsApp Analysis
    chat_content = file_manager.read_whatsapp_file()
    if not chat_content:
        print("Could not read WhatsApp file.", file=sys.stderr)
        sys.exit(1)
    sheet_id = whatsapp_service.analyze_and_upload(chat_content)
    if not sheet_id:
        print("WhatsApp analysis failed.", file=sys.stderr)
        sys.exit(1)
    print(f"WhatsApp analysis completed. Sheet ID: {sheet_id}")

    # Gmail Analysis
    if not gmail_analyzer.authenticate():
        print("Gmail authentication failed.", file=sys.stderr)
        sys.exit(1)
    threads_no_reply, threads_last_replier = gmail_analyzer.analyze_threads()
    print("\nThreads started by sender without replies:")
    for thread in threads_no_reply:
        print(f"Date: {thread.date}, Subject: {thread.subject}")
        print(f"Link: https://mail.google.com/mail/u/0/#all/{thread.thread_id}")
    print("\nThreads where sender was the last to reply:")
    for thread in threads_last_replier:
        print(f"Date: {thread.date}, Subject: {thread.subject}")
        print(f"Link: https://mail.google.com/mail/u/0/#all/{thread.thread_id}")


if __name__ == "__main__":
    main() 