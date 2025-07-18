# -*- coding: utf-8 -*-
"""
WhatsApp Chat Analyzer Module
Handles WhatsApp chat parsing and analysis
"""

import re
import calendar
import collections
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from config.config import Config
from models.models import ChatMessage, MessageType

class WhatsAppAnalyzer:
    """Handles WhatsApp chat analysis - Single Responsibility Principle! 🎯"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging to avoid silent error swallowing"""
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def parse_chat_content(self, chat_content: str) -> List[ChatMessage]:
        """Parse WhatsApp chat content into structured messages"""
        if not chat_content:
            self.logger.warning("No chat content provided")
            return []
        
        messages = []
        lines = chat_content.split("\n")
        
        for line in lines:
            try:
                if self._is_valid_message_line(line):
                    message = self._parse_message_line(line)
                    if message:
                        messages.append(message)
            except Exception as e:
                self.logger.error(f"Error parsing line: {line[:50]}... Error: {e}")
                continue
        
        self.logger.info(f"Successfully parsed {len(messages)} messages")
        return messages
    
    def _is_valid_message_line(self, line: str) -> bool:
        """Check if line matches WhatsApp message format"""
        return bool(re.match(r"\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ", line, re.IGNORECASE))
    
    def _parse_message_line(self, line: str) -> Optional[ChatMessage]:
        """Parse a single message line"""
        try:
            date_str, message_content = line.split(" - ", 1)
            timestamp = datetime.strptime(date_str, self.config.WHATSAPP_DATE_FORMAT)
            
            # Determine message type based on content
            if self.config.SENDER_NAME in message_content:
                message_type = MessageType.SENDER_MESSAGE
                sender = self.config.SENDER_NAME
            elif self.config.RECIPIENT_NAME in message_content:
                message_type = MessageType.RECIPIENT_MESSAGE
                sender = self.config.RECIPIENT_NAME
            else:
                message_type = MessageType.UNKNOWN
                sender = "Unknown"
            
            return ChatMessage(
                timestamp=timestamp,
                content=message_content.strip(),
                sender=sender,
                message_type=message_type
            )
        except Exception as e:
            self.logger.error(f"Failed to parse message line: {e}")
            return None
    
    def analyze_first_messages(self, messages: List[ChatMessage]) -> Dict[str, int]:
        """Analyze first messages of the day"""
        if not messages:
            return {}
        
        # Get date range
        start_date = min(messages, key=lambda x: x.timestamp).timestamp
        end_date = max(messages, key=lambda x: x.timestamp).timestamp
        month_years = self._generate_month_years(start_date, end_date)
        
        first_messages_count = {month_year: 0 for month_year in month_years}
        seen_dates = set()
        
        for message in messages:
            if message.message_type == MessageType.RECIPIENT_MESSAGE:
                date_str = message.timestamp.strftime(self.config.MONTH_FORMAT)
                date_key = message.timestamp.date()
                
                if date_key not in seen_dates:
                    first_messages_count[date_str] += 1
                    seen_dates.add(date_key)
        
        return first_messages_count
    
    def analyze_replies(self, messages: List[ChatMessage]) -> Dict[str, Dict[str, int]]:
        """Analyze reply patterns"""
        if not messages:
            return {'with_reply': {}, 'without_reply': {}}
        
        # Get date range
        start_date = min(messages, key=lambda x: x.timestamp).timestamp
        end_date = max(messages, key=lambda x: x.timestamp).timestamp
        month_years = self._generate_month_years(start_date, end_date)
        
        or_messages_without_reply = collections.defaultdict(int)
        or_messages_with_reply = collections.defaultdict(int)
        
        for month_year in month_years:
            daily_messages = [msg for msg in messages if msg.timestamp.strftime(self.config.MONTH_FORMAT) == month_year]
            seen_dates = set()
            
            for message in daily_messages:
                date_str = message.timestamp.strftime(self.config.DATE_FORMAT)
                if date_str in seen_dates:
                    continue
                seen_dates.add(date_str)
                
                if message.message_type == MessageType.SENDER_MESSAGE:
                    # Check if recipient replied on the same day
                    has_reply = any(
                        m.message_type == MessageType.RECIPIENT_MESSAGE 
                        for m in daily_messages 
                        if m.timestamp.strftime(self.config.DATE_FORMAT) == date_str
                    )
                    
                    if has_reply:
                        or_messages_with_reply[month_year] += 1
                    else:
                        or_messages_without_reply[month_year] += 1
        
        return {
            'with_reply': dict(or_messages_with_reply),
            'without_reply': dict(or_messages_without_reply)
        }
    
    def _generate_month_years(self, start_date: datetime, end_date: datetime) -> List[str]:
        """Generate all month-year combinations between start and end dates"""
        month_years = []
        current_date = start_date.replace(day=1)
        
        while current_date <= end_date:
            month_years.append(current_date.strftime(self.config.MONTH_FORMAT))
            days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
            current_date += timedelta(days=days_in_month)
        
        return month_years