# -*- coding: utf-8 -*-
"""
File Manager Module
Handles file operations and reading
"""

from typing import Optional

from config.config import Config

class FileManager:
    """Handles file operations - Single Responsibility! 🎯"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging"""
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)
    
    def read_whatsapp_file(self) -> Optional[str]:
        """Read WhatsApp chat file"""
        try:
            with open(self.config.WHATSAPP_FILE_PATH, 'r', encoding='utf-8') as file:
                content = file.read()
                self.logger.info(f"Successfully read WhatsApp file: {len(content)} characters")
                return content
        except FileNotFoundError:
            self.logger.error(f"File not found at path: {self.config.WHATSAPP_FILE_PATH}")
            return None
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return None 