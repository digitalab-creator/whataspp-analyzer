# -*- coding: utf-8 -*-
"""
Data models for WhatsApp and Gmail Communication Analyzer
Contains data classes and enums
"""

from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class MessageType(Enum):
    """Enum for message types to avoid magic strings"""
    SENDER_MESSAGE = "sender"
    RECIPIENT_MESSAGE = "recipient"
    UNKNOWN = "unknown"

@dataclass
class ChatMessage:
    """Data class for chat messages"""
    timestamp: datetime
    content: str
    sender: str
    message_type: MessageType

@dataclass
class ThreadAnalysis:
    """Data class for thread analysis results"""
    thread_id: str
    date: str
    subject: str
    has_reply: bool
    last_sender: str 