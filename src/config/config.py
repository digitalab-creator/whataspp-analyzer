# -*- coding: utf-8 -*-
"""
Configuration module for WhatsApp and Gmail Communication Analyzer
Contains all constants and configuration settings
"""

import os

class Config:
    """Configuration constants to avoid magic strings"""
    
    # Date formats
    WHATSAPP_DATE_FORMAT = '%d/%m/%Y, %H:%M'
    SHEET_DATE_FORMAT = "%d/%m/%Y, %H:%M"
    MONTH_FORMAT = '%Y-%m'
    DATE_FORMAT = '%Y-%m-%d'
    
    # User identifiers
    SENDER_NAME = "אור שוורץ"
    RECIPIENT_NAME = "מיכל ט"
    SENDER_EMAIL = "or.shvartz70@gmail.com"
    RECIPIENT_EMAIL = "michaltad@gmail.com"
    
    # File paths - production ready with environment variables
    CLIENT_SECRETS_PATH = os.getenv(
        'CLIENT_SECRETS_PATH', 
        './credentials/service-account.json'
    )
    WHATSAPP_FILE_PATH = os.getenv(
        'WHATSAPP_FILE_PATH',
        './data/whatsapp-chat.txt'
    )
    TOKEN_PATH = os.getenv(
        'TOKEN_PATH',
        './credentials/token.pickle'
    )
    AUTH_CLIENT_SECRET_PATH = os.getenv(
        'AUTH_CLIENT_SECRET_PATH',
        './credentials/auth-client-secret.json'
    )
    
    # Google API scopes
    DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    # Default values
    DEFAULT_SHEET_TITLE = os.getenv('DEFAULT_SHEET_TITLE', 'WhatsApp Chat Analysis')
    DEFAULT_SHARED_EMAIL = os.getenv('DEFAULT_SHARED_EMAIL', 'or.shvartz70@gmail.com')
    
    # Docker-specific settings
    DOCKER_MODE = os.getenv('DOCKER_MODE', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO') 