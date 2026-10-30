import logging
import sys
from src.config import settings

def setup_logger(name: str):
    """Setup logger with custom formatting"""
    
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        return logger
    # Ensure stdout/stderr use UTF-8 to prevent UnicodeEncodeError on Windows consoles
    try:
        if sys.stdout and (sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        if sys.stderr and (sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger
