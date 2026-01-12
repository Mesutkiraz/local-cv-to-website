"""
Logger Utility
==============
Centralized logging with pretty formatting.
Single Responsibility: Handle all logging operations.
"""

from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """Log level enumeration."""
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BRAIN = "BRAIN"
    CODE = "CODE"
    FILE = "FILE"
    ROCKET = "ROCKET"
    VRAM = "VRAM"


class Logger:
    """
    Pretty console logger with timestamps and icons.
    Single Responsibility: Only handles logging.
    """
    
    ICONS = {
        LogLevel.INFO: "ℹ️ ",
        LogLevel.SUCCESS: "✅",
        LogLevel.WARNING: "⚠️ ",
        LogLevel.ERROR: "❌",
        LogLevel.BRAIN: "🧠",
        LogLevel.CODE: "💻",
        LogLevel.FILE: "📄",
        LogLevel.ROCKET: "🚀",
        LogLevel.VRAM: "🎮",
    }
    
    def __init__(self, prefix: Optional[str] = None):
        """Initialize logger with optional prefix."""
        self.prefix = prefix
    
    def _format_message(self, message: str, level: LogLevel) -> str:
        """Format a log message with timestamp and icon."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = self.ICONS.get(level, "•")
        prefix = f"[{self.prefix}] " if self.prefix else ""
        return f"[{timestamp}] {icon}  {prefix}{message}"
    
    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """Log a message at the specified level."""
        print(self._format_message(message, level))
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.log(message, LogLevel.INFO)
    
    def success(self, message: str) -> None:
        """Log a success message."""
        self.log(message, LogLevel.SUCCESS)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.log(message, LogLevel.WARNING)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.log(message, LogLevel.ERROR)
    
    def brain(self, message: str) -> None:
        """Log a brain/AI message."""
        self.log(message, LogLevel.BRAIN)
    
    def code(self, message: str) -> None:
        """Log a code-related message."""
        self.log(message, LogLevel.CODE)
    
    def file(self, message: str) -> None:
        """Log a file-related message."""
        self.log(message, LogLevel.FILE)
    
    def rocket(self, message: str) -> None:
        """Log a rocket/launch message."""
        self.log(message, LogLevel.ROCKET)
    
    def vram(self, message: str) -> None:
        """Log a VRAM/GPU message."""
        self.log(message, LogLevel.VRAM)


# Global logger instance for convenience
_default_logger = Logger()


def log(message: str, level: str = "INFO") -> None:
    """
    Convenience function for quick logging.
    Maintains backward compatibility with original implementation.
    """
    try:
        log_level = LogLevel[level.upper()]
    except KeyError:
        log_level = LogLevel.INFO
    _default_logger.log(message, log_level)
