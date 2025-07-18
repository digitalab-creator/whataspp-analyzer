# -*- coding: utf-8 -*-
"""
WhatsApp Analysis Service Module
Orchestrates WhatsApp analysis workflow
"""

from typing import List, Optional
import gspread

from config.config import Config
from models.models import ChatMessage
from services.whatsapp_analyzer import WhatsAppAnalyzer
from services.google_sheets_manager import GoogleSheetsManager

class WhatsAppAnalysisService:
    """Service for WhatsApp analysis - Business Logic Layer! 🎯"""
    
    def __init__(self, config: Config):
        self.config = config
        self.analyzer = WhatsAppAnalyzer(config)
        self.sheets_manager = GoogleSheetsManager(config)
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging"""
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def analyze_and_upload(self, chat_content: str) -> Optional[str]:
        """Main analysis and upload workflow"""
        try:
            # Parse messages
            messages = self.analyzer.parse_chat_content(chat_content)
            if not messages:
                self.logger.warning("No messages to analyze")
                return None
            
            # Authenticate with Google Sheets
            if not self.sheets_manager.authenticate():
                self.logger.error("Failed to authenticate with Google Sheets")
                return None
            
            # Create or get spreadsheet
            sheet = self.sheets_manager.create_or_get_spreadsheet(self.config.DEFAULT_SHEET_TITLE)
            if not sheet:
                self.logger.error("Failed to create or get spreadsheet")
                return None
            
            # Perform analysis and upload
            self._upload_raw_data(sheet, messages)
            self._upload_first_messages_analysis(sheet, messages)
            self._upload_reply_analysis(sheet, messages)
            
            # Share the sheet
            self.sheets_manager.share_spreadsheet(sheet, self.config.DEFAULT_SHARED_EMAIL)
            
            self.logger.info(f"Analysis completed successfully. Sheet ID: {sheet.id}")
            return sheet.id
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return None
    
    def _upload_raw_data(self, sheet: gspread.Spreadsheet, messages: List[ChatMessage]):
        """Upload raw message data to first worksheet"""
        try:
            worksheet = sheet.get_worksheet(0)
            worksheet.clear()
            
            # Prepare data
            data = [["Date", "Message", "Sender", "Type"]]
            for msg in messages:
                data.append([
                    msg.timestamp.strftime(self.config.SHEET_DATE_FORMAT),
                    msg.content,
                    msg.sender,
                    msg.message_type.value
                ])
            
            self.sheets_manager.update_worksheet_data(worksheet, data)
            
        except Exception as e:
            self.logger.error(f"Failed to upload raw data: {e}")
    
    def _upload_first_messages_analysis(self, sheet: gspread.Spreadsheet, messages: List[ChatMessage]):
        """Upload first messages analysis to Sheet2"""
        try:
            # Analyze first messages
            first_messages_count = self.analyzer.analyze_first_messages(messages)
            
            # Upload to Sheet2
            chart_worksheet = self.sheets_manager.get_or_create_worksheet(sheet, 'Sheet2')
            data = [["Month", "First Messages Count"]]
            for month, count in first_messages_count.items():
                data.append([month, count])
            
            self.sheets_manager.update_worksheet_data(chart_worksheet, data)
            
        except Exception as e:
            self.logger.error(f"Failed to upload first messages analysis: {e}")
    
    def _upload_reply_analysis(self, sheet: gspread.Spreadsheet, messages: List[ChatMessage]):
        """Upload reply analysis to Sheet4"""
        try:
            # Analyze replies
            reply_analysis = self.analyzer.analyze_replies(messages)
            
            # Upload to Sheet4
            sheet4_worksheet = self.sheets_manager.get_or_create_worksheet(sheet, 'Sheet4')
            data = [["Month", "Messages without Reply", "Messages with Reply"]]
            
            # Get all month-years from both analyses
            all_month_years = set(reply_analysis['with_reply'].keys()) | set(reply_analysis['without_reply'].keys())
            
            for month_year in sorted(all_month_years):
                count_without_reply = reply_analysis['without_reply'].get(month_year, 0)
                count_with_reply = reply_analysis['with_reply'].get(month_year, 0)
                data.append([month_year, count_without_reply, count_with_reply])
            
            self.sheets_manager.update_worksheet_data(sheet4_worksheet, data)
            
        except Exception as e:
            self.logger.error(f"Failed to upload reply analysis: {e}") 