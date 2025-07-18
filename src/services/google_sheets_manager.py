# -*- coding: utf-8 -*-
"""
Google Sheets Manager Module
Handles Google Sheets operations and data upload
"""

from typing import List, Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config.config import Config

class GoogleSheetsManager:
    """Handles Google Sheets operations - Single Responsibility! 🎯"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging"""
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def authenticate(self) -> bool:
        """Authenticate with Google Sheets"""
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.config.CLIENT_SECRETS_PATH, scope)
            self.client = gspread.authorize(creds)
            self.logger.info("Successfully authenticated with Google Sheets")
            return True
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False
    
    def create_or_get_spreadsheet(self, title: str) -> Optional[gspread.Spreadsheet]:
        """Create or get existing spreadsheet"""
        try:
            sheet = self.client.open(title)
            self.logger.info(f"Found existing spreadsheet: {title}")
        except gspread.SpreadsheetNotFound:
            sheet = self.client.create(title)
            self.logger.info(f"Created new spreadsheet: {title}")
        
        return sheet
    
    def update_worksheet_data(self, worksheet: gspread.Worksheet, data: List[List[str]], start_cell: str = 'A1'):
        """Update worksheet with data"""
        try:
            if data:
                end_cell = f"{chr(ord('A') + len(data[0]) - 1)}{len(data)}"
                worksheet.update(f'{start_cell}:{end_cell}', data)
                self.logger.info(f"Updated worksheet with {len(data)} rows")
            else:
                self.logger.warning("No data to update")
        except Exception as e:
            self.logger.error(f"Failed to update worksheet: {e}")
    
    def get_or_create_worksheet(self, sheet: gspread.Spreadsheet, title: str) -> gspread.Worksheet:
        """Get existing worksheet or create new one"""
        try:
            worksheet = sheet.worksheet(title)
            worksheet.clear()
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=title, rows="100", cols="20")
        
        return worksheet
    
    def share_spreadsheet(self, sheet: gspread.Spreadsheet, email: str, role: str = 'writer'):
        """Share spreadsheet with specified email"""
        try:
            sheet.share(email, perm_type='user', role=role)
            self.logger.info(f"Shared spreadsheet with {email}")
        except Exception as e:
            self.logger.error(f"Failed to share spreadsheet: {e}") 