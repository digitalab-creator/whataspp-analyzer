# -*- coding: utf-8 -*-
"""
Gmail Analyzer Module
Handles Gmail operations and thread analysis
"""

import os
import pickle
from typing import List, Tuple, Optional, Dict
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from config.config import Config
from models.models import ThreadAnalysis

class GmailAnalyzer:
    """Handles Gmail analysis - Single Responsibility! 🎯"""
    
    def __init__(self, config: Config):
        self.config = config
        self.service = None
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging"""
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail API"""
        try:
            creds = None
            
            if os.path.exists(self.config.TOKEN_PATH):
                with open(self.config.TOKEN_PATH, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = Flow.from_client_secrets_file(
                        self.config.AUTH_CLIENT_SECRET_PATH,
                        scopes=self.config.GMAIL_SCOPES,
                        redirect_uri='http://localhost'
                    )
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    self.logger.info(f'Please go to this URL and finish the authentication flow: {auth_url}')
                    code = input('Enter the authorization code: ')
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    
                    with open(self.config.TOKEN_PATH, 'wb') as token:
                        pickle.dump(creds, token)
            
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Successfully authenticated with Gmail API")
            return True
            
        except Exception as e:
            self.logger.error(f"Gmail authentication failed: {e}")
            return False
    
    def analyze_threads(self) -> Tuple[List[ThreadAnalysis], List[ThreadAnalysis]]:
        """Analyze email threads between sender and recipient"""
        if not self.service:
            self.logger.error("Gmail service not authenticated")
            return [], []
        
        try:
            # Search for threads
            thread_ids = self._search_threads()
            
            threads_started_by_sender_no_reply = []
            threads_with_sender_as_last_replier = []
            
            for thread_id in thread_ids:
                analysis = self._analyze_single_thread(thread_id)
                if analysis:
                    if analysis.has_reply == False:
                        threads_started_by_sender_no_reply.append(analysis)
                    if self.config.SENDER_EMAIL.lower() in analysis.last_sender.lower():
                        threads_with_sender_as_last_replier.append(analysis)
            
            self.logger.info(f"Found {len(threads_started_by_sender_no_reply)} threads without replies")
            self.logger.info(f"Found {len(threads_with_sender_as_last_replier)} threads with sender as last replier")
            
            return threads_started_by_sender_no_reply, threads_with_sender_as_last_replier
            
        except Exception as e:
            self.logger.error(f"Thread analysis failed: {e}")
            return [], []
    
    def _search_threads(self) -> List[str]:
        """Search for threads between sender and recipient"""
        try:
            query = f'from:{self.config.SENDER_EMAIL} to:{self.config.RECIPIENT_EMAIL}'
            response = self.service.users().threads().list(userId='me', q=query).execute()
            threads = response.get('threads', [])
            return [thread['id'] for thread in threads]
        except HttpError as error:
            self.logger.error(f'Error searching threads: {error}')
            return []
    
    def _analyze_single_thread(self, thread_id: str) -> Optional[ThreadAnalysis]:
        """Analyze a single email thread"""
        try:
            thread = self.service.users().threads().get(userId='me', id=thread_id, format='full').execute()
            messages = thread.get('messages', [])
            
            if not messages:
                return None
            
            first_message = messages[0]
            last_message = messages[-1]
            
            # Get headers
            first_sender = self._extract_sender(first_message)
            last_sender = self._extract_sender(last_message)
            
            # Check for replies from recipient
            has_reply_from_recipient = any(
                self.config.RECIPIENT_EMAIL.lower() in self._extract_sender(msg).lower()
                for msg in messages
            )
            
            # Get thread details
            date, subject = self._get_thread_details(thread_id)
            
            return ThreadAnalysis(
                thread_id=thread_id,
                date=date or "No Date",
                subject=subject or "No Subject",
                has_reply=has_reply_from_recipient,
                last_sender=last_sender
            )
            
        except HttpError as error:
            self.logger.error(f'Error analyzing thread {thread_id}: {error}')
            return None
    
    def _extract_sender(self, message: Dict) -> str:
        """Extract sender from message headers"""
        headers = message.get('payload', {}).get('headers', [])
        return next(
            (header['value'] for header in headers if header['name'].lower() == 'from'),
            'Unknown'
        )
    
    def _get_thread_details(self, thread_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Get thread date and subject"""
        try:
            thread = self.service.users().threads().get(userId='me', id=thread_id, format='metadata').execute()
            messages = thread.get('messages', [])
            
            if not messages:
                return None, None
            
            headers = messages[0].get('payload', {}).get('headers', [])
            subject = next(
                (header['value'] for header in headers if header['name'].lower() == 'subject'),
                'No Subject'
            )
            date = next(
                (header['value'] for header in headers if header['name'].lower() == 'date'),
                'No Date'
            )
            
            return date, subject
            
        except HttpError as error:
            self.logger.error(f'Error getting thread details for {thread_id}: {error}')
            return None, None 